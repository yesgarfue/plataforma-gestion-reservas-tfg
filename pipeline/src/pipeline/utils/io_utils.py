# src/pipeline/utils/io_utils.py
"""
Utilidades de entrada/salida agnósticas del dominio.

Portado y adaptado desde el Run 01 (src/io_utils.py), con los siguientes
cambios respecto al legacy:

  - Se eliminan `assert_approved` y `classify_artifact`: asumían un campo
    `estado: "Approved"` dentro del JSON del artefacto, patrón propio del
    sistema de congelación del Run 01. En el spec nuevo (Bloque 5) la
    aprobación vive en `gate_humano.md` fuera del artefacto, así que esas
    funciones ya no aplican aquí.
  - Se añaden helpers menores (`ensure_dir`, `now_iso_madrid`, `sha256_dict`)
    que se usan en renderers, manifest y frontmatter de artefactos MD.

Todo lo demás se conserva tal cual el legacy: hashes SHA-256, escritura
idempotente de texto y JSON, lectura con validación, limpieza de cercas
markdown del output del LLM, y guardado de intentos fallidos para auditoría.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple
from zoneinfo import ZoneInfo


# ---------------------------------------------------------------------------
# Hashes
# ---------------------------------------------------------------------------

def sha256_text(text: str) -> str:
    """Hash SHA-256 de una cadena de texto, codificada en UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    """Hash SHA-256 del contenido de un archivo. Devuelve '' si no existe."""
    if not path.exists():
        return ""
    return sha256_text(path.read_text(encoding="utf-8"))


def sha256_dict(obj: Dict[str, Any]) -> str:
    """
    Hash SHA-256 de un diccionario, serializado de forma canónica
    (claves ordenadas, sin espacios superfluos) para que el hash sea estable
    entre ejecuciones. Útil para hashear configs parseadas desde YAML.
    """
    canonical = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return sha256_text(canonical)


# ---------------------------------------------------------------------------
# Filesystem
# ---------------------------------------------------------------------------

def ensure_dir(path: Path) -> Path:
    """Crea `path` como directorio si no existe. Devuelve la misma ruta."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_text(path: Path, text: str) -> None:
    """
    Escribe `text` en `path`, creando directorios intermedios si hace falta.
    Normaliza el final con un único '\\n' para que los diffs entre runs
    sean limpios.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text((text or "").rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, obj: Any) -> None:
    """
    Escribe `obj` como JSON UTF-8 indentado (2 espacios), creando directorios
    intermedios si hace falta. `ensure_ascii=False` para preservar acentos.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    """Lee texto. Falla si no existe o está vacío (evita bugs silenciosos)."""
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"El archivo está vacío: {path}")
    return content


def load_json_or_fail(path: Path) -> Dict[str, Any]:
    """Carga un JSON y exige que sea un objeto (dict). Falla si no."""
    obj = json.loads(read_text(path))
    if not isinstance(obj, dict):
        raise ValueError(f"JSON inválido: se esperaba un objeto en {path}")
    return obj


def load_json_safe(path: Path) -> Optional[Dict[str, Any]]:
    """
    Versión tolerante: devuelve `dict` si todo va bien, `None` si el
    archivo no existe, está vacío, es JSON inválido o no es un objeto.
    No lanza excepciones. Útil para inspeccionar estado sin romper flujo.
    """
    if not path.exists():
        return None

    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return None

    try:
        obj = json.loads(raw)
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Limpieza de respuestas del LLM
# ---------------------------------------------------------------------------

def strip_markdown_fences(text: str) -> str:
    """
    Limpia respuestas típicas del LLM cuando se le pide JSON:
      - ```json ... ```
      - ``` ... ```
      - texto con basura antes/después del JSON: recorta al primer '{'
        y al último '}'.

    No garantiza que el resultado sea JSON válido; solo lo prepara para
    que `json.loads` tenga más probabilidades de éxito.
    """
    if text is None:
        return ""

    s = text.strip()

    # Quitar cercas ```json o ``` al inicio/fin
    if s.startswith("```"):
        lines = s.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        s = "\n".join(lines).strip()

    # Recortar al primer '{' y último '}' por si quedan preámbulos
    first = s.find("{")
    last = s.rfind("}")
    if first != -1 and last != -1 and last > first:
        s = s[first:last + 1].strip()

    return s


def parse_and_validate_json_text(
    *,
    raw_content: str,
    validator: Callable[[Dict[str, Any]], Any],
) -> Any:
    """
    Operación única: limpiar → parsear → validar.

    Los reintentos reales (volver a llamar al LLM) viven en el runner o crew,
    que es quien tiene contexto para decidir cuántas veces reintentar.
    """
    clean = strip_markdown_fences(raw_content)
    obj = json.loads(clean)
    if not isinstance(obj, dict):
        raise ValueError("Se esperaba un objeto JSON en la salida del modelo.")
    return validator(obj)


# ---------------------------------------------------------------------------
# Auditoría de intentos
# ---------------------------------------------------------------------------

def save_attempt_artifacts(
    *,
    attempts_dir: Path,
    base_name: str,
    attempt: int,
    raw: str,
    error: Exception | None = None,
) -> Tuple[Path, Path | None]:
    """
    Guarda el output crudo del LLM (y el error, si lo hubo) en `attempts_dir`.

    Archivos producidos:
      - <base_name>.raw_attempt_<n>.txt        (siempre)
      - <base_name>.error_attempt_<n>.txt      (solo si `error` no es None)

    Se llama en cada intento fallido de generación, antes de reintentar.
    Los archivos resultantes son evidencia del Run y se preservan.
    """
    raw_path = attempts_dir / f"{base_name}.raw_attempt_{attempt}.txt"
    write_text(raw_path, raw)

    err_path: Path | None = None
    if error is not None:
        err_path = attempts_dir / f"{base_name}.error_attempt_{attempt}.txt"
        write_text(err_path, f"{type(error).__name__}: {error}")

    return raw_path, err_path


# ---------------------------------------------------------------------------
# Render de MD desde JSON canónico
# ---------------------------------------------------------------------------

def render_md_from_json(
    *,
    json_path: Path,
    md_path: Path,
    validator: Callable[[Dict[str, Any]], Any],
    renderer: Callable[[Any], str],
) -> Dict[str, Any]:
    """
    Flujo idempotente para regenerar el MD desde el JSON canónico:
      1. Lee `json_path`.
      2. Valida + normaliza con `validator`.
      3. Reescribe el JSON canónico normalizado.
      4. Genera `md_path` llamando a `renderer(obj_norm)`.
      5. Devuelve el objeto normalizado.

    Útil para el patrón del spec (Bloque 3): el JSON es fuente de verdad;
    el MD se regenera siempre desde él, nunca al revés.
    """
    obj = load_json_safe(json_path)
    if obj is None:
        raise ValueError(f"JSON inexistente/vacío/corrupto: {json_path}")

    obj_norm = validator(obj)
    write_json(json_path, obj_norm)
    write_text(md_path, renderer(obj_norm))
    return obj_norm


# ---------------------------------------------------------------------------
# Timestamps
# ---------------------------------------------------------------------------

def now_iso_madrid() -> str:
    """
    Timestamp ISO 8601 con zona Europe/Madrid (requisito del brief: locale
    España). Se usa en el frontmatter YAML de los artefactos MD y en el
    manifest del Run. Ejemplo: '2026-04-25T10:32:18+02:00'.
    """
    return datetime.now(ZoneInfo("Europe/Madrid")).isoformat(timespec="seconds")