# src/pipeline/utils/renderers.py
"""
Renderers deterministas de artefactos del pipeline: consumen un modelo
Pydantic validado y devuelven su representación Markdown humana.

Principio (spec Bloque 3):
    JSON canónico = fuente de verdad.
    MD = función pura del JSON, regenerable en cualquier momento.

Consecuencia: estos renderers NO escriben archivos. Solo devuelven strings.
La escritura a disco la hace quien llama (normalmente `io_utils.write_text`).

Portado y reescrito desde el Run 01 (src/renderers.py). Cambios:

  - APIs ahora son `Modelo Pydantic -> str`, no `dict -> str`. El legacy
    trabajaba con TypedDict; aquí tenemos Pydantic, así que usamos atributos.
  - Nombres de campos alineados al spec nuevo (Bloque 3):
      `requisitos_funcionales` (no `fr`), `requisitos_no_funcionales` (no `nfr`),
      `historias` con campos {id, titulo, descripcion, criterios_aceptacion,
      prioridad, estimacion}, etc.
  - Se eliminan renderers de artefactos descartados del Run 01
    (`render_revision_context_md`, `render_stack_restricciones_md`,
    `render_dev_freeze_md`, `render_sprint_contract_map_md`, etc.).
  - Se añade `render_frontmatter`: helper único para el bloque YAML que
    encabeza todos los MD de artefacto (Bloque 3 del spec).
"""

from __future__ import annotations

from typing import List

from ..validation.schemas import (
    Backlog,
    BacklogSprint,
    DisenoTecnico,
    PlanSprints,
    RegistroRequisitos,
    ReviewSprint,
    Riesgos,
    ValidacionFinal,
)


# ---------------------------------------------------------------------------
# Helpers de escape / formato
# ---------------------------------------------------------------------------

def _md_bullets(items: List[str]) -> str:
    """Lista de strings → bullets Markdown. '(vacío)' si la lista está vacía."""
    if not items:
        return "- (vacío)\n"
    return "".join(f"- {x.strip()}\n" for x in items)


def _esc_cell(value: object) -> str:
    """
    Escapa una celda de tabla Markdown: reemplaza '|' por '\\|' (porque
    rompería la tabla) y saltos de línea por '<br>' (porque las tablas MD
    no permiten newlines reales dentro de una celda).
    """
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", "<br>").strip()


# ---------------------------------------------------------------------------
# Frontmatter YAML estándar (Bloque 3 del spec)
# ---------------------------------------------------------------------------

def render_frontmatter(
    *,
    run_id: str,
    fase: str,
    agente: str,
    modelo: str,
    timestamp: str,
    hash_brief: str,
    regeneraciones_previas: int = 0,
) -> str:
    """
    Genera el frontmatter YAML estándar que encabeza cada artefacto MD.
    Se escribe manualmente (sin librería YAML) porque son seis campos
    siempre iguales y queremos controlar el orden exacto.

    Campos definidos en pipeline_specs.md, Bloque 3.
    """
    return (
        "---\n"
        f"run_id: {run_id}\n"
        f"fase: {fase}\n"
        f"agente: {agente}\n"
        f"modelo: {modelo}\n"
        f"timestamp: {timestamp}\n"
        f"hash_brief: {hash_brief}\n"
        f"regeneraciones_previas: {regeneraciones_previas}\n"
        "---\n\n"
    )


# ---------------------------------------------------------------------------
# 01 — Registro de Requisitos (Analista)
# ---------------------------------------------------------------------------

def render_requisitos_md(registro: RegistroRequisitos) -> str:
    """
    Renderiza un `RegistroRequisitos` validado como Markdown.

    Secciones producidas:
      - Cabecera con id_ejecucion.
      - Tabla de requisitos funcionales.
      - Tabla de requisitos no funcionales.

    NO incluye frontmatter; se añade fuera con `render_frontmatter`.
    """
    md: List[str] = []

    md.append("# 01 — Registro de requisitos\n\n")
    md.append(f"**ID de ejecución**: `{registro.id_ejecucion}`\n\n")

    # --- Requisitos funcionales ---
    md.append("## Requisitos funcionales\n\n")
    md.append(f"Total: **{len(registro.requisitos_funcionales)}**\n\n")
    md.append("| ID | Descripción | Prioridad |\n")
    md.append("|---|---|---|\n")
    if registro.requisitos_funcionales:
        for r in registro.requisitos_funcionales:
            md.append(
                f"| {_esc_cell(r.id)} | {_esc_cell(r.descripcion)} | {_esc_cell(r.prioridad)} |\n"
            )
    else:
        md.append("| _(sin requisitos)_ | | |\n")
    md.append("\n")

    # --- Requisitos no funcionales ---
    md.append("## Requisitos no funcionales\n\n")
    md.append(f"Total: **{len(registro.requisitos_no_funcionales)}**\n\n")
    md.append("| ID | Categoría | Condición / Métrica | Prioridad |\n")
    md.append("|---|---|---|---|\n")
    if registro.requisitos_no_funcionales:
        for r in registro.requisitos_no_funcionales:
            md.append(
                f"| {_esc_cell(r.id)} | {_esc_cell(r.categoria)} | "
                f"{_esc_cell(r.condicion_metrica)} | {_esc_cell(r.prioridad)} |\n"
            )
    else:
        md.append("| _(sin requisitos)_ | | | |\n")
    md.append("\n")

    return "".join(md)


# ---------------------------------------------------------------------------
# 02 — Backlog (PM)
# ---------------------------------------------------------------------------

def render_backlog_md(backlog: Backlog) -> str:
    """
    Renderiza un `Backlog` validado como Markdown.

    Cada historia se muestra como bloque con su tabla resumen y, debajo,
    la lista de criterios de aceptación. No se fuerzan en una sola tabla
    porque los criterios suelen ser multi-línea y romperían el layout.
    """
    md: List[str] = []

    md.append("# 02 — Backlog\n\n")
    md.append(f"**ID de ejecución**: `{backlog.id_ejecucion}`\n\n")
    md.append(f"Total de historias: **{len(backlog.historias)}**\n\n")

    if not backlog.historias:
        md.append("_(sin historias)_\n")
        return "".join(md)

    md.append("## Historias\n\n")
    for h in backlog.historias:
        md.append(f"### {h.id} — {h.titulo}\n\n")
        md.append(f"- **Prioridad**: {h.prioridad}\n")
        md.append(f"- **Estimación**: {h.estimacion}\n\n")
        md.append(f"**Descripción**\n\n{h.descripcion.strip()}\n\n")
        md.append("**Criterios de aceptación**\n\n")
        if h.criterios_aceptacion:
            for c in h.criterios_aceptacion:
                md.append(f"- {c.strip()}\n")
        else:
            md.append("- _(sin criterios)_\n")
        md.append("\n")

    return "".join(md)


# ---------------------------------------------------------------------------
# 04-06 — Backlog derivado por sprint (script)
# ---------------------------------------------------------------------------

def render_backlog_sprint_md(backlog_sprint: BacklogSprint) -> str:
    """
    Renderiza un `BacklogSprint` derivado de forma determinista.

    Es deliberadamente parecido a `render_backlog_md`, pero deja visible el
    número de sprint para que el Desarrollador y la revisión automática
    trabajen sobre un subconjunto claro del backlog aceptado.
    """
    md: List[str] = []

    md.append(f"# Sprint {backlog_sprint.numero_sprint} — Backlog del sprint\n\n")
    md.append(f"**ID de ejecución**: `{backlog_sprint.id_ejecucion}`\n\n")
    md.append(f"Total de historias: **{len(backlog_sprint.historias)}**\n\n")

    if not backlog_sprint.historias:
        md.append("_(sin historias)_\n")
        return "".join(md)

    md.append("## Historias del sprint\n\n")
    for h in backlog_sprint.historias:
        md.append(f"### {h.id} — {h.titulo}\n\n")
        md.append(f"- **Prioridad**: {h.prioridad}\n")
        md.append(f"- **Estimación**: {h.estimacion}\n\n")
        md.append(f"**Descripción**\n\n{h.descripcion.strip()}\n\n")
        md.append("**Criterios de aceptación**\n\n")
        if h.criterios_aceptacion:
            for c in h.criterios_aceptacion:
                md.append(f"- {c.strip()}\n")
        else:
            md.append("- _(sin criterios)_\n")
        md.append("\n")

    return "".join(md)


# ---------------------------------------------------------------------------
# 02 — Plan de Sprints (PM)
# ---------------------------------------------------------------------------

def render_plan_sprints_md(plan: PlanSprints) -> str:
    """
    Renderiza un `PlanSprints` validado como Markdown.

    Por cada sprint muestra: número, objetivo, historias asignadas (IDs
    del backlog) y entregable verificable.
    """
    md: List[str] = []

    md.append("# 02 — Plan de sprints\n\n")
    md.append(f"**ID de ejecución**: `{plan.id_ejecucion}`\n\n")
    md.append(f"Número de sprints: **{len(plan.sprints)}**\n\n")

    if not plan.sprints:
        md.append("_(sin sprints)_\n")
        return "".join(md)

    for s in plan.sprints:
        md.append(f"## Sprint {s.numero}\n\n")
        md.append(f"**Objetivo**: {s.objetivo.strip()}\n\n")
        md.append("**Historias asignadas**\n\n")
        if s.historias_ids:
            for hid in s.historias_ids:
                md.append(f"- `{_esc_cell(hid)}`\n")
        else:
            md.append("- _(sin historias asignadas)_\n")
        md.append("\n")
        md.append(f"**Entregable verificable**: {s.entregable_verificable.strip()}\n\n")

    return "".join(md)


# ---------------------------------------------------------------------------
# 02 — Riesgos (PM)
# ---------------------------------------------------------------------------

def render_riesgos_md(riesgos: Riesgos) -> str:
    """
    Renderiza un `Riesgos` validado como Markdown, con una tabla única.
    """
    md: List[str] = []

    md.append("# 02 — Registro de riesgos\n\n")
    md.append(f"**ID de ejecución**: `{riesgos.id_ejecucion}`\n\n")
    md.append(f"Total de riesgos: **{len(riesgos.riesgos)}**\n\n")

    md.append("| ID | Descripción | Probabilidad | Impacto | Mitigación |\n")
    md.append("|---|---|---|---|---|\n")
    if riesgos.riesgos:
        for r in riesgos.riesgos:
            md.append(
                f"| {_esc_cell(r.id)} | {_esc_cell(r.descripcion)} | "
                f"{_esc_cell(r.probabilidad)} | {_esc_cell(r.impacto)} | "
                f"{_esc_cell(r.mitigacion)} |\n"
            )
    else:
        md.append("| _(sin riesgos)_ | | | | |\n")
    md.append("\n")

    return "".join(md)


# ---------------------------------------------------------------------------
# 03 — Diseño técnico (Arquitecto)
# ---------------------------------------------------------------------------
def render_diseno_tecnico_md(diseno: DisenoTecnico) -> str:
    """
    Renderiza un `DisenoTecnico` validado como Markdown.

    Se mantiene fiel al schema congelado: stack, apps Django, modelos y
    rutas. La riqueza del diseño debe venir en el contenido generado por
    el Arquitecto, no en campos extra añadidos por el renderer.
    """
    md: List[str] = []

    md.append("# 03 — Diseño técnico\n\n")
    md.append(f"**ID de ejecución**: `{diseno.id_ejecucion}`\n\n")

    md.append("## Stack técnico\n\n")
    md.append(_md_bullets(diseno.stack))
    md.append("\n")

    md.append("## Apps Django\n\n")
    if not diseno.apps_django:
        md.append("_(sin apps Django)_\n\n")
    else:
        for app in diseno.apps_django:
            md.append(f"### {app.nombre}\n\n")
            md.append(f"**Propósito**: {app.proposito.strip()}\n\n")
            md.append("**Archivos principales**\n\n")
            md.append(_md_bullets(app.archivos_principales))
            md.append("\n")

    md.append("## Modelos\n\n")
    if not diseno.modelos:
        md.append("_(sin modelos)_\n\n")
    else:
        for modelo in diseno.modelos:
            md.append(f"### {modelo.nombre}\n\n")
            md.append(f"- **App**: {modelo.app}\n\n")
            md.append("**Campos**\n\n")
            md.append(_md_bullets(modelo.campos))
            md.append("\n")

    md.append("## Rutas\n\n")
    md.append("| Path | Name | Método | Auth | Vista |\n")
    md.append("|---|---|---|---|---|\n")
    if diseno.rutas:
        for ruta in diseno.rutas:
            md.append(
                f"| {_esc_cell(ruta.path)} | {_esc_cell(ruta.name)} | "
                f"{_esc_cell(ruta.metodo)} | {_esc_cell(ruta.auth)} | "
                f"{_esc_cell(ruta.vista)} |\n"
            )
    else:
        md.append("| _(sin rutas)_ | | | | |\n")
    md.append("\n")

    return "".join(md)


# ---------------------------------------------------------------------------
# 04-06 — Review automático de sprint (script)
# ---------------------------------------------------------------------------

def render_review_sprint_md(review: ReviewSprint) -> str:
    """Renderiza un `ReviewSprint` factual como Markdown."""
    md: List[str] = []

    md.append(f"# Sprint {review.sprint} — Review automático\n\n")
    md.append(f"**ID de ejecución**: `{review.id_ejecucion}`\n\n")

    md.append("## Arranque\n\n")
    md.append(f"- **Comando**: `python manage.py check`\n")
    md.append(f"- **OK**: `{review.arranque.ok}`\n")
    md.append(f"- **Return code**: `{review.arranque.returncode}`\n")
    md.append(f"- **Timeout**: `{review.arranque.timeout}` ({review.arranque.timeout_s}s)\n\n")

    if review.arranque.stdout_resumen:
        md.append("### stdout\n\n")
        md.append("```text\n")
        md.append(review.arranque.stdout_resumen.strip())
        md.append("\n```\n\n")

    if review.arranque.stderr_resumen:
        md.append("### stderr\n\n")
        md.append("```text\n")
        md.append(review.arranque.stderr_resumen.strip())
        md.append("\n```\n\n")

    md.append("## Incidencias ejecutables\n\n")
    if review.incidencias:
        for incidencia in review.incidencias:
            md.append(f"- {_esc_cell(incidencia)}\n")
    else:
        md.append("- _(sin incidencias ejecutables detectadas)_\n")
    md.append("\n")

    if review.rutas:
        md.append("## Rutas revisadas\n\n")
        md.append("| Ruta | Ejecutada | OK | Status | Detalle |\n")
        md.append("|---|---:|---:|---:|---|\n")
        for ruta in review.rutas:
            detalle = ruta.detalle or ruta.error or ruta.motivo_no_ejecutado
            status = "" if ruta.status_code is None else str(ruta.status_code)
            md.append(
                f"| `{_esc_cell(ruta.path)}` | `{ruta.ejecutado}` | "
                f"`{ruta.ok}` | `{status}` | {_esc_cell(detalle)} |\n"
            )
        md.append("\n")

    if review.templates:
        md.append("## Templates revisadas\n\n")
        md.append("| Template | Ejecutada | OK | Detalle |\n")
        md.append("|---|---:|---:|---|\n")
        for template in review.templates:
            detalle = template.error or template.motivo_no_ejecutado
            md.append(
                f"| `{_esc_cell(template.template)}` | `{template.ejecutado}` | "
                f"`{template.ok}` | {_esc_cell(detalle)} |\n"
            )
        md.append("\n")

    md.append("## Cumplimiento por historia\n\n")
    md.append("| Historia | Estado |\n")
    md.append("|---|---|\n")
    if review.cumplimiento:
        for historia_id in review.backlog_items_pedidos:
            estado = review.cumplimiento.get(historia_id, "ausente")
            md.append(f"| `{_esc_cell(historia_id)}` | `{_esc_cell(estado)}` |\n")
    else:
        md.append("| _(sin historias)_ | |\n")
    md.append("\n")

    md.append("## Archivos inspeccionados\n\n")
    if review.archivos_entregados:
        for path in review.archivos_entregados:
            md.append(f"- `{path}`\n")
    else:
        md.append("- _(sin archivos)_\n")
    md.append("\n")

    return "".join(md)


# ---------------------------------------------------------------------------
# 99 — Review final determinista (script)
# ---------------------------------------------------------------------------

def render_review_final_md(validacion: ValidacionFinal) -> str:
    """Renderiza la validacion final como Markdown humano."""
    md: List[str] = []
    review = validacion.review_final

    md.append("# 99 — Review final determinista\n\n")
    md.append(f"**ID de ejecucion**: `{validacion.id_ejecucion}`\n\n")
    md.append(f"**Protocolo**: `{review.protocolo_validacion}`\n\n")
    md.append(f"**OK global**: `{validacion.ok_global}`\n\n")
    md.append(f"**Clasificacion**: `{review.clasificacion}`\n\n")

    md.append("## Resumen de checks\n\n")
    md.append(f"- Planificados: **{len(review.checks_planificados)}**\n")
    md.append(f"- Ejecutados: **{len(review.checks_ejecutados)}**\n")
    md.append(f"- No ejecutados: **{len(review.checks_no_ejecutados)}**\n\n")

    if review.checks_no_ejecutados:
        md.append("### Checks no ejecutados\n\n")
        md.append("| Check | Motivo |\n")
        md.append("|---|---|\n")
        for check_id, motivo in review.checks_no_ejecutados.items():
            md.append(f"| `{_esc_cell(check_id)}` | {_esc_cell(motivo)} |\n")
        md.append("\n")

    md.append("## Comandos\n\n")
    md.append("| Check | Ejecutado | OK | Return code | Timeout |\n")
    md.append("|---|---:|---:|---:|---:|\n")
    for comando in (
        validacion.check,
        validacion.migrate,
        validacion.seed_data,
        validacion.runserver,
    ):
        returncode = "" if comando.returncode is None else str(comando.returncode)
        md.append(
            f"| `{_esc_cell(comando.nombre)}` | `{comando.ejecutado}` | "
            f"`{comando.ok}` | `{returncode}` | `{comando.timeout}` |\n"
        )
    md.append("\n")

    md.append("## Migraciones\n\n")
    md.append(f"- **OK**: `{validacion.migraciones.ok}`\n")
    md.append(
        f"- Apps con modelos: "
        f"{', '.join(validacion.migraciones.apps_con_modelos) or 'ninguna'}\n"
    )
    md.append(
        f"- Apps sin migraciones: "
        f"{', '.join(validacion.migraciones.apps_sin_migraciones) or 'ninguna'}\n\n"
    )

    md.append("## Rutas minimas\n\n")
    md.append("| Ruta | Ejecutada | OK | Status | Detalle |\n")
    md.append("|---|---:|---:|---:|---|\n")
    for ruta in validacion.rutas:
        status = "" if ruta.status_code is None else str(ruta.status_code)
        detalle = ruta.error or ruta.motivo_no_ejecutado or ruta.final_url
        md.append(
            f"| `{_esc_cell(ruta.path)}` | `{ruta.ejecutado}` | "
            f"`{ruta.ok}` | `{status}` | {_esc_cell(detalle)} |\n"
        )
    md.append("\n")

    md.append("## Templates criticas\n\n")
    md.append("| Template | Ejecutada | OK | Detalle |\n")
    md.append("|---|---:|---:|---|\n")
    for template in validacion.templates:
        detalle = template.error or template.motivo_no_ejecutado
        md.append(
            f"| `{_esc_cell(template.template)}` | `{template.ejecutado}` | "
            f"`{template.ok}` | {_esc_cell(detalle)} |\n"
        )
    md.append("\n")

    md.append("## Incidencias\n\n")
    if review.incidencias:
        for incidencia in review.incidencias:
            md.append(f"- {incidencia}\n")
    else:
        md.append("- _(sin incidencias)_\n")
    md.append("\n")

    md.append("## Factores bloqueantes\n\n")
    if review.factores_bloqueantes:
        for factor in review.factores_bloqueantes:
            md.append(f"- {factor}\n")
    else:
        md.append("- _(sin factores bloqueantes)_\n")
    md.append("\n")

    md.append("## Preparacion manual requerida\n\n")
    if validacion.preparacion_manual_requerida:
        for item in validacion.preparacion_manual_requerida:
            md.append(f"- {item}\n")
    else:
        md.append("- _(no detectada)_\n")
    md.append("\n")

    return "".join(md)
