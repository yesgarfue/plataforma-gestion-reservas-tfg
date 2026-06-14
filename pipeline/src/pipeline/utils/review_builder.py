# src/pipeline/utils/review_builder.py
"""
Review automático determinista por sprint.

La heurística no pretende demostrar calidad funcional. Su objetivo es dejar
evidencia repetible sobre si cada historia de usuario pedida deja señales en
los paths o contenidos entregados.
"""

from __future__ import annotations

import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import re
from pathlib import Path
from typing import Iterable, Sequence

from pipeline.utils.django_runner import (
    _detectar_commands_apps_no_instaladas,
    _resolver_python_django_check,
    _resumir_salida,
)
from pipeline.validation.schemas import (
    ArranqueResult,
    BacklogSprint,
    EstadoCumplimiento,
    ResultadoReviewRuta,
    ResultadoReviewTemplate,
    ReviewSprint,
)


PALABRAS_VACIAS = {
    "a",
    "al",
    "como",
    "con",
    "de",
    "del",
    "el",
    "en",
    "es",
    "la",
    "las",
    "lo",
    "los",
    "para",
    "por",
    "que",
    "quiero",
    "se",
    "un",
    "una",
    "y",
}

RUTAS_CANONICAS = [
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


def listar_archivos_codigo(codigo_dir: Path) -> list[Path]:
    """
    Lista archivos dentro de `codigo_dir`, ignorando cachés y artefactos
    volátiles. Devuelve rutas absolutas ordenadas para lectura posterior.
    """
    if not codigo_dir.exists():
        return []

    ignorar_partes = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        "db.sqlite3",
    }
    archivos: list[Path] = []
    for path in codigo_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignorar_partes for part in path.parts):
            continue
        archivos.append(path)
    return sorted(archivos)


def _leer_archivos_para_review(
    *,
    codigo_dir: Path,
    archivos: Sequence[Path],
    max_chars_por_archivo: int = 12000,
) -> tuple[list[str], str]:
    partes: list[str] = []
    paths_relativos: list[str] = []

    for path in archivos:
        rel = path.relative_to(codigo_dir).as_posix()
        paths_relativos.append(rel)
        try:
            contenido = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            contenido = ""
        partes.append(f"\n--- FILE: {rel} ---\n{contenido[:max_chars_por_archivo]}")

    return paths_relativos, "\n".join(partes).lower()


def _tokens_relevantes(textos: Iterable[str]) -> set[str]:
    tokens: set[str] = set()
    for texto in textos:
        for token in re.findall(r"[a-záéíóúüñ0-9_]{4,}", texto.lower()):
            if token not in PALABRAS_VACIAS:
                tokens.add(token)
    return tokens


def _clasificar_historia(
    *,
    titulo: str,
    descripcion: str,
    criterios: Sequence[str],
    corpus: str,
) -> EstadoCumplimiento:
    tokens_titulo = _tokens_relevantes([titulo])
    tokens_criterios = _tokens_relevantes(criterios)
    tokens_descripcion = _tokens_relevantes([descripcion])

    coincidencias_titulo = sum(1 for token in tokens_titulo if token in corpus)
    coincidencias_criterios = sum(1 for token in tokens_criterios if token in corpus)
    coincidencias_descripcion = sum(1 for token in tokens_descripcion if token in corpus)

    # Señal fuerte: aparece algo del título y algo de criterios/descripcion.
    if coincidencias_titulo >= 1 and (coincidencias_criterios >= 1 or coincidencias_descripcion >= 2):
        return "ok"

    # Señal media: varias coincidencias aunque no crucen título+criterios.
    if coincidencias_titulo + coincidencias_criterios + coincidencias_descripcion >= 2:
        return "parcial"

    # Señal mínima: una única palabra relevante aparece en paths/contenido.
    if coincidencias_titulo + coincidencias_criterios + coincidencias_descripcion == 1:
        return "parcial"

    return "ausente"


def construir_review_sprint(
    *,
    sprint_backlog: BacklogSprint,
    codigo_dir: Path,
    arranque: ArranqueResult,
) -> ReviewSprint:
    """
    Construye un `ReviewSprint` factual a partir del backlog y el código.
    """
    archivos = listar_archivos_codigo(codigo_dir)
    paths_relativos, corpus = _leer_archivos_para_review(
        codigo_dir=codigo_dir,
        archivos=archivos,
    )

    cumplimiento: dict[str, EstadoCumplimiento] = {}
    for historia in sprint_backlog.historias:
        cumplimiento[historia.id] = _clasificar_historia(
            titulo=historia.titulo,
            descripcion=historia.descripcion,
            criterios=historia.criterios_aceptacion,
            corpus=corpus,
        )

    rutas, templates, incidencias_ejecutables = _review_ejecutable_incremental(
        codigo_dir=codigo_dir,
        corpus=corpus,
        timeout_s=arranque.timeout_s,
    )
    incidencias = list(incidencias_ejecutables)
    if not arranque.ok:
        incidencias.insert(0, "manage.py check no fue correcto.")

    return ReviewSprint(
        id_ejecucion=sprint_backlog.id_ejecucion,
        sprint=sprint_backlog.numero_sprint,
        backlog_items_pedidos=[historia.id for historia in sprint_backlog.historias],
        archivos_entregados=paths_relativos,
        cumplimiento=cumplimiento,
        arranque=arranque,
        rutas=rutas,
        templates=templates,
        incidencias=incidencias,
    )


def _review_ejecutable_incremental(
    *,
    codigo_dir: Path,
    corpus: str,
    timeout_s: int,
) -> tuple[list[ResultadoReviewRuta], list[ResultadoReviewTemplate], list[str]]:
    """
    Ejecuta checks pragmaticos sobre una copia temporal del codigo.

    No bloquea el sprint ni intenta ser una suite funcional completa. Solo
    registra fallos ejecutables que el siguiente sprint puede corregir.
    """
    incidencias: list[str] = []
    rutas: list[ResultadoReviewRuta] = []
    templates: list[ResultadoReviewTemplate] = []

    python_path, origen_python = _resolver_python_django_check()
    if python_path is None:
        incidencias.append(f"No se ejecutan checks incrementales: {origen_python}")
        return rutas, templates, incidencias

    if not (codigo_dir / "manage.py").exists():
        incidencias.append("No se ejecutan checks incrementales: no existe manage.py.")
        return rutas, templates, incidencias

    try:
        with tempfile.TemporaryDirectory(prefix="hundidos_review_") as tmp:
            copia_dir = Path(tmp) / "codigo"
            shutil.copytree(codigo_dir, copia_dir)

            migrate = _ejecutar_manage(
                python_path=python_path,
                codigo_dir=copia_dir,
                args=["migrate", "--noinput"],
                timeout_s=timeout_s,
            )
            if not migrate.ok:
                incidencias.append(
                    "migrate --noinput no fue correcto en review incremental: "
                    f"{migrate.detalle}"
                )
                return rutas, templates, incidencias

            if _existe_seed_data(copia_dir):
                seed = _ejecutar_manage(
                    python_path=python_path,
                    codigo_dir=copia_dir,
                    args=["seed_data"],
                    timeout_s=timeout_s,
                )
                if not seed.ok:
                    incidencias.append(
                        "seed_data no fue correcto en review incremental: "
                        f"{seed.detalle}"
                    )

            templates = _compilar_templates(
                python_path=python_path,
                codigo_dir=copia_dir,
                timeout_s=timeout_s,
            )
            for template in templates:
                if not template.ok:
                    incidencias.append(
                        f"Template {template.template} no compila: {template.error}."
                    )

            rutas = _validar_rutas_presentes(
                python_path=python_path,
                codigo_dir=copia_dir,
                corpus=corpus,
                timeout_s=min(timeout_s, 20),
            )
            for ruta in rutas:
                if not ruta.ok:
                    detalle = ruta.detalle or ruta.error or ruta.motivo_no_ejecutado
                    incidencias.append(
                        f"Ruta {ruta.path} no responde correctamente: {detalle}."
                    )
    except Exception as e:
        incidencias.append(
            f"Review incremental no pudo completarse: {type(e).__name__}: {e}"
        )

    incidencias.extend(_incidencias_navegacion_estatica(codigo_dir))
    # Check estático: apps con management/commands/ no incluidas en INSTALLED_APPS.
    # Se ejecuta sobre el directorio original (no la copia) porque es análisis de archivos,
    # no ejecución Django. Detecta la incidencia en el sprint que la introduce.
    incidencias.extend(_detectar_commands_apps_no_instaladas(codigo_dir))
    return rutas, templates, incidencias


def _existe_seed_data(codigo_dir: Path) -> bool:
    return any(
        path.name == "seed_data.py"
        and "management" in path.parts
        and "commands" in path.parts
        for path in codigo_dir.rglob("seed_data.py")
    )


def _ejecutar_manage(
    *,
    python_path: Path,
    codigo_dir: Path,
    args: list[str],
    timeout_s: int,
) -> ResultadoReviewRuta:
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
        detalle = _resumir_salida(completed.stderr or completed.stdout)
        return ResultadoReviewRuta(
            path=" ".join(["manage.py", *args]),
            ejecutado=True,
            ok=completed.returncode == 0,
            status_code=completed.returncode,
            detalle=detalle,
        )
    except subprocess.TimeoutExpired as e:
        stderr = e.stderr if isinstance(e.stderr, str) else ""
        return ResultadoReviewRuta(
            path=" ".join(["manage.py", *args]),
            ejecutado=True,
            ok=False,
            error=_resumir_salida(stderr or "Timeout."),
        )
    except Exception as e:
        return ResultadoReviewRuta(
            path=" ".join(["manage.py", *args]),
            ejecutado=True,
            ok=False,
            error=f"{type(e).__name__}: {e}",
        )


def _compilar_templates(
    *,
    python_path: Path,
    codigo_dir: Path,
    timeout_s: int,
) -> list[ResultadoReviewTemplate]:
    templates_root = codigo_dir / "templates"
    if not templates_root.exists():
        return []

    resultados: list[ResultadoReviewTemplate] = []
    for template_path in sorted(templates_root.rglob("*.html")):
        rel = template_path.relative_to(templates_root).as_posix()
        codigo = (
            "from django.template.loader import get_template\n"
            f"get_template({rel!r})\n"
        )
        resultado = _ejecutar_shell(
            python_path=python_path,
            codigo_dir=codigo_dir,
            codigo=codigo,
            timeout_s=timeout_s,
        )
        resultados.append(
            ResultadoReviewTemplate(
                template=rel,
                ejecutado=True,
                ok=resultado.ok,
                error=resultado.error or resultado.detalle,
            )
        )
    return resultados


def _ejecutar_shell(
    *,
    python_path: Path,
    codigo_dir: Path,
    codigo: str,
    timeout_s: int,
) -> ResultadoReviewRuta:
    return _ejecutar_manage(
        python_path=python_path,
        codigo_dir=codigo_dir,
        args=["shell", "-c", codigo],
        timeout_s=timeout_s,
    )


def _rutas_presentes(corpus: str) -> list[str]:
    rutas: list[str] = []
    for ruta in RUTAS_CANONICAS:
        if ruta == "/" or ruta.strip("/") in corpus or ruta in corpus:
            rutas.append(ruta)
    return rutas


def _validar_rutas_presentes(
    *,
    python_path: Path,
    codigo_dir: Path,
    corpus: str,
    timeout_s: int,
) -> list[ResultadoReviewRuta]:
    rutas = _rutas_presentes(corpus)
    if not rutas:
        return []

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
        if not _esperar_servidor(base_url, timeout_s=timeout_s):
            stdout, stderr = _terminar_proceso(proc)
            detalle = _resumir_salida(stderr or stdout or "runserver no respondio.")
            return [
                ResultadoReviewRuta(
                    path=ruta,
                    ejecutado=False,
                    ok=False,
                    motivo_no_ejecutado=detalle,
                )
                for ruta in rutas
            ]

        resultados = [_consultar_ruta(base_url, ruta) for ruta in rutas]
        stdout, stderr = _terminar_proceso(proc)
        servidor_detalle = _resumir_salida(stderr or stdout)
        for resultado in resultados:
            if resultado.status_code and resultado.status_code >= 500 and servidor_detalle:
                resultado.detalle = servidor_detalle
        return resultados
    except Exception as e:
        if proc is not None:
            _terminar_proceso(proc)
        return [
            ResultadoReviewRuta(
                path=ruta,
                ejecutado=False,
                ok=False,
                motivo_no_ejecutado=f"{type(e).__name__}: {e}",
            )
            for ruta in rutas
        ]


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


def _consultar_ruta(base_url: str, path: str) -> ResultadoReviewRuta:
    try:
        status_code, final_url = _abrir_url(base_url + path)
        return ResultadoReviewRuta(
            path=path,
            ejecutado=True,
            ok=status_code < 500 and status_code != 404,
            status_code=status_code,
            final_url=final_url,
            detalle=final_url,
        )
    except Exception as e:
        return ResultadoReviewRuta(
            path=path,
            ejecutado=True,
            ok=False,
            error=f"{type(e).__name__}: {e}",
        )


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


def _terminar_proceso(proc: subprocess.Popen[str]) -> tuple[str, str]:
    if proc.poll() is None:
        proc.terminate()
        try:
            return proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            return proc.communicate(timeout=5)
    return proc.communicate(timeout=5)


def _incidencias_navegacion_estatica(codigo_dir: Path) -> list[str]:
    incidencias: list[str] = []
    base_html = codigo_dir / "templates" / "base.html"
    accounts_views = codigo_dir / "accounts" / "views.py"
    if not base_html.exists() or not accounts_views.exists():
        return incidencias
    base = base_html.read_text(encoding="utf-8", errors="replace")
    views = accounts_views.read_text(encoding="utf-8", errors="replace")
    logout_view = re.search(
        r"class\s+LogoutView\b(?P<body>.*?)(?:\nclass\s+\w+|\Z)",
        views,
        flags=re.S,
    )
    logout_body = logout_view.group("body") if logout_view else ""
    enlace_logout_get = re.search(
        r"<a\b[^>]*href=[\"'][^\"']*logout",
        base,
        flags=re.I,
    )
    if (
        enlace_logout_get
        and logout_body
        and "def post" in logout_body
        and "def get" not in logout_body
    ):
        incidencias.append(
            "La navegacion visible enlaza logout por GET, pero LogoutView "
            "solo define POST."
        )
    return incidencias
