# src/pipeline/utils/llm_factory.py
"""
Fábrica de instancias LLM configuradas desde `pipeline_config.yaml`.

Cada agente del pipeline recibe un LLM construido por esta factoría.
Tras Run 18, todas las fases activas usan Anthropic:

    - 'default'   → Analista de fase 01, Anthropic Claude Haiku.
    - 'pm'        → PM de fase 02, Anthropic Claude Haiku.
    - 'architect' → Arquitecto de fase 03, Anthropic Claude Haiku.
    - 'developer' → Desarrollador de sprints, Anthropic Claude Haiku.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Literal

import yaml
import os
from crewai import LLM

Perfil = Literal["default", "pm", "architect", "developer"]

# Ruta al YAML de config, resuelta relativa al paquete.
# `__file__` = .../src/pipeline/utils/llm_factory.py
# Subiendo dos niveles llegamos a src/pipeline/, y de ahí bajamos a config/.
_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "pipeline_config.yaml"
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _PROJECT_ROOT / ".env"


@lru_cache(maxsize=1)
def _load_config() -> Dict[str, Any]:
    """
    Carga el `pipeline_config.yaml` una sola vez por proceso.
    Cachear evita I/O en cada `get_llm()`, lo cual importa cuando hay
    docenas de llamadas al LLM a lo largo de un Run.
    """
    if not _CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"No se encuentra pipeline_config.yaml en {_CONFIG_PATH}. "
            "Verifica la estructura del proyecto."
        )
    with _CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def _load_dotenv_if_present() -> None:
    """
    Carga un `.env` simple sin depender de python-dotenv.

    Solo soporta líneas `CLAVE=valor`, que es suficiente para
    ANTHROPIC_API_KEY. No sobrescribe variables ya presentes en el
    entorno para permitir que la shell tenga prioridad.
    """
    if not _ENV_PATH.exists():
        return

    for raw_line in _ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def get_model_name(perfil: Perfil = "default") -> str:
    """Devuelve el nombre de modelo configurado para metadatos y tests."""
    cfg = _load_config()
    return str(cfg["model"][perfil]["name"])


def get_llm(perfil: Perfil = "default") -> LLM:
    """
    Construye una instancia de `crewai.LLM` para el perfil solicitado.

    Todos los perfiles activos usan Anthropic. La API key se lee de
    ANTHROPIC_API_KEY, cargada desde `.env` si existe. No se pasa seed:
    Anthropic no ofrece un parámetro equivalente estable; usamos
    temperature=0.0.
    """
    cfg = _load_config()
    model_cfg = cfg["model"][perfil]
    timeout_s = cfg["timeouts"]["llm_call_s"]

    # Forzar timeout HTTP en httpx (que litellm usa por debajo).
    # Si CrewAI/litellm tiene un timeout HTTP por defecto bajo, esto lo sobreescribe.
    os.environ["LITELLM_REQUEST_TIMEOUT"] = str(timeout_s)
    os.environ["OPENAI_TIMEOUT"] = str(timeout_s)

    provider = model_cfg["provider"]

    if provider == "ollama":
        return LLM(
            model=model_cfg["name"],
            base_url=model_cfg["api_base"],
            timeout=timeout_s,
        )

    if provider == "anthropic":
        _load_dotenv_if_present()
        api_key_env = model_cfg.get("api_key_env", "ANTHROPIC_API_KEY")
        api_key = os.environ.get(api_key_env)

        kwargs: dict[str, Any] = {
            "model": model_cfg["name"],
            "temperature": float(model_cfg.get("temperature", 0.0)),
            "max_tokens": int(model_cfg.get("max_tokens", 8192)),
            "timeout": timeout_s,
        }
        if api_key:
            kwargs["api_key"] = api_key

        return LLM(**kwargs)

    raise ValueError(f"Provider LLM no soportado: {provider!r}")
