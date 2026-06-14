"""Manifest determinista de ejecucion del pipeline."""

from __future__ import annotations

import importlib.metadata
import subprocess
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from pipeline.utils.io_utils import load_json_safe, now_iso_madrid, sha256_file


def construir_manifest(
    *,
    state: Any,
    project_root: Path,
    pipeline_specs_path: Path,
    pipeline_config_path: Path,
) -> dict[str, Any]:
    """Construye el manifest completo del run sin modificar el producto."""
    paths = state.paths
    if paths is None:
        raise ValueError("No hay paths en state; no se puede construir manifest.")

    config = _leer_yaml(pipeline_config_path)
    run_summary = load_json_safe(paths.root / "run_summary.json") or {}
    validacion_final = None
    if state.validacion_final is not None:
        validacion_final = _resumen_validacion_final(state.validacion_final)

    manifest = {
        "schema_version": "manifest_v1",
        "generated_at": now_iso_madrid(),
        "run_id": state.run_id,
        "resultado_final": state.resultado_final,
        "run_dir": str(paths.root),
        "protocolo": {
            "pipeline_specs_path": str(pipeline_specs_path),
            "pipeline_specs_hash": state.hashes.pipeline_specs,
            "brief_hash": state.hashes.brief,
            "pipeline_config_hash": state.hashes.pipeline_config,
        },
        "versiones": {
            "git_commit": _git_commit(project_root),
            "python_pipeline": _python_version(),
            "crewai": _package_version("crewai"),
            "pydantic": _package_version("pydantic"),
            "django_validacion": _django_validacion_version(project_root),
        },
        "modelos": _extraer_modelos(config),
        "fases": _resumen_fases(state),
        "gates": _resumen_gates(paths.root),
        "validacion_final": validacion_final,
        "artefactos_principales": _listar_artefactos_principales(paths.root),
        "run_summary": run_summary,
        "observaciones": [
            "Manifest generado de forma determinista a partir del estado del Flow y artefactos del run.",
            "Los tiempos oficiales de gate son los calculados por el Flow; timestamps manuales en gate_humano.md son documentales.",
        ],
    }
    return _json_safe(manifest)


def _leer_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _python_version() -> str:
    import sys

    return sys.version.split()[0]


def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return ""


def _git_commit(project_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except Exception:
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def _django_validacion_version(project_root: Path) -> str:
    python_path = project_root / ".venv_Test" / "Scripts" / "python.exe"
    if not python_path.exists():
        return ""
    try:
        completed = subprocess.run(
            [str(python_path), "-c", "import django; print(django.get_version())"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except Exception:
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def _extraer_modelos(config: dict[str, Any]) -> dict[str, Any]:
    llms = config.get("model", {})
    if not isinstance(llms, dict):
        return {}
    modelos: dict[str, Any] = {}
    for perfil, datos in llms.items():
        if not isinstance(datos, dict):
            continue
        modelos[perfil] = {
            "provider": datos.get("provider", ""),
            "name": datos.get("name", ""),
            "temperature": datos.get("temperature", ""),
            "max_tokens": datos.get("max_tokens", ""),
        }
    return modelos


def _resumen_fases(state: Any) -> dict[str, dict[str, Any]]:
    fases: dict[str, dict[str, Any]] = {}
    for nombre, status in state.fases_status.items():
        fases[nombre] = {
            "reintentos_automaticos": status.reintentos_automaticos,
            "regeneraciones_humanas": status.regeneraciones_humanas,
            "gate_decision": status.gate_decision,
            "duracion_s_ejec": status.duracion_s_ejec,
            "duracion_s_gate_humano": status.duracion_s_gate_humano,
        }
    return fases


def _resumen_gates(run_dir: Path) -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = []
    for gate_path in sorted(run_dir.glob("0*_*/gate_humano.md")):
        rel = gate_path.relative_to(run_dir).as_posix()
        gates.append(
            {
                "path": rel,
                "sha256": sha256_file(gate_path),
                "metadata": _leer_frontmatter_gate(gate_path),
            }
        )
    return gates


def _leer_frontmatter_gate(path: Path) -> dict[str, Any]:
    try:
        lineas = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return {}
    if not lineas or lineas[0].strip() != "---":
        return {}
    cierre = None
    for i in range(1, len(lineas)):
        if lineas[i].strip() == "---":
            cierre = i
            break
    if cierre is None:
        return {}
    try:
        meta = yaml.safe_load("\n".join(lineas[1:cierre])) or {}
    except Exception:
        return {}
    return meta if isinstance(meta, dict) else {}


def _json_safe(value: Any) -> Any:
    """Convierte valores cargados desde YAML/Pydantic a JSON serializable."""
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    return value


def _resumen_validacion_final(validacion: Any) -> dict[str, Any]:
    review = validacion.review_final
    return {
        "ok_global": validacion.ok_global,
        "clasificacion": review.clasificacion,
        "checks_planificados": len(review.checks_planificados),
        "checks_ejecutados": len(review.checks_ejecutados),
        "checks_no_ejecutados": len(review.checks_no_ejecutados),
        "incidencias": list(review.incidencias),
        "factores_bloqueantes": list(review.factores_bloqueantes),
        "preparacion_manual_requerida": list(validacion.preparacion_manual_requerida),
    }


def _listar_artefactos_principales(run_dir: Path) -> list[dict[str, str]]:
    artefactos: list[dict[str, str]] = []
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(run_dir).as_posix()
        if "/codigo/" in rel or rel.startswith("99_cierre/_validacion_tmp/"):
            continue
        if "__pycache__" in rel:
            continue
        if path.suffix.lower() not in {".json", ".md", ".txt", ".yaml", ".yml"}:
            continue
        artefactos.append({"path": rel, "sha256": sha256_file(path)})
    return artefactos
