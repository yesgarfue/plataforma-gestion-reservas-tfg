"""
Crew de desarrollo para los sprints 04-06.

Un único agente (Desarrollador) ejecuta una única task
(`implementar_sprint`) que produce una `EntregaSprint`.

La crew no escribe archivos en disco. El LLM devuelve un contrato Pydantic
con rutas relativas y contenidos completos; el Flow validará la entrega y
será responsable de escribirla dentro de `runs/run_X/0N_sprint_N/codigo/`.

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
from pipeline.validation.schemas import EntregaSprint


@CrewBase
class DesarrolloCrew:
    """Crew de desarrollo: produce una entrega de código para un sprint."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # -----------------------------------------------------------------------
    # Agentes
    # -----------------------------------------------------------------------

    @agent
    def desarrollador(self) -> Agent:
        """
        Agente Desarrollador. Usa el perfil `developer` del
        pipeline_config.yaml, separado de PM y Arquitecto para preservar
        trazabilidad por rol aunque apunte al mismo modelo cloud.
        """
        return Agent(
            config=self.agents_config["desarrollador"],  # type: ignore[index]
            llm=get_llm("developer"),
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    # -----------------------------------------------------------------------
    # Tasks
    # -----------------------------------------------------------------------

    @task
    def implementar_sprint(self) -> Task:
        """
        Task única de desarrollo. La salida se fuerza a `EntregaSprint`;
        si el LLM emite JSON fuera de schema, CrewAI/Pydantic lo rechaza
        y el Flow lo contabilizará como reintento automático al integrarla.
        """
        return Task(
            config=self.tasks_config["implementar_sprint"],  # type: ignore[index]
            output_pydantic=EntregaSprint,
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
