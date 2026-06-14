from __future__ import annotations
import os
from textwrap import dedent
from crewai import Agent, Task, LLM

MODEL_ID = os.getenv("MODEL_ID", "ollama/qwen2.5:14b-instruct")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def _make_llm() -> LLM:
    return LLM(model=MODEL_ID, base_url=OLLAMA_URL)


def build_closed_prompt_context(sprint_contract: dict, stack: dict) -> str:
    """
    Construye el bloque de contexto cerrado que se inyecta en TODOS los prompts.
    El modelo nunca ve más que esto del diseño técnico.
    """
    models    = sprint_contract.get("models", [])
    routes    = sprint_contract.get("routes", [])
    templates = sprint_contract.get("templates", [])
    sprint_id = sprint_contract.get("sprint_id", "?")
    freeze_id = sprint_contract.get("freeze_id", "?")
    s_type    = sprint_contract.get("type", "full")

    forbidden_imports = stack.get("forbidden_imports", [
        "requests", "httpx", "celery", "redis",
        "rest_framework", "graphene", "channels",
    ])

    return dedent(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║         CONTRATO DE SPRINT — LECTURA OBLIGATORIA         ║
    ╚══════════════════════════════════════════════════════════╝
    sprint_id   : {sprint_id}
    freeze_id   : {freeze_id}
    sprint_type : {s_type}

    MODELOS QUE PUEDES USAR (SOLO ESTOS — sin excepción):
    {chr(10).join(f"  - {m}" for m in models) or "  (ninguno en este sprint)"}

    RUTAS QUE DEBES IMPLEMENTAR (SOLO ESTAS):
    {chr(10).join(f"  - {r}" for r in routes) or "  (ninguna en este sprint)"}

    TEMPLATES QUE DEBES GENERAR (SOLO ESTOS):
    {chr(10).join(f"  - {t}" for t in templates) or "  (ninguno en este sprint)"}

    STACK NO NEGOCIABLE (del contrato 09):
      - Framework  : Django (server-rendered, NO SPA)
      - Frontend   : Django Templates + Bootstrap
      - Base datos : SQLite + Django ORM
      - Sin APIs externas ni servicios de terceros

    PROHIBICIONES ABSOLUTAS:
      - Crear apps Django no existentes
      - Definir modelos NO listados arriba
      - Agregar campos no definidos en el contrato de entidades (09b)
      - Usar fetch(), axios o XMLHttpRequest en templates
      - Importar paquetes prohibidos: {", ".join(forbidden_imports)}
      - Añadir rutas fuera de las listadas arriba
      - Lógica de negocio dentro de templates HTML

    FORMATO DE RESPUESTA — JSON PURO (sin texto previo ni markdown):
    {{
      "sprint_id": "{sprint_id}",
      "artifacts": [
        {{
          "name"   : "NombreClaseOArchivo",
          "type"   : "model|view|urls|template",
          "path"   : "ruta/relativa/desde/repo_root/archivo.ext",
          "content": "contenido completo del archivo"
        }}
      ]
    }}
    ══════════════════════════════════════════════════════════
    """).strip()


def create_developer_agent() -> Agent:
    return Agent(
        role="Django Developer",
        goal=(
            "Implementar EXACTAMENTE lo definido en el contrato de sprint. "
            "Ni más, ni menos. Toda adición fuera del contrato es un error grave."
        ),
        backstory=dedent("""
            Eres un desarrollador Django disciplinado que opera bajo contratos de código
            estrictos. No tomas iniciativas arquitectónicas. No "mejoras" el diseño.
            Si el contrato no lo contempla, no lo implementas.
            Tu output siempre es un JSON válido con la estructura especificada.
        """),
        llm=_make_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_frontend_agent() -> Agent:
    return Agent(
        role="Django Template Developer",
        goal=(
            "Generar templates HTML funcionales con Django Templates + Bootstrap. "
            "Sin lógica de negocio. Sin dependencias externas."
        ),
        backstory=dedent("""
            Eres especialista en Django Templates y Bootstrap.
            Generas HTML semántico y accesible. Nunca añades JavaScript complejo.
            Nunca escribes lógica de negocio en templates.
            Tu output siempre es un JSON válido con la estructura especificada.
        """),
        llm=_make_llm(),
        verbose=True,
        allow_delegation=False,
    )


def build_python_task(agent: Agent, context: str, sprint_contract: dict) -> Task:
    models = sprint_contract.get("models", [])
    routes = sprint_contract.get("routes", [])

    return Task(
        description=dedent(f"""
            {context}

            TU TAREA:
            Genera el código Python para este sprint.
            Produce ÚNICAMENTE (según lo que indique el contrato):
              - models.py  → modelos: {models}
              - views.py   → vistas para las rutas: {routes}
              - urls.py    → path() para las rutas: {routes}

            Responde SOLO con el JSON especificado. Sin texto adicional.
        """),
        expected_output="JSON con artefactos Python generados según contrato de sprint.",
        agent=agent,
    )


def build_template_task(agent: Agent, context: str, sprint_contract: dict) -> Task:
    templates = sprint_contract.get("templates", [])

    return Task(
        description=dedent(f"""
            {context}

            TU TAREA:
            Genera los templates HTML para este sprint.
            Templates a generar (exactamente estos):
            {chr(10).join(f"  - {t}" for t in templates)}

            Cada template debe:
              - Usar {{% extends 'base.html' %}}
              - Layout con Bootstrap
              - Variables de contexto Django ({{{{ variable }}}})
              - Sin lógica de negocio
              - Sin fetch(), axios ni JS complejo

            Responde SOLO con el JSON especificado. Sin texto adicional.
        """),
        expected_output="JSON con templates HTML generados según contrato de sprint.",
        agent=agent,
    )