"""
Validacion final determinista del producto Django generado.

El validador no corrige el producto. Trabaja sobre una copia del codigo final
para que comandos como migrate o seed_data no alteren el entregable generado
por el LLM.
"""

from __future__ import annotations

import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

from pipeline.utils.django_runner import (
    _detectar_commands_apps_no_instaladas,
    _resolver_python_django_check,
    _resumir_salida,
)
from pipeline.validation.schemas import (
    ResultadoComando,
    ResultadoMigraciones,
    ResultadoRuta,
    ResultadoTemplate,
    ReviewFinal,
    ValidacionFinal,
)


PROTOCOLO_VALIDACION_FINAL = "validacion_final_v1"

RUTAS_MINIMAS = [
    "/",
    "/barcos/",
    "/cesta/",
    "/accounts/registro/",
    "/accounts/login/",
    "/reserva/paso1/",
    "/reserva/paso2/",
    "/reserva/paso3/",
    "/admin/",
    "/admin-panel/",
]

# Nombre canónico estándar para la template del paso 3.
# El resolver dinámico acepta también el nombre alternativo 'checkout_step3.html'
# si es el que el producto entrega, para no invalidar un producto correcto por
# una diferencia de nombre no contemplada en el contrato técnico.
TEMPLATES_CRITICAS = [
    "reservations/step3.html",
]


def construir_validacion_final(
    *,
    id_ejecucion: str,
    codigo_dir: Path,
    salida_dir: Path,
    timeout_s: int = 60,
    runserver_timeout_s: int = 20,
) -> ValidacionFinal:
    """
    Ejecuta la validacion final sobre una copia del codigo generado.

    Args:
        id_ejecucion: run_id del pipeline.
        codigo_dir: carpeta `codigo/` final, normalmente 06_sprint_3/codigo.
        salida_dir: carpeta donde se crea `_validacion_tmp/codigo`.
        timeout_s: timeout para comandos manage.py.
        runserver_timeout_s: tiempo maximo de espera del servidor local.
    """
    checks_planificados = _checks_planificados()
    observaciones: list[str] = []
    preparacion_manual_requerida: list[str] = []

    copia_dir = _preparar_copia_validacion(codigo_dir, salida_dir)
    manage_py = copia_dir / "manage.py"
    python_path, origen_python = _resolver_python_django_check()

    templates_criticas = _resolver_templates_criticas(copia_dir)

    if python_path is None:
        check = _comando_no_ejecutado(
            nombre="check",
            comando=["python", "manage.py", "check"],
            timeout_s=timeout_s,
            motivo=origen_python,
        )
        migraciones = ResultadoMigraciones(
            ok=False,
            apps_con_modelos=[],
            apps_con_migraciones=[],
            apps_sin_migraciones=[],
        )
        migrate = _comando_no_ejecutado(
            nombre="migrate",
            comando=["python", "manage.py", "migrate", "--noinput"],
            timeout_s=timeout_s,
            motivo=origen_python,
        )
        seed_data = _comando_no_ejecutado(
            nombre="seed_data",
            comando=["python", "manage.py", "seed_data"],
            timeout_s=timeout_s,
            motivo=origen_python,
        )
        runserver = _comando_no_ejecutado(
            nombre="runserver",
            comando=["python", "manage.py", "runserver"],
            timeout_s=runserver_timeout_s,
            motivo=origen_python,
        )
        rutas = [
            _ruta_no_ejecutada(path, origen_python)
            for path in RUTAS_MINIMAS
        ]
        templates = [
            _template_no_ejecutada(template, origen_python)
            for template in templates_criticas
        ]
    elif not manage_py.exists():
        motivo = f"No existe manage.py en la copia de validacion: {copia_dir}"
        check = _comando_no_ejecutado(
            nombre="check",
            comando=[str(python_path), "manage.py", "check"],
            timeout_s=timeout_s,
            motivo=motivo,
        )
        migraciones = ResultadoMigraciones(
            ok=False,
            apps_con_modelos=[],
            apps_con_migraciones=[],
            apps_sin_migraciones=[],
        )
        migrate = _comando_no_ejecutado(
            nombre="migrate",
            comando=[str(python_path), "manage.py", "migrate", "--noinput"],
            timeout_s=timeout_s,
            motivo=motivo,
        )
        seed_data = _comando_no_ejecutado(
            nombre="seed_data",
            comando=[str(python_path), "manage.py", "seed_data"],
            timeout_s=timeout_s,
            motivo=motivo,
        )
        runserver = _comando_no_ejecutado(
            nombre="runserver",
            comando=[str(python_path), "manage.py", "runserver"],
            timeout_s=runserver_timeout_s,
            motivo=motivo,
        )
        rutas = [_ruta_no_ejecutada(path, motivo) for path in RUTAS_MINIMAS]
        templates = [
            _template_no_ejecutada(template, motivo)
            for template in templates_criticas
        ]
    else:
        check = _ejecutar_manage(
            nombre="check",
            python_path=python_path,
            codigo_dir=copia_dir,
            args=["check"],
            timeout_s=timeout_s,
        )
        migraciones = _detectar_migraciones(copia_dir)
        if not migraciones.ok:
            preparacion_manual_requerida.append(
                "El producto no incluye migraciones iniciales para todas las "
                "apps propias con modelos. `migrate --run-syncdb` podria "
                "desbloquear inspeccion manual, pero no cuenta como criterio "
                "principal."
            )

        migrate = _ejecutar_manage(
            nombre="migrate",
            python_path=python_path,
            codigo_dir=copia_dir,
            args=["migrate", "--noinput"],
            timeout_s=timeout_s,
        )
        if not migrate.ok:
            preparacion_manual_requerida.append(
                "El `migrate` estandar no fue correcto. No se ejecuta "
                "`migrate --run-syncdb` como correccion dentro del validador."
            )

        if _existe_comando_seed_data(copia_dir):
            seed_data = _ejecutar_manage(
                nombre="seed_data",
                python_path=python_path,
                codigo_dir=copia_dir,
                args=["seed_data"],
                timeout_s=timeout_s,
            )
        else:
            seed_data = _comando_no_ejecutado(
                nombre="seed_data",
                comando=[str(python_path), "manage.py", "seed_data"],
                timeout_s=timeout_s,
                motivo="No existe comando de gestion seed_data.",
            )
            preparacion_manual_requerida.append(
                "No existe comando seed_data para cargar datos de prueba."
            )

        templates = [
            _renderizar_template(
                python_path=python_path,
                codigo_dir=copia_dir,
                template=template,
                timeout_s=timeout_s,
            )
            for template in templates_criticas
        ]

        runserver, rutas = _validar_runserver_y_rutas(
            python_path=python_path,
            codigo_dir=copia_dir,
            timeout_s=runserver_timeout_s,
            rutas=RUTAS_MINIMAS,
        )

    incidencias = _construir_incidencias(
        check=check,
        migraciones=migraciones,
        migrate=migrate,
        seed_data=seed_data,
        runserver=runserver,
        rutas=rutas,
        templates=templates,
    )
    # Check estático: apps con management/commands/ no incluidas en INSTALLED_APPS.
    # No requiere ejecutar Django; se añade independientemente del resultado de check.
    incidencias.extend(_detectar_commands_apps_no_instaladas(copia_dir))

    factores_bloqueantes = _factores_bloqueantes(
        check=check,
        migrate=migrate,
        runserver=runserver,
    )
    checks_ejecutados, checks_no_ejecutados = _resumen_checks(
        check=check,
        migraciones=migraciones,
        migrate=migrate,
        seed_data=seed_data,
        runserver=runserver,
        rutas=rutas,
        templates=templates,
    )
    clasificacion = _clasificar(
        check=check,
        migrate=migrate,
        runserver=runserver,
        incidencias=incidencias,
        factores_bloqueantes=factores_bloqueantes,
    )
    ok_global = not incidencias

    review_final = ReviewFinal(
        protocolo_validacion=PROTOCOLO_VALIDACION_FINAL,
        checks_planificados=checks_planificados,
        checks_ejecutados=checks_ejecutados,
        checks_no_ejecutados=checks_no_ejecutados,
        incidencias=incidencias,
        factores_bloqueantes=factores_bloqueantes,
        clasificacion=clasificacion,
    )

    return ValidacionFinal(
        id_ejecucion=id_ejecucion,
        codigo_dir=str(codigo_dir),
        copia_validacion_dir=str(copia_dir),
        ok_global=ok_global,
        check=check,
        migraciones=migraciones,
        migrate=migrate,
        seed_data=seed_data,
        runserver=runserver,
        rutas=rutas,
        templates=templates,
        preparacion_manual_requerida=preparacion_manual_requerida,
        observaciones=observaciones,
        review_final=review_final,
    )


def _checks_planificados() -> list[str]:
    checks = [
        "check",
        "migraciones",
        "migrate",
        "seed_data",
        "runserver",
    ]
    checks.extend(f"ruta:{path}" for path in RUTAS_MINIMAS)
    checks.extend(f"template:{template}" for template in TEMPLATES_CRITICAS)
    return checks


def _resolver_templates_criticas(codigo_dir: Path) -> list[str]:
    """
    Devuelve la lista real de templates críticas a validar para este producto.

    Para el paso 3 acepta tanto 'step3.html' como 'checkout_step3.html':
    ambos son nombres válidos derivados de la arquitectura del producto. Si
    ninguno existe, devuelve el nombre estándar para que el fallo quede
    documentado. Esto evita acoplar el validador a un nombre histórico único
    que no forma parte del contrato técnico aceptado.
    """
    templates_root = codigo_dir / "templates"
    paso3_candidatos = [
        "reservations/step3.html",
        "reservations/checkout_step3.html",
    ]
    for candidato in paso3_candidatos:
        if (templates_root / candidato).exists():
            return [candidato]
    # Ninguno existe: devuelve el nombre estándar para documentar la ausencia.
    return ["reservations/step3.html"]


def _preparar_copia_validacion(codigo_dir: Path, salida_dir: Path) -> Path:
    tmp_root = salida_dir / "_validacion_tmp"
    copia_dir = tmp_root / "codigo"
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir(parents=True, exist_ok=True)
    if codigo_dir.exists():
        shutil.copytree(codigo_dir, copia_dir)
    else:
        copia_dir.mkdir(parents=True, exist_ok=True)
    return copia_dir


def _comando_no_ejecutado(
    *,
    nombre: str,
    comando: list[str],
    timeout_s: int,
    motivo: str,
) -> ResultadoComando:
    return ResultadoComando(
        nombre=nombre,
        comando=comando,
        ejecutado=False,
        ok=False,
        returncode=None,
        timeout_s=timeout_s,
        motivo_no_ejecutado=motivo,
    )


def _ejecutar_manage(
    *,
    nombre: str,
    python_path: Path,
    codigo_dir: Path,
    args: list[str],
    timeout_s: int,
) -> ResultadoComando:
    comando = [str(python_path), "manage.py", *args]
    try:
        completed = subprocess.run(
            comando,
            cwd=codigo_dir,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        return ResultadoComando(
            nombre=nombre,
            comando=comando,
            ejecutado=True,
            ok=completed.returncode == 0,
            returncode=completed.returncode,
            stdout_resumen=_resumir_salida(completed.stdout),
            stderr_resumen=_resumir_salida(completed.stderr),
            timeout_s=timeout_s,
            timeout=False,
        )
    except subprocess.TimeoutExpired as e:
        stdout = (
            e.stdout.decode("utf-8", errors="replace")
            if isinstance(e.stdout, bytes)
            else (e.stdout or "")
        )
        stderr = (
            e.stderr.decode("utf-8", errors="replace")
            if isinstance(e.stderr, bytes)
            else (e.stderr or "")
        )
        return ResultadoComando(
            nombre=nombre,
            comando=comando,
            ejecutado=True,
            ok=False,
            returncode=None,
            stdout_resumen=_resumir_salida(stdout),
            stderr_resumen=_resumir_salida(stderr or f"Timeout ejecutando {nombre}."),
            timeout_s=timeout_s,
            timeout=True,
        )
    except Exception as e:
        return ResultadoComando(
            nombre=nombre,
            comando=comando,
            ejecutado=True,
            ok=False,
            returncode=None,
            stderr_resumen=f"{type(e).__name__}: {e}",
            timeout_s=timeout_s,
            timeout=False,
        )


def _detectar_migraciones(codigo_dir: Path) -> ResultadoMigraciones:
    apps_con_modelos: list[str] = []
    apps_con_migraciones: list[str] = []
    apps_sin_migraciones: list[str] = []

    for models_py in sorted(codigo_dir.glob("*/models.py")):
        app_dir = models_py.parent
        app_name = app_dir.name
        try:
            contenido = models_py.read_text(encoding="utf-8", errors="replace")
        except Exception:
            contenido = ""
        if "models.Model" not in contenido:
            continue
        apps_con_modelos.append(app_name)
        migrations_dir = app_dir / "migrations"
        tiene_migracion = migrations_dir.exists() and any(
            path.is_file() and path.name != "__init__.py" and path.suffix == ".py"
            for path in migrations_dir.iterdir()
        )
        if tiene_migracion:
            apps_con_migraciones.append(app_name)
        else:
            apps_sin_migraciones.append(app_name)

    return ResultadoMigraciones(
        ok=not apps_sin_migraciones,
        apps_con_modelos=apps_con_modelos,
        apps_con_migraciones=apps_con_migraciones,
        apps_sin_migraciones=apps_sin_migraciones,
    )


def _existe_comando_seed_data(codigo_dir: Path) -> bool:
    return any(
        path.name == "seed_data.py"
        and "management" in path.parts
        and "commands" in path.parts
        for path in codigo_dir.rglob("seed_data.py")
    )


def _renderizar_template(
    *,
    python_path: Path,
    codigo_dir: Path,
    template: str,
    timeout_s: int,
) -> ResultadoTemplate:
    codigo = (
        "from django.template.loader import get_template\n"
        f"get_template({template!r})\n"
    )
    resultado = _ejecutar_manage(
        nombre=f"template:{template}",
        python_path=python_path,
        codigo_dir=codigo_dir,
        args=["shell", "-c", codigo],
        timeout_s=timeout_s,
    )
    return ResultadoTemplate(
        template=template,
        ejecutado=resultado.ejecutado,
        ok=resultado.ok,
        error=resultado.stderr_resumen or resultado.stdout_resumen,
        motivo_no_ejecutado=resultado.motivo_no_ejecutado,
    )


def _validar_runserver_y_rutas(
    *,
    python_path: Path,
    codigo_dir: Path,
    timeout_s: int,
    rutas: Iterable[str],
) -> tuple[ResultadoComando, list[ResultadoRuta]]:
    port = _puerto_libre()
    comando = [
        str(python_path),
        "manage.py",
        "runserver",
        f"127.0.0.1:{port}",
        "--noreload",
    ]
    proc: subprocess.Popen[str] | None = None
    try:
        proc = subprocess.Popen(
            comando,
            cwd=codigo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        base_url = f"http://127.0.0.1:{port}"
        arrancado = _esperar_servidor(base_url, timeout_s=timeout_s)
        if not arrancado:
            stdout, stderr = _terminar_proceso(proc)
            runserver = ResultadoComando(
                nombre="runserver",
                comando=comando,
                ejecutado=True,
                ok=False,
                returncode=proc.returncode,
                stdout_resumen=_resumir_salida(stdout),
                stderr_resumen=_resumir_salida(stderr or "El servidor no respondio a tiempo."),
                timeout_s=timeout_s,
                timeout=True,
            )
            return runserver, [
                _ruta_no_ejecutada(path, "runserver no arranco correctamente")
                for path in rutas
            ]

        resultados_rutas = [
            _consultar_ruta(base_url, path)
            for path in rutas
        ]
        stdout, stderr = _terminar_proceso(proc)
        detalle_servidor = _resumir_salida(stderr or stdout)
        for resultado in resultados_rutas:
            if (
                resultado.status_code is not None
                and resultado.status_code >= 500
                and detalle_servidor
            ):
                resultado.error = detalle_servidor
        runserver = ResultadoComando(
            nombre="runserver",
            comando=comando,
            ejecutado=True,
            ok=True,
            returncode=0,
            stdout_resumen=_resumir_salida(stdout),
            stderr_resumen=_resumir_salida(stderr),
            timeout_s=timeout_s,
            timeout=False,
        )
        return runserver, resultados_rutas
    except Exception as e:
        if proc is not None:
            stdout, stderr = _terminar_proceso(proc)
        else:
            stdout, stderr = "", ""
        runserver = ResultadoComando(
            nombre="runserver",
            comando=comando,
            ejecutado=True,
            ok=False,
            returncode=None,
            stdout_resumen=_resumir_salida(stdout),
            stderr_resumen=_resumir_salida(stderr or f"{type(e).__name__}: {e}"),
            timeout_s=timeout_s,
            timeout=False,
        )
        return runserver, [
            _ruta_no_ejecutada(path, "error ejecutando runserver")
            for path in rutas
        ]


def _puerto_libre() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _esperar_servidor(base_url: str, *, timeout_s: int) -> bool:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            _abrir_url(base_url + "/")
            return True
        except Exception:
            time.sleep(0.5)
    return False


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        return None


def _abrir_url(url: str) -> tuple[int, str]:
    opener = urllib.request.build_opener(_NoRedirectHandler)
    try:
        with opener.open(url, timeout=5) as response:
            return int(response.status), response.geturl()
    except urllib.error.HTTPError as e:
        return int(e.code), e.headers.get("Location", "")


def _consultar_ruta(base_url: str, path: str) -> ResultadoRuta:
    try:
        status_code, final_url = _abrir_url(base_url + path)
        return ResultadoRuta(
            path=path,
            ejecutado=True,
            ok=status_code < 500 and status_code != 404,
            status_code=status_code,
            final_url=final_url,
        )
    except Exception as e:
        return ResultadoRuta(
            path=path,
            ejecutado=True,
            ok=False,
            error=f"{type(e).__name__}: {e}",
        )


def _ruta_no_ejecutada(path: str, motivo: str) -> ResultadoRuta:
    return ResultadoRuta(
        path=path,
        ejecutado=False,
        ok=False,
        motivo_no_ejecutado=motivo,
    )


def _template_no_ejecutada(template: str, motivo: str) -> ResultadoTemplate:
    return ResultadoTemplate(
        template=template,
        ejecutado=False,
        ok=False,
        motivo_no_ejecutado=motivo,
    )


def _terminar_proceso(proc: subprocess.Popen[str]) -> tuple[str, str]:
    if proc.poll() is None:
        proc.terminate()
        try:
            return proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            return proc.communicate(timeout=5)
    return proc.communicate(timeout=5)


def _construir_incidencias(
    *,
    check: ResultadoComando,
    migraciones: ResultadoMigraciones,
    migrate: ResultadoComando,
    seed_data: ResultadoComando,
    runserver: ResultadoComando,
    rutas: list[ResultadoRuta],
    templates: list[ResultadoTemplate],
) -> list[str]:
    incidencias: list[str] = []
    if not check.ok:
        incidencias.append("manage.py check no fue correcto.")
    if not migraciones.ok:
        incidencias.append(
            "Faltan migraciones propias en apps con modelos: "
            + ", ".join(migraciones.apps_sin_migraciones)
        )
    if not migrate.ok:
        incidencias.append("manage.py migrate --noinput no fue correcto.")
    if not seed_data.ok:
        incidencias.append("seed_data no se ejecuto correctamente o no existe.")
    if not runserver.ok:
        incidencias.append("runserver no arranco correctamente.")
    for ruta in rutas:
        if not ruta.ok:
            detalle = (
                f"status {ruta.status_code}"
                if ruta.status_code is not None
                else ruta.error or ruta.motivo_no_ejecutado
            )
            incidencias.append(f"Ruta {ruta.path} no supero smoke test: {detalle}.")
    for template in templates:
        if not template.ok:
            detalle = template.error or template.motivo_no_ejecutado
            incidencias.append(f"Template {template.template} no compila: {detalle}.")
    return incidencias


def _factores_bloqueantes(
    *,
    check: ResultadoComando,
    migrate: ResultadoComando,
    runserver: ResultadoComando,
) -> list[str]:
    factores: list[str] = []
    for resultado in (check, migrate, runserver):
        if not resultado.ejecutado and resultado.motivo_no_ejecutado:
            factores.append(resultado.motivo_no_ejecutado)
    if check.ejecutado and not check.ok:
        factores.append("El proyecto no supera manage.py check.")
    if runserver.ejecutado and not runserver.ok:
        factores.append("El servidor Django no arranca para smoke tests.")
    return factores


def _resumen_checks(
    *,
    check: ResultadoComando,
    migraciones: ResultadoMigraciones,
    migrate: ResultadoComando,
    seed_data: ResultadoComando,
    runserver: ResultadoComando,
    rutas: list[ResultadoRuta],
    templates: list[ResultadoTemplate],
) -> tuple[list[str], dict[str, str]]:
    ejecutados: list[str] = []
    no_ejecutados: dict[str, str] = {}

    for resultado in (check, migrate, seed_data, runserver):
        if resultado.ejecutado:
            ejecutados.append(resultado.nombre)
        else:
            no_ejecutados[resultado.nombre] = resultado.motivo_no_ejecutado

    ejecutados.append("migraciones")
    if not migraciones.ok and not migraciones.apps_con_modelos:
        no_ejecutados["migraciones"] = "No se detectaron apps con modelos."

    for ruta in rutas:
        check_id = f"ruta:{ruta.path}"
        if ruta.ejecutado:
            ejecutados.append(check_id)
        else:
            no_ejecutados[check_id] = ruta.motivo_no_ejecutado

    for template in templates:
        check_id = f"template:{template.template}"
        if template.ejecutado:
            ejecutados.append(check_id)
        else:
            no_ejecutados[check_id] = template.motivo_no_ejecutado

    return ejecutados, no_ejecutados


def _clasificar(
    *,
    check: ResultadoComando,
    migrate: ResultadoComando,
    runserver: ResultadoComando,
    incidencias: list[str],
    factores_bloqueantes: list[str],
) -> str:
    if not check.ejecutado or not migrate.ejecutado or not runserver.ejecutado:
        return "fallo_entorno_validacion"
    if factores_bloqueantes:
        return "bloqueado_arranque"
    if incidencias:
        return "parcial_con_incidencias"
    return "apto_para_revision_funcional"
