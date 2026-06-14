# src/pipeline/utils/django_runner.py
"""
Ejecución determinista de comprobaciones Django post-sprint.

Este módulo no interpreta si el producto es bueno o malo: solo ejecuta
comandos acotados por timeout y devuelve un `ArranqueResult` factual.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from pipeline.validation.schemas import ArranqueResult


MAX_RESUMEN_CHARS = 4000
DJANGO_CHECK_ENV_VAR = "DJANGO_CHECK_PYTHON"
DEFAULT_DJANGO_CHECK_VENV = ".venv_Test"


def _resumir_salida(texto: str, max_chars: int = MAX_RESUMEN_CHARS) -> str:
    """
    Recorta stdout/stderr para que el review no crezca sin límite.

    Conserva tanto el inicio como el final del texto para que los tracebacks
    de Django muestren tanto la importación raíz como la causa real (última
    línea del traceback, donde suele aparecer el error concreto).
    """
    texto = (texto or "").strip()
    if len(texto) <= max_chars:
        return texto
    mitad = max_chars // 2
    inicio = texto[:mitad].rstrip()
    final = texto[-mitad:].lstrip()
    return f"{inicio}\n...[salida truncada]...\n{final}"

def _project_root() -> Path:
    """Localiza la raiz del proyecto para resolver .venv_Test."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return Path.cwd()


def _resolver_python_django_check() -> tuple[Path | None, str]:
    """
    Devuelve el Python usado para validar codigo Django generado.

    La validacion usa un entorno fijo separado del entorno de CrewAI para no
    mezclar dependencias del pipeline con dependencias del producto generado.
    """
    configurado = os.getenv(DJANGO_CHECK_ENV_VAR, "").strip().strip('"')
    if configurado:
        python_path = Path(configurado)
        if python_path.exists():
            return python_path, f"{DJANGO_CHECK_ENV_VAR}={python_path}"
        return None, (
            f"{DJANGO_CHECK_ENV_VAR} apunta a un interprete inexistente: "
            f"{python_path}"
        )

    root = _project_root()
    candidatos = [
        root / DEFAULT_DJANGO_CHECK_VENV / "Scripts" / "python.exe",
        root / DEFAULT_DJANGO_CHECK_VENV / "bin" / "python",
    ]
    for python_path in candidatos:
        if python_path.exists():
            return python_path, f"entorno fijo {DEFAULT_DJANGO_CHECK_VENV}: {python_path}"

    return None, (
        "No existe un interprete Django de validacion. Crea "
        f"{root / DEFAULT_DJANGO_CHECK_VENV} o define {DJANGO_CHECK_ENV_VAR}."
    )


def ejecutar_manage_check(codigo_dir: Path, timeout_s: int) -> ArranqueResult:
    """
    Ejecuta `python manage.py check` dentro de `codigo_dir`.

    Usa un entorno fijo de validacion Django separado del entorno que ejecuta
    el pipeline. Si el entorno no existe o el proyecto no arranca, eso queda
    reflejado en stderr y `ok=False`; no se lanza excepcion porque el Run debe
    continuar o abortar segun la fase que consume este resultado.
    """
    manage_py = codigo_dir / "manage.py"
    if not codigo_dir.exists():
        return ArranqueResult(
            ok=False,
            returncode=-1,
            stdout_resumen="",
            stderr_resumen=f"No existe la carpeta de código: {codigo_dir}",
            timeout_s=timeout_s,
            timeout=False,
        )
    if not manage_py.exists():
        return ArranqueResult(
            ok=False,
            returncode=-1,
            stdout_resumen="",
            stderr_resumen=f"No existe manage.py en: {codigo_dir}",
            timeout_s=timeout_s,
            timeout=False,
        )

    python_check, origen_python = _resolver_python_django_check()
    if python_check is None:
        return ArranqueResult(
            ok=False,
            returncode=-1,
            stdout_resumen="",
            stderr_resumen=origen_python,
            timeout_s=timeout_s,
            timeout=False,
        )

    try:
        version_check = subprocess.run(
            [str(python_check), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if version_check.returncode != 0:
            return ArranqueResult(
                ok=False,
                returncode=version_check.returncode,
                stdout_resumen=_resumir_salida(version_check.stdout),
                stderr_resumen=_resumir_salida(
                    "El interprete Django de validacion existe, pero no puede "
                    f"ejecutarse ({origen_python}). "
                    f"{version_check.stderr}"
                ),
                timeout_s=timeout_s,
                timeout=False,
            )

        completed = subprocess.run(
            [str(python_check), "manage.py", "check"],
            cwd=codigo_dir,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        return ArranqueResult(
            ok=completed.returncode == 0,
            returncode=completed.returncode,
            stdout_resumen=_resumir_salida(completed.stdout),
            stderr_resumen=_resumir_salida(completed.stderr),
            timeout_s=timeout_s,
            timeout=False,
        )
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout.decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = e.stderr.decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        return ArranqueResult(
            ok=False,
            returncode=-1,
            stdout_resumen=_resumir_salida(stdout),
            stderr_resumen=_resumir_salida(stderr or "Timeout ejecutando manage.py check."),
            timeout_s=timeout_s,
            timeout=True,
        )
    except Exception as e:
        return ArranqueResult(
            ok=False,
            returncode=-1,
            stdout_resumen="",
            stderr_resumen=f"{type(e).__name__}: {e}",
            timeout_s=timeout_s,
            timeout=False,
        )


# ---------------------------------------------------------------------------
# Análisis estático de configuración Django (sin ejecutar el proyecto)
# ---------------------------------------------------------------------------

def _buscar_settings_py(codigo_dir: Path) -> Path | None:
    """Localiza settings.py dentro del código generado, ignorando entornos virtuales."""
    for candidate in sorted(codigo_dir.rglob("settings.py")):
        parts = candidate.parts
        if ".venv" in parts or "__pycache__" in parts:
            continue
        return candidate
    return None


def _extraer_installed_apps_estatico(settings_content: str) -> set[str] | None:
    """
    Extrae INSTALLED_APPS de settings.py mediante análisis de texto estático.

    Devuelve None si no puede parsear la lista con suficiente confianza
    (p.ej. si usa asignación dinámica). No ejecuta el settings; solo lee texto.
    """
    match = re.search(
        r"INSTALLED_APPS\s*=\s*\[([^\]]*)\]",
        settings_content,
        re.DOTALL,
    )
    if not match:
        return None
    bloque = match.group(1)
    return set(re.findall(r"['\"]([^'\"]+)['\"]", bloque))


def _detectar_commands_apps_no_instaladas(codigo_dir: Path) -> list[str]:
    """
    Detecta apps con management/commands/*.py cuya app no está en INSTALLED_APPS.

    Es un check estático: lee archivos, no ejecuta Django. Si no puede parsear
    INSTALLED_APPS de forma fiable, devuelve lista vacía para evitar falsos
    positivos. Django solo descubre comandos de gestión en apps instaladas;
    si una app con comandos no está en INSTALLED_APPS, manage.py no la encontrará.
    """
    apps_con_commands: set[str] = set()
    for cmd_py in codigo_dir.rglob("management/commands/*.py"):
        if cmd_py.name == "__init__.py":
            continue
        # Estructura: codigo_dir/appname/management/commands/cmd.py
        app_dir = cmd_py.parent.parent.parent
        apps_con_commands.add(app_dir.name)

    if not apps_con_commands:
        return []

    settings_py = _buscar_settings_py(codigo_dir)
    if settings_py is None:
        return []

    try:
        settings_content = settings_py.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    installed_apps = _extraer_installed_apps_estatico(settings_content)
    if installed_apps is None:
        return []

    incidencias: list[str] = []
    for app in sorted(apps_con_commands):
        en_installed = any(
            app == ia or ia.startswith(f"{app}.") or ia.endswith(f".{app}")
            for ia in installed_apps
        )
        if not en_installed:
            incidencias.append(
                f"La app '{app}' tiene management/commands/ pero no está en "
                f"INSTALLED_APPS: sus comandos de gestión no serán descubiertos "
                f"por Django."
            )
    return incidencias
