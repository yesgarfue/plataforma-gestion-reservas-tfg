# src/pipeline/state.py
"""
Estado del Flow del Caso 02 (Hundidos).

CrewAI Flow comparte una única instancia de `Caso02State` entre todos los
métodos `@start()` y `@listen()` del `Flow[Caso02State]`. Este archivo
define ese estado y las subestructuras que lo componen.

Principios de diseño:

  1. El state contiene slots para TODAS las fases del pipeline, pero casi
     todos empiezan como `None`. A medida que cada fase completa, su
     artefacto se asigna al slot correspondiente. Métodos posteriores pueden
     comprobar la presencia (`self.state.backlog is not None`) antes de usar.

  2. Los artefactos se guardan como modelos Pydantic tipados (no como dict).
     Esto da chequeo de tipos en tiempo de asignación gracias a
     `validate_assignment=True` heredado del `_StrictModel`.

  3. Todo lo que sea metadato de ejecución (run_id, paths, hashes,
     contadores) vive aquí. Los gates humanos NO viven en el state: se
     leen de disco (`gate_humano.md`) cuando hace falta.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .validation.schemas import (
    Backlog,
    BacklogSprint,
    DisenoTecnico,
    EntregaSprint,
    PlanSprints,
    RegistroRequisitos,
    ReviewSprint,
    Riesgos,
    ValidacionFinal,
)


# ---------------------------------------------------------------------------
# Subestructuras
# ---------------------------------------------------------------------------

class _StrictModel(BaseModel):
    """Base común: rechaza campos extra, normaliza whitespace, valida
    asignaciones. Duplicamos la clase aquí en vez de importar desde
    `schemas.py` para mantener `state.py` con un grafo de deps mínimo."""
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,  # necesario para `Path`
    )


class RunPaths(_StrictModel):
    """
    Rutas de carpeta de un Run, calculadas una sola vez al arrancar.
    Centralizar aquí evita string concatenation de rutas por toda la codebase.

    Se instancia con `build_run_paths(run_root)` (función al final del módulo).
    """
    root: Path
    fase_01_requisitos: Path
    fase_02_planificacion: Path
    fase_03_arquitectura: Path
    fase_03b_scaffold: Path
    fase_04_sprint_1: Path
    fase_05_sprint_2: Path
    fase_06_sprint_3: Path
    fase_99_cierre: Path
    logs: Path
    attempts: Path
    manifest: Path


class RunHashes(_StrictModel):
    """
    Hashes SHA-256 capturados al arranque del Run (Bloque 7 del spec).
    Estos valores se verifican antes de cada fase para detectar
    modificaciones durante la ejecución ('abortado_por_cambio_spec').

    `agents_yaml_por_crew` y `tasks_yaml_por_crew` son dicts {nombre_crew: hash}.
    """
    brief: str = ""
    pipeline_specs: str = ""
    pipeline_config: str = ""
    agents_yaml_por_crew: Dict[str, str] = Field(default_factory=dict)
    tasks_yaml_por_crew: Dict[str, str] = Field(default_factory=dict)


GateDecision = Literal["aceptado", "rechazado", "abortado", "N/A"]


class FaseStatus(_StrictModel):
    """
    Contadores y resultado de cada fase, alimentan el manifest
    (Bloque 7 del spec, estructura `fases[]`).

    Se actualizan incrementalmente durante la fase y al llegar al gate.
    `gate_decision` queda como 'N/A' para fases sin gate (sprints).
    """
    reintentos_automaticos: int = 0
    regeneraciones_humanas: int = 0
    gate_decision: GateDecision = "N/A"
    duracion_s_ejec: float = 0.0
    duracion_s_gate_humano: float = 0.0


# ---------------------------------------------------------------------------
# Estado principal del Flow
# ---------------------------------------------------------------------------

class Caso02State(_StrictModel):
    """
    Estado compartido por todos los métodos del Flow del Caso 02.

    Se instancia con valores por defecto vacíos al construir el Flow; los
    primeros métodos (típicamente el `@start()`) rellenan `run_id`,
    `paths`, `hashes` y `brief_texto`, y el resto de campos se van
    poblando a medida que cada fase completa su artefacto.
    """

    # --- Identidad del Run ---
    run_id: str = ""
    brief_texto: str = ""
    paths: Optional[RunPaths] = None
    hashes: RunHashes = Field(default_factory=RunHashes)

    # --- Artefactos por fase ---
    # Fase 01
    registro_requisitos: Optional[RegistroRequisitos] = None
    # Fase 02
    backlog: Optional[Backlog] = None
    plan_sprints: Optional[PlanSprints] = None
    riesgos: Optional[Riesgos] = None
    # Fase 03
    diseno_tecnico: Optional[DisenoTecnico] = None
    # Fases 04-06
    sprint_backlogs: Dict[int, BacklogSprint] = Field(default_factory=dict)
    entregas_sprint: Dict[int, EntregaSprint] = Field(default_factory=dict)
    reviews_sprint: Dict[int, ReviewSprint] = Field(default_factory=dict)
    validacion_final: Optional[ValidacionFinal] = None

    # --- Estado operativo por fase ---
    # Clave = nombre de fase (p.ej. '01_requisitos'). Se crea el slot al
    # iniciar cada fase. El manifest final se construye a partir de aquí.
    fases_status: Dict[str, FaseStatus] = Field(default_factory=dict)

    # --- Resultado global del Run ---
    # Se asigna al final por el método de cierre del Flow.
    resultado_final: Literal[
        "pendiente",
        "completo",
        "abortado_en_gate",
        "abortado_por_limite",
        "bloqueado_arranque",
        "abortado_por_cambio_spec",
    ] = "pendiente"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_run_paths(runs_dir: Path, run_id: str) -> RunPaths:
    """
    Dado el directorio raíz de Runs (`runs/`) y un `run_id`, construye
    el `RunPaths` con todas las subcarpetas canónicas del Bloque 4 del spec.

    NO crea las carpetas en disco. La creación la hace quien instancia el
    Run (típicamente el `@start()` del Flow), usando `ensure_dir` de
    `io_utils.py`. Separar cálculo de rutas y creación permite que este
    módulo sea puro y testeable.
    """
    root = runs_dir / run_id
    return RunPaths(
        root=root,
        fase_01_requisitos=root / "01_requisitos",
        fase_02_planificacion=root / "02_planificacion",
        fase_03_arquitectura=root / "03_arquitectura",
        fase_03b_scaffold=root / "03b_scaffold",
        fase_04_sprint_1=root / "04_sprint_1",
        fase_05_sprint_2=root / "05_sprint_2",
        fase_06_sprint_3=root / "06_sprint_3",
        fase_99_cierre=root / "99_cierre",
        logs=root / "logs",
        attempts=root / "_attempts",
        manifest=root / "99_cierre" / "manifest.json",
    )
