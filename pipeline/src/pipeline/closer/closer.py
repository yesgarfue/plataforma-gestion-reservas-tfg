"""Closer documental determinista del run."""

from __future__ import annotations

from typing import Any


def render_readme_cierre(*, state: Any, manifest: dict[str, Any]) -> str:
    """Genera un README humano-legible del run sin juicio subjetivo."""
    validacion = manifest.get("validacion_final") or {}
    fases = manifest.get("fases") or {}
    lines: list[str] = []
    lines.append("# Cierre del run\n")
    lines.append(f"- **Run**: `{manifest.get('run_id', state.run_id)}`")
    lines.append(f"- **Resultado Flow**: `{manifest.get('resultado_final', state.resultado_final)}`")
    if validacion:
        lines.append(f"- **Validacion final OK global**: `{validacion.get('ok_global')}`")
        lines.append(f"- **Clasificacion validacion final**: `{validacion.get('clasificacion')}`")
    lines.append("")
    lines.append("## Artefactos principales\n")
    lines.append("- `run_summary.json`: resumen operativo del Flow.")
    lines.append("- `99_cierre/manifest.json`: trazabilidad estructurada del run.")
    lines.append("- `99_cierre/validacion_final.json`: resultado determinista de validacion del producto.")
    lines.append("- `99_cierre/review_final.md`: vista humana de la validacion final.")
    lines.append("- `99_cierre/lecciones_aprendidas.md`: cierre documental factual.")
    lines.append("")
    lines.append("## Fases ejecutadas\n")
    for nombre, datos in fases.items():
        lines.append(
            f"- `{nombre}`: gate=`{datos.get('gate_decision')}`, "
            f"auto_retries=`{datos.get('reintentos_automaticos')}`, "
            f"regeneraciones=`{datos.get('regeneraciones_humanas')}`"
        )
    lines.append("")
    lines.append("## Inspeccion del producto\n")
    lines.append("El codigo final generado vive en `06_sprint_3/codigo/`.")
    lines.append(
        "La validacion final se ejecuta sobre una copia temporal en "
        "`99_cierre/_validacion_tmp/codigo/` para no modificar el entregable."
    )
    lines.append("")
    lines.append("## Nota metodologica\n")
    lines.append(
        "Este cierre no corrige codigo generado ni reinterpreta el resultado. "
        "Solo consolida evidencia producida por el Flow."
    )
    return "\n".join(lines)


def render_lecciones_aprendidas(*, state: Any, manifest: dict[str, Any]) -> str:
    """Genera un cierre factual de incidencias y observaciones."""
    validacion = manifest.get("validacion_final") or {}
    incidencias = validacion.get("incidencias") or []
    preparacion = validacion.get("preparacion_manual_requerida") or []
    gates = manifest.get("gates") or []
    lines: list[str] = []
    lines.append("# Lecciones aprendidas del run\n")
    lines.append(f"**Run**: `{manifest.get('run_id', state.run_id)}`\n")
    lines.append("## Resultado observado\n")
    lines.append(f"- Resultado del Flow: `{manifest.get('resultado_final', state.resultado_final)}`")
    if validacion:
        lines.append(f"- OK global de validacion final: `{validacion.get('ok_global')}`")
        lines.append(f"- Clasificacion: `{validacion.get('clasificacion')}`")
        lines.append(f"- Checks ejecutados: `{validacion.get('checks_ejecutados')}/{validacion.get('checks_planificados')}`")
    lines.append("")
    lines.append("## Incidencias de validacion final\n")
    if incidencias:
        for incidencia in incidencias:
            lines.append(f"- {incidencia}")
    else:
        lines.append("- No se registraron incidencias en validacion final.")
    lines.append("")
    lines.append("## Preparacion manual requerida\n")
    if preparacion:
        for item in preparacion:
            lines.append(f"- {item}")
    else:
        lines.append("- No detectada por la validacion final.")
    lines.append("")
    lines.append("## Gates humanos\n")
    if gates:
        for gate in gates:
            meta = gate.get("metadata") or {}
            lines.append(
                f"- `{gate.get('path')}`: gate=`{meta.get('gate')}`, "
                f"fase=`{meta.get('fase')}`, decision=`{meta.get('decision')}`"
            )
    else:
        lines.append("- No se encontraron actas de gate.")
    lines.append("")
    lines.append("## Alcance de estas lecciones\n")
    lines.append(
        "Las metricas externas del estudio, como implementation rate, pass-rate "
        "de suite comun y log estructurado de incidencias, se calculan fuera del "
        "pipeline para no mezclar generacion con evaluacion comparativa."
    )
    return "\n".join(lines)
