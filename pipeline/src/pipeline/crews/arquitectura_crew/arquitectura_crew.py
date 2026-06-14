# src/pipeline/crews/arquitectura_crew/arquitectura_crew.py
"""
Crew de la fase 03 (Arquitectura).

Un único agente (Arquitecto) ejecuta una única task
(`disenar_arquitectura`) que produce un `DisenoTecnico`.

El contexto completo de fases anteriores entra por `inputs` del kickoff:
registro de requisitos, backlog, plan de sprints, riesgos y feedback
humano. No se declara `context` entre tasks porque esta crew solo tiene
una task.

Convención CrewAI respetada:
  - Prompts en YAML (config/agents.yaml, config/tasks.yaml).
  - Clase decorada con @CrewBase.
  - Métodos @agent, @task, @crew cuyos nombres coinciden con las entradas
    raíz de los YAML.
"""

from __future__ import annotations

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from pipeline.utils.llm_factory import get_llm
from pipeline.validation.schemas import DisenoTecnico


@CrewBase
class ArquitecturaCrew:
    """Crew de la fase 03: produce el diseño técnico del proyecto."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # -----------------------------------------------------------------------
    # Agentes
    # -----------------------------------------------------------------------

    @agent
    def arquitecto(self) -> Agent:
        """
        Agente Arquitecto. Usa el perfil `architect` del
        pipeline_config.yaml, separado de `pm` para preservar trazabilidad
        por fase aunque ambos perfiles apunten al mismo modelo cloud.

        max_iter=5 mantiene el mismo criterio que el PM en cloud: margen
        suficiente para reparación interna de formato sin permitir bucles
        largos y caros.
        """
        return Agent(
            config=self.agents_config["arquitecto"],  # type: ignore[index]
            llm=get_llm("architect"),
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    # -----------------------------------------------------------------------
    # Tasks
    # -----------------------------------------------------------------------

    @task
    def disenar_arquitectura(self) -> Task:
        """
        Task única de arquitectura. La salida se fuerza a `DisenoTecnico`;
        si el LLM emite JSON fuera de schema, CrewAI/Pydantic lo rechaza
        y el Flow lo contabiliza como reintento automático.
        """
        return Task(
            config=self.tasks_config["disenar_arquitectura"],  # type: ignore[index]
            output_pydantic=DisenoTecnico,
        )

    # -----------------------------------------------------------------------
    # Crew
    # -----------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        """Construye el objeto Crew final con proceso secuencial."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
