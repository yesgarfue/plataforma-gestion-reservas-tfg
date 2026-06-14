# src/pipeline/crews/planificacion_crew/planificacion_crew.py
"""
Crew de la fase 02 (Planificación).

Un único agente (PM) ejecuta tres tasks secuenciales:

    construir_backlog  →  planificar_sprints  →  analizar_riesgos

Cada task fuerza su salida al modelo Pydantic correspondiente
mediante `output_pydantic`:

    construir_backlog   →  Backlog
    planificar_sprints  →  PlanSprints
    analizar_riesgos    →  Riesgos

El `context` se declara explícitamente en cada task (no se confía
en la propagación implícita de `Process.sequential`):

    construir_backlog   →  sin context (recibe el registro vía inputs).
    planificar_sprints  →  context=[construir_backlog].
    analizar_riesgos    →  context=[construir_backlog,
                                    planificar_sprints].

Razón de declarar context explícito: `analizar_riesgos` necesita
ver TANTO el backlog como el plan, no solo el plan (que es lo que
recibiría por propagación implícita de la task inmediatamente
anterior). Hacerlo explícito también deja autodocumentadas las
dependencias entre tasks.

Convención CrewAI respetada (igual que en `requisitos_crew.py`):
  - Prompts en YAML (config/agents.yaml, config/tasks.yaml).
  - Clase decorada con @CrewBase.
  - Métodos @agent, @task, @crew cuyos nombres coinciden con las
    entradas raíz de los YAML.

Esta clase no se invoca todavía desde el Flow. Su integración
(con reintentos automáticos y gate humano) es el subpaso 8f.
"""

from __future__ import annotations

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from pipeline.utils.llm_factory import get_llm
from pipeline.validation.schemas import Backlog, PlanSprints, Riesgos


@CrewBase
class PlanificacionCrew:
    """
    Crew de la fase 02: produce backlog, plan de sprints y registro
    de riesgos a partir del registro de requisitos aceptado en la
    fase 01.
    """

    # Rutas a los YAML, relativas a este archivo. CrewAI las resuelve
    # automáticamente y las usa para construir agentes y tareas.
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # -----------------------------------------------------------------------
    # Agentes
    # -----------------------------------------------------------------------

    @agent
    def pm(self) -> Agent:
        """
        Agente PM (Project Manager). El decorador @agent lee la entrada
        'pm' de agents.yaml (role/goal/backstory) y construye el Agent.
        Le enchufamos el LLM configurado con el perfil 'pm' del
        pipeline_config.yaml. Ese perfil apunta a Anthropic Claude Haiku,
        igual que el resto de fases activas tras Run 18.

        max_iter=5: con el PM en cloud no necesitamos el margen defensivo
        de 15 iteraciones que se añadió para qwen2.5-coder:7b local. Un
        límite más bajo reduce coste y evita bucles de reparación largos
        si una salida no cumple el esquema.
        """
        return Agent(
            config=self.agents_config["pm"],  # type: ignore[index]
            llm=get_llm("pm"),
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    # -----------------------------------------------------------------------
    # Tasks
    # -----------------------------------------------------------------------
    #
    # ORDEN IMPORTANTE: @CrewBase recoge las tasks en self.tasks en el
    # orden en que aparecen los métodos @task en la clase. Ese mismo
    # orden es el que ejecuta Process.sequential. Cualquier reordenación
    # rompe las dependencias declaradas en `context`.

    @task
    def construir_backlog(self) -> Task:
        """
        Task 1: produce el `Backlog` a partir del registro de requisitos.

        No declara `context` porque es la primera task. El registro
        de requisitos llega como input al kickoff a través del
        placeholder {registro_requisitos_json} en tasks.yaml.

        La salida se fuerza a `Backlog`: si el LLM devuelve algo que
        no valida, CrewAI lanza ValidationError, que el helper de fase
        02 (subpaso 8f) capturará y contará como reintento automático.
        """
        return Task(
            config=self.tasks_config["construir_backlog"],  # type: ignore[index]
            output_pydantic=Backlog,
        )

    @task
    def planificar_sprints(self) -> Task:
        """
        Task 2: produce el `PlanSprints` a partir del backlog.

        Declara `context=[self.construir_backlog()]`: el output de la
        task 1 entra en el prompt de esta task. CrewAI serializa
        automáticamente el output de la task referenciada y lo añade
        al contexto del prompt antes de invocar al LLM.

        La salida se fuerza a `PlanSprints`. Las reglas duras de la
        partición exacta (3 sprints, cobertura completa, sin
        solapamientos) se chequean a posteriori con
        validate_plan_sprints_contenido() en el helper de fase 02.
        """
        return Task(
            config=self.tasks_config["planificar_sprints"],  # type: ignore[index]
            output_pydantic=PlanSprints,
            context=[self.construir_backlog()],
        )

    @task
    def analizar_riesgos(self) -> Task:
        """
        Task 3: produce el `Riesgos` a partir del registro, el backlog
        y el plan.

        Declara `context=[self.construir_backlog(),
        self.planificar_sprints()]`: ambas tasks anteriores entran en
        el prompt. Esto permite al PM razonar riesgos a la luz tanto
        del backlog completo como del reparto entre sprints (p.ej.
        riesgos de dependencias cruzadas entre sprints).

        La salida se fuerza a `Riesgos`. La validación de contenido
        mínimo (≥5 riesgos, IDs únicos, capitalizaciones correctas)
        se chequea a posteriori con validate_riesgos_contenido() en
        el helper de fase 02.
        """
        return Task(
            config=self.tasks_config["analizar_riesgos"],  # type: ignore[index]
            output_pydantic=Riesgos,
            context=[
                self.construir_backlog(),
                self.planificar_sprints(),
            ],
        )

    # -----------------------------------------------------------------------
    # Crew
    # -----------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        """
        Construye el objeto Crew final. Proceso secuencial: las tres
        tasks se ejecutan en el orden definido por @CrewBase
        (construir_backlog → planificar_sprints → analizar_riesgos).

        El context declarado explícitamente en cada task se respeta
        por encima del orden secuencial: aunque `analizar_riesgos`
        venga después de `planificar_sprints` por orden, lo que
        importa para el prompt es la lista de tasks en `context`.
        """
        return Crew(
            agents=self.agents,          # inyectados por @CrewBase
            tasks=self.tasks,            # inyectados por @CrewBase
            process=Process.sequential,
            verbose=True,
        )
