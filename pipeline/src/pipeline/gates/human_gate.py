# src/pipeline/gates/human_gate.py
"""
Gate humano del pipeline (Bloque 5 del spec).

Función pura `human_gate(...)`: muestra por consola las rutas de los
artefactos producidos por una fase, espera el handshake del operador
(`ok` / `abort`), lee `gate_humano.md` de la carpeta de la fase, lo
valida y devuelve un `GateResult` con la decisión.

Lo que ESTE módulo NO hace (deliberado, ver subpaso 8b):
  - No actualiza `Caso02State` ni `fases_status`. Eso lo hace el llamante
    (Flow) cuando se integre el gate en 8c.
  - No incrementa `regeneraciones_humanas`. Idem.
  - Solo escribe una plantilla de `gate_humano.md` si no existe. La decision
    final la escribe la operadora.
  - No verifica límites de regeneraciones. El llamante compara
    `regeneraciones_humanas` contra `max_regeneraciones` y decide qué
    hacer con un `decision="rechazado"` que ya excede el presupuesto.

Política (Bloque 5):
  - La operadora NO edita los artefactos producidos por los agentes.
    Las únicas decisiones válidas son aceptar, rechazar (regenerar)
    o abortar.
  - Si decisión = rechazado, la sección `## Acción` debe contener
    instrucciones accionables (input para la regeneración).

Cambio en 8f: el parámetro `artefacto_md` (Path) pasa a ser
`artefactos_md` (list[Path]). El gate 2 evalúa tres artefactos
(backlog, plan_sprints, riesgos) en bloque (decisión metodológica D1).
La firma se generaliza para soportar 1..N artefactos sin asumir
cantidad. Para un solo artefacto (gate 1) basta con pasar `[ruta]`.
"""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional
from zoneinfo import ZoneInfo

import yaml
from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------------

GateDecision = Literal["aceptado", "rechazado", "abortado"]

_DECISIONES_VALIDAS: tuple[GateDecision, ...] = ("aceptado", "rechazado", "abortado")


class GateResult(BaseModel):
    """
    Resultado del gate humano para una fase.

    Diseñado como objeto de retorno: el llamante (Flow en 8c) decide qué
    hacer con él (ramificar, incrementar contadores, escribir manifest).
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    decision: GateDecision
    observaciones: str = ""
    accion: Optional[str] = None
    timestamp_inicio: str
    timestamp_fin: str
    duracion_s: float


class GateError(Exception):
    """Error técnico del gate (no confundir con decisión humana)."""


# ---------------------------------------------------------------------------
# Punto de entrada público
# ---------------------------------------------------------------------------

def human_gate(
    *,
    fase: str,
    fase_dir: Path,
    artefactos_md: list[Path],
    numero_gate: int,
    regeneraciones_consumidas: int,
    max_regeneraciones: int = 3,
) -> GateResult:
    """
    Ejecuta el gate humano para una fase.

    Args:
        fase: nombre de la fase, p.ej. "01_requisitos". Se compara con el
            campo `fase` del frontmatter del MD (warning si discrepa).
        fase_dir: carpeta de la fase dentro del Run. Se espera que el
            operador escriba `gate_humano.md` aquí.
        artefactos_md: lista de rutas absolutas a los MDs producidos por
            la fase, que la operadora debe revisar antes de escribir el
            gate. Solo se imprimen por consola; no se leen. Para gates
            sobre un único artefacto (gate 1, gate 3) se pasa una lista
            de longitud 1. Para el gate 2, se pasan los tres MDs de
            planificación. La lista no puede estar vacía.
        numero_gate: 1, 2 o 3 (Bloque 5 del spec).
        regeneraciones_consumidas: cuántas regeneraciones humanas se han
            consumido ya en esta fase. Solo se imprime para informar a la
            operadora antes de su decisión.
        max_regeneraciones: presupuesto total de regeneraciones humanas
            (por defecto 3, Bloque 5). Solo se imprime.

    Returns:
        GateResult con la decisión del operador y los timestamps del gate.

    Raises:
        GateError: errores técnicos imposibles de recuperar interactivamente
            (p.ej. `fase_dir` inexistente, `artefactos_md` vacía). Los
            errores recuperables — archivo ausente, frontmatter mal
            formado, decisión inválida — se reportan por consola y se
            vuelve a pedir `ok`/`abort`.
    """
    if not fase_dir.is_dir():
        raise GateError(f"fase_dir no existe o no es directorio: {fase_dir}")

    if not artefactos_md:
        raise GateError(
            "artefactos_md está vacía: el gate necesita al menos un "
            "artefacto MD que la operadora pueda revisar."
        )

    gate_md_path = fase_dir / "gate_humano.md"

    _imprimir_header(
        fase=fase,
        artefactos_md=artefactos_md,
        gate_md_path=gate_md_path,
        numero_gate=numero_gate,
        regeneraciones_consumidas=regeneraciones_consumidas,
        max_regeneraciones=max_regeneraciones,
    )

    timestamp_inicio = _now_iso_madrid()
    _crear_plantilla_gate_si_no_existe(
        gate_md_path=gate_md_path,
        fase=fase,
        numero_gate=numero_gate,
        timestamp_inicio=timestamp_inicio,
    )
    t0 = time.monotonic()

    while True:
        respuesta = input(
            "\nCuando hayas escrito gate_humano.md en la carpeta de la fase, "
            "escribe 'ok' para continuar (o 'abort' para abortar el Run): "
        ).strip().lower()

        if respuesta == "abort":
            duracion_s = time.monotonic() - t0
            print("\n[Gate] Abortado por la operadora sin leer gate_humano.md.")
            return GateResult(
                decision="abortado",
                observaciones="",
                accion=None,
                timestamp_inicio=timestamp_inicio,
                timestamp_fin=_now_iso_madrid(),
                duracion_s=duracion_s,
            )

        if respuesta != "ok":
            print("[Gate] Respuesta no reconocida. Escribe 'ok' o 'abort'.")
            continue

        # Handshake recibido: leemos y validamos el MD.
        try:
            decision, observaciones, accion = _leer_y_validar_gate_md(
                gate_md_path=gate_md_path,
                fase_esperada=fase,
                numero_gate_esperado=numero_gate,
            )
        except _ValidacionGateError as e:
            print(f"\n[Gate] Problema con gate_humano.md: {e}")
            print("[Gate] Corrige el archivo y vuelve a escribir 'ok' (o 'abort').")
            continue

        duracion_s = time.monotonic() - t0
        return GateResult(
            decision=decision,
            observaciones=observaciones,
            accion=accion,
            timestamp_inicio=timestamp_inicio,
            timestamp_fin=_now_iso_madrid(),
            duracion_s=duracion_s,
        )


# ---------------------------------------------------------------------------
# Internos
# ---------------------------------------------------------------------------

class _ValidacionGateError(Exception):
    """Validación del gate_humano.md falló de forma recuperable."""


def _imprimir_header(
    *,
    fase: str,
    artefactos_md: list[Path],
    gate_md_path: Path,
    numero_gate: int,
    regeneraciones_consumidas: int,
    max_regeneraciones: int,
) -> None:
    """
    Cabecera del gate por consola.

    Para un único artefacto sale: "Artefacto a revisar: ruta".
    Para varios sale: "Artefactos a revisar (N):" seguido de un bullet
    por archivo. Mantiene la línea simple para el caso común (gate 1 y
    gate 3) y solo se expande para el gate 2.
    """
    print("\n" + "=" * 70)
    print(f"GATE HUMANO {numero_gate} — fase {fase}")
    print("=" * 70)

    if len(artefactos_md) == 1:
        print(f"Artefacto a revisar: {artefactos_md[0]}")
    else:
        print(f"Artefactos a revisar ({len(artefactos_md)}):")
        for ruta in artefactos_md:
            print(f"  - {ruta}")

    print(f"Escribe tu decisión en: {gate_md_path}")
    print(
        f"Regeneraciones consumidas: "
        f"{regeneraciones_consumidas}/{max_regeneraciones}"
    )
    print(
        "Decisiones válidas en gate_humano.md: "
        "aceptado | rechazado | abortado"
    )
    print(
        "Política: si rechazas, la sección '## Acción' debe contener "
        "instrucciones para la regeneración."
    )


def _crear_plantilla_gate_si_no_existe(
    *,
    gate_md_path: Path,
    fase: str,
    numero_gate: int,
    timestamp_inicio: str,
) -> None:
    """
    Crea una plantilla de acta de gate sin sobrescribir decisiones existentes.

    Los timestamps son documentales para auditoria futura; el tiempo oficial
    del gate se calcula con el cronometro interno de `human_gate`.
    """
    if gate_md_path.exists():
        return

    contenido = (
        "---\n"
        f"gate: {numero_gate}\n"
        f"fase: {fase}\n"
        "decision:\n"
        f"timestamp_revision_inicio: {timestamp_inicio}\n"
        "timestamp_revision_fin:\n"
        "---\n\n"
        "## Observaciones\n\n"
        "Revisión formal pendiente.\n\n"
        "## Acción\n\n"
        "\n"
    )
    gate_md_path.write_text(contenido, encoding="utf-8")


def _leer_y_validar_gate_md(
    *,
    gate_md_path: Path,
    fase_esperada: str,
    numero_gate_esperado: int,
) -> tuple[GateDecision, str, Optional[str]]:
    """
    Lee y valida `gate_humano.md`. Devuelve (decision, observaciones, accion).
    Lanza `_ValidacionGateError` si algo no cuadra (recuperable: el llamante
    reimprime el error y vuelve a pedir 'ok'/'abort').
    """
    if not gate_md_path.exists():
        raise _ValidacionGateError(
            f"no se encuentra el archivo en {gate_md_path}."
        )

    contenido = gate_md_path.read_text(encoding="utf-8")
    frontmatter, cuerpo = _split_frontmatter(contenido)
    meta = _parse_yaml_frontmatter(frontmatter)

    decision = _validar_decision(meta)
    _validar_metadatos_gate(
        meta=meta,
        fase_esperada=fase_esperada,
        numero_gate_esperado=numero_gate_esperado,
    )

    observaciones = _extraer_seccion(cuerpo, "Observaciones")
    accion_raw = _extraer_seccion(cuerpo, "Acción")
    accion = accion_raw if accion_raw else None

    if decision == "rechazado" and not accion:
        raise _ValidacionGateError(
            "decisión 'rechazado' requiere sección '## Acción' con "
            "instrucciones no vacías para la regeneración."
        )

    return decision, observaciones, accion


def _split_frontmatter(contenido: str) -> tuple[str, str]:
    """
    Separa el frontmatter YAML del cuerpo Markdown.

    Espera el patrón estándar:

        ---
        clave: valor
        ...
        ---

        cuerpo del MD

    Devuelve (frontmatter_yaml, cuerpo). Si no hay frontmatter, lanza error.
    """
    lineas = contenido.splitlines()
    if not lineas or lineas[0].strip() != "---":
        raise _ValidacionGateError(
            "el archivo no empieza con '---'; falta el frontmatter YAML."
        )

    # Buscamos el segundo '---' que cierra el frontmatter.
    cierre_idx: Optional[int] = None
    for i in range(1, len(lineas)):
        if lineas[i].strip() == "---":
            cierre_idx = i
            break

    if cierre_idx is None:
        raise _ValidacionGateError(
            "no se encuentra el '---' de cierre del frontmatter."
        )

    frontmatter = "\n".join(lineas[1:cierre_idx])
    cuerpo = "\n".join(lineas[cierre_idx + 1 :])
    return frontmatter, cuerpo


def _parse_yaml_frontmatter(frontmatter: str) -> dict:
    try:
        meta = yaml.safe_load(frontmatter) or {}
    except yaml.YAMLError as e:
        raise _ValidacionGateError(f"frontmatter no es YAML válido: {e}")

    if not isinstance(meta, dict):
        raise _ValidacionGateError(
            "el frontmatter debe ser un mapping clave: valor."
        )
    return meta


def _validar_decision(meta: dict) -> GateDecision:
    if "decision" not in meta:
        raise _ValidacionGateError(
            "falta la clave 'decision' en el frontmatter."
        )

    valor = meta["decision"]
    if not isinstance(valor, str):
        raise _ValidacionGateError(
            f"'decision' debe ser un string; recibido: {type(valor).__name__}."
        )

    decision = valor.strip().lower()
    if decision not in _DECISIONES_VALIDAS:
        raise _ValidacionGateError(
            f"'decision' inválida: {valor!r}. "
            f"Valores permitidos: {', '.join(_DECISIONES_VALIDAS)}."
        )
    return decision  # type: ignore[return-value]


def _validar_metadatos_gate(
    *,
    meta: dict,
    fase_esperada: str,
    numero_gate_esperado: int,
) -> None:
    """
    Valida `gate` y `fase` de forma estricta. Los timestamps documentales
    pueden estar presentes en el frontmatter, pero no se usan como fuente
    oficial de tiempo.
    """
    fase_md = meta.get("fase")
    if fase_md is None:
        raise _ValidacionGateError("falta la clave 'fase' en el frontmatter.")
    if str(fase_md).strip() != fase_esperada:
        raise _ValidacionGateError(
            f"'fase' en gate_humano.md = {fase_md!r}, "
            f"se esperaba {fase_esperada!r}."
        )

    gate_md = meta.get("gate")
    if gate_md is None:
        raise _ValidacionGateError("falta la clave 'gate' en el frontmatter.")
    try:
        gate_md_int = int(gate_md)
    except (TypeError, ValueError):
        raise _ValidacionGateError(
            f"'gate' debe ser un entero; recibido: {gate_md!r}."
        )
    if gate_md_int != numero_gate_esperado:
        raise _ValidacionGateError(
            f"'gate' en gate_humano.md = {gate_md_int}, "
            f"se esperaba {numero_gate_esperado}."
        )


def _extraer_seccion(cuerpo: str, titulo: str) -> str:
    """
    Devuelve el texto de la sección `## {titulo}` (sin el encabezado),
    hasta el siguiente encabezado de nivel >= 2 o el final del documento.
    Si la sección no existe, devuelve "".

    Comparación case-insensitive y robusta a espacios. Tolerante a
    encabezados con prefijo extra: '## Acción (solo si rechazado)' cuenta
    como sección 'Acción'.
    """
    lineas = cuerpo.splitlines()
    inicio: Optional[int] = None
    titulo_norm = titulo.strip().lower()

    for i, linea in enumerate(lineas):
        stripped = linea.strip()
        if stripped.startswith("## "):
            cabecera = stripped[3:].strip().lower()
            # Match exacto o que empiece por el título seguido de espacio/paréntesis.
            if cabecera == titulo_norm or cabecera.startswith(titulo_norm + " ") \
               or cabecera.startswith(titulo_norm + "("):
                inicio = i + 1
                break

    if inicio is None:
        return ""

    fin = len(lineas)
    for j in range(inicio, len(lineas)):
        stripped = lineas[j].strip()
        if stripped.startswith("## ") or stripped.startswith("# "):
            fin = j
            break

    return "\n".join(lineas[inicio:fin]).strip()


def _now_iso_madrid() -> str:
    """ISO-8601 con tz Europe/Madrid, mismo criterio que `now_iso_madrid`."""
    return datetime.now(ZoneInfo("Europe/Madrid")).isoformat(timespec="seconds")
