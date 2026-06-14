# src/pipeline/crews/requisitos_crew/requisitos_crew.py
"""
Crew de la fase 01 (Requisitos).

Un único agente (Analista) ejecuta una única task (extraer requisitos
desde el brief). La salida se fuerza al tipo Pydantic
`RegistroRequisitos` mediante `output_pydantic`: si el LLM devuelve
algo que no valida, CrewAI lanza una excepción que captura quien
invoca `kickoff()`.

Convención oficial de CrewAI respetada:
  - Prompts en YAML (config/agents.yaml, config/tasks.yaml).
  - Clase decorada con @CrewBase.
  - Métodos @agent, @task, @crew cuyos nombres coinciden con las
    entradas raíz de los YAML.
"""

from __future__ import annotations

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from pipeline.utils.llm_factory import get_llm
from pipeline.validation.schemas import RegistroRequisitos


@CrewBase
class RequisitosCrew:
    """Crew de la fase 01: extrae el registro de requisitos desde el brief."""

    # Rutas a los YAML, relativas a este archivo. CrewAI las resuelve
    # automáticamente y las usa para construir agentes y tareas.
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # -----------------------------------------------------------------------
    # Agentes
    # -----------------------------------------------------------------------

    @agent
    def analista(self) -> Agent:
        """
        Agente Analista. El decorador @agent lee la entrada 'analista' de
        agents.yaml (role/goal/backstory) y construye el Agent. Le
        enchufamos aquí el LLM configurado con el perfil 'default' del
        pipeline_config.yaml.
        """
        return Agent(
            config=self.agents_config["analista"],  # type: ignore[index]
            llm=get_llm("default"),
            verbose=True,
            allow_delegation=False,
            # max_iter bajo porque el Analista no debe iterar contra sí
            # mismo muchas veces: o devuelve el registro, o lo rehace.
            max_iter=3,
        )

    # -----------------------------------------------------------------------
    # Tasks
    # -----------------------------------------------------------------------

    @task
    def extraer_requisitos(self) -> Task:
        """
        Task 'extraer_requisitos'. Leída de tasks.yaml. La salida se
        fuerza al tipo Pydantic `RegistroRequisitos`: CrewAI intenta
        parsear la respuesta del LLM a ese modelo, y lanza
        ValidationError si no cuadra.
        """
        return Task(
            config=self.tasks_config["extraer_requisitos"],  # type: ignore[index]
            output_pydantic=RegistroRequisitos,
        )

    # -----------------------------------------------------------------------
    # Crew
    # -----------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        """
        Construye el objeto Crew final. Proceso secuencial (trivial aquí
        con un único agente y una única task, pero es la convención).
        """
        return Crew(
            agents=self.agents,          # inyectados por @CrewBase
            tasks=self.tasks,            # inyectados por @CrewBase
            process=Process.sequential,
            verbose=True,
        )