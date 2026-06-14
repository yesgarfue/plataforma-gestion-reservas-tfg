# src/pipeline/utils/sprint_backlog_builder.py
"""
Derivación determinista de backlogs por sprint.

Entrada:
  - Backlog aceptado en fase 02.
  - PlanSprints aceptado en fase 02.

Salida:
  - Tres BacklogSprint, uno por cada sprint planificado.

No hay LLM en este paso. La función solo aplica la partición ya aceptada
por el PM y validada por `validate_plan_sprints_contenido`.
"""

from __future__ import annotations

from collections import Counter

from pipeline.validation.schemas import Backlog, BacklogSprint, PlanSprints


def derivar_sprint_backlogs(
    *,
    backlog: Backlog,
    plan: PlanSprints,
    run_id: str,
) -> list[BacklogSprint]:
    """
    Deriva un `BacklogSprint` por sprint del plan.

    Valida defensivamente:
      - Que cada ID del plan exista en el backlog.
      - Que ninguna historia aparezca en más de un sprint.
      - Que todo el backlog quede cubierto.

    Aunque estas reglas ya se comprueban al validar fase 02, repetirlas aquí
    hace que el paso determinista sea autocontenido y falle con un mensaje
    claro si se invoca con artefactos inconsistentes.
    """
    historias_por_id = {historia.id: historia for historia in backlog.historias}
    ids_backlog = set(historias_por_id)

    ids_plan_flat: list[str] = []
    for sprint in plan.sprints:
        ids_plan_flat.extend(sprint.historias_ids)

    ids_plan = set(ids_plan_flat)
    ids_inexistentes = sorted(ids_plan - ids_backlog)
    if ids_inexistentes:
        raise ValueError(
            "El plan referencia historias que no existen en el backlog: "
            f"{ids_inexistentes}."
        )

    duplicados = sorted(
        historia_id
        for historia_id, veces in Counter(ids_plan_flat).items()
        if veces > 1
    )
    if duplicados:
        raise ValueError(
            "El plan asigna historias a más de un sprint: "
            f"{duplicados}."
        )

    ids_sin_asignar = sorted(ids_backlog - ids_plan)
    if ids_sin_asignar:
        raise ValueError(
            "Hay historias del backlog sin asignar a ningún sprint: "
            f"{ids_sin_asignar}."
        )

    sprint_backlogs: list[BacklogSprint] = []
    for sprint in sorted(plan.sprints, key=lambda s: s.numero):
        historias = [historias_por_id[historia_id] for historia_id in sprint.historias_ids]
        sprint_backlogs.append(
            BacklogSprint(
                id_ejecucion=run_id,
                numero_sprint=sprint.numero,
                historias=historias,
            )
        )

    return sprint_backlogs
