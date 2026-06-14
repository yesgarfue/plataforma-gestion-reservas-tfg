# src/pipeline/validation/validators.py
"""
Validadores deterministas de contenido mínimo (Bloque 6 del spec, Nivel 2).

Estas funciones se aplican DESPUÉS de la validación Pydantic. Reciben un
modelo ya estructuralmente válido y deciden si el contenido cumple el
listón de calidad mínima que el spec congeló.

  - Si todo cumple → la función devuelve `None` (no hace nada).
  - Si algo no cumple → lanza `ContenidoInsuficienteError` con un mensaje
    accionable que puede inyectarse en el prompt de regeneración.

Por qué excepción propia (no `ValueError`):
    Queremos distinguir dos tipos de fallo en el runner de la crew:
      - Fallo de esquema (Pydantic): el LLM emitió JSON malformado o le
        faltan campos. El arreglo es volver a llamar al LLM, quizá
        reparando el JSON primero.
      - Fallo de contenido (esta capa): el LLM emitió JSON válido pero
        por debajo del listón. El arreglo es una regeneración con prompt
        ajustado ("devolviste 12 requisitos, necesito al menos 15").
    La política de reintentos puede diferir.

Los mínimos numéricos viven como constantes al inicio del módulo para
facilitar su ajuste si las primeras ejecuciones lo exigen (regla de
ajuste documentada en la nota final del Bloque 6).
"""

from __future__ import annotations

import re
from collections import Counter
from typing import List

from .schemas import (
    Backlog,
    DisenoTecnico,
    EntregaSprint,
    PlanSprints,
    RegistroRequisitos,
    Riesgos,
)


# ---------------------------------------------------------------------------
# Excepción
# ---------------------------------------------------------------------------

class ContenidoInsuficienteError(Exception):
    """
    El artefacto es estructuralmente válido pero el contenido está por
    debajo del listón mínimo del Bloque 6 del spec. El mensaje describe
    qué falta, en términos accionables para que un prompt de regeneración
    pueda incluirlo sin reformulación humana.
    """


# ---------------------------------------------------------------------------
# Mínimos (Bloque 6 del spec).
#
# Cualquier cambio aquí se documenta en pipeline_bitacora.md y activa una
# nueva congelación del spec (regla de ajuste del Bloque 6).
# ---------------------------------------------------------------------------

MIN_REQUISITOS_FUNCIONALES = 15
MIN_REQUISITOS_NO_FUNCIONALES = 3

MIN_HISTORIAS_BACKLOG = 11

NUM_SPRINTS_EXACTO = 3

MIN_RIESGOS = 5

STACK_KEYWORDS_OBLIGATORIAS = ("Django 3.2", "SQLite", "PayPal")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ids_duplicados(ids: List[str]) -> List[str]:
    """Devuelve la lista de IDs que aparecen más de una vez (cada uno una vez)."""
    counter = Counter(ids)
    return sorted([i for i, c in counter.items() if c > 1])


# ---------------------------------------------------------------------------
# 01 — Requisitos
# ---------------------------------------------------------------------------

def validate_requisitos_contenido(registro: RegistroRequisitos) -> None:
    """Valida el contenido mínimo de un `RegistroRequisitos`."""
    errors: List[str] = []

    n_fr = len(registro.requisitos_funcionales)
    n_nfr = len(registro.requisitos_no_funcionales)

    if n_fr < MIN_REQUISITOS_FUNCIONALES:
        errors.append(
            f"Hay {n_fr} requisitos funcionales; el mínimo es "
            f"{MIN_REQUISITOS_FUNCIONALES}. Añade "
            f"{MIN_REQUISITOS_FUNCIONALES - n_fr} más."
        )

    if n_nfr < MIN_REQUISITOS_NO_FUNCIONALES:
        errors.append(
            f"Hay {n_nfr} requisitos no funcionales; el mínimo es "
            f"{MIN_REQUISITOS_NO_FUNCIONALES}. Añade "
            f"{MIN_REQUISITOS_NO_FUNCIONALES - n_nfr} más."
        )

    dup_fr = _ids_duplicados([r.id for r in registro.requisitos_funcionales])
    if dup_fr:
        errors.append(f"IDs duplicados en requisitos funcionales: {dup_fr}.")

    dup_nfr = _ids_duplicados([r.id for r in registro.requisitos_no_funcionales])
    if dup_nfr:
        errors.append(f"IDs duplicados en requisitos no funcionales: {dup_nfr}.")

    if errors:
        raise ContenidoInsuficienteError(
            "RegistroRequisitos: " + " ".join(errors)
        )


# ---------------------------------------------------------------------------
# 02 — Backlog
# ---------------------------------------------------------------------------

def validate_backlog_contenido(backlog: Backlog) -> None:
    """Valida el contenido mínimo de un `Backlog`."""
    errors: List[str] = []

    n = len(backlog.historias)
    if n < MIN_HISTORIAS_BACKLOG:
        errors.append(
            f"Hay {n} historias; el mínimo es {MIN_HISTORIAS_BACKLOG}. "
            f"Añade {MIN_HISTORIAS_BACKLOG - n} más."
        )

    dup = _ids_duplicados([h.id for h in backlog.historias])
    if dup:
        errors.append(f"IDs duplicados en historias: {dup}.")

    # Pydantic acepta `criterios_aceptacion: []` a nivel de esquema.
    # Aquí exigimos que cada historia tenga al menos un criterio.
    sin_criterios = [h.id for h in backlog.historias if not h.criterios_aceptacion]
    if sin_criterios:
        errors.append(
            f"Historias sin criterios de aceptación: {sin_criterios}. "
            "Cada historia debe tener al menos uno."
        )

    if errors:
        raise ContenidoInsuficienteError("Backlog: " + " ".join(errors))


# ---------------------------------------------------------------------------
# 02 — Plan de sprints
# ---------------------------------------------------------------------------

def validate_plan_sprints_contenido(plan: PlanSprints, backlog: Backlog) -> None:
    """
    Valida el contenido mínimo de un `PlanSprints` contra un `Backlog` dado.

    Reglas (Bloque 6 del spec):
      - Exactamente 3 sprints.
      - Numerados 1, 2, 3 sin huecos ni duplicados.
      - La unión de `historias_ids` cubre todos los IDs del backlog.
      - Ninguna historia asignada a dos sprints (interpretación estricta
        de 'cobertura': una historia por sprint).
      - Todos los `historias_ids` referencian historias existentes en el
        backlog (no IDs inventados).
    """
    errors: List[str] = []

    # Cantidad exacta de sprints
    n_sprints = len(plan.sprints)
    if n_sprints != NUM_SPRINTS_EXACTO:
        errors.append(
            f"Hay {n_sprints} sprints; deben ser exactamente {NUM_SPRINTS_EXACTO}."
        )

    # Numeración 1..N sin huecos ni duplicados (solo si la cantidad es correcta)
    if n_sprints == NUM_SPRINTS_EXACTO:
        numeros = sorted(s.numero for s in plan.sprints)
        esperados = list(range(1, NUM_SPRINTS_EXACTO + 1))
        if numeros != esperados:
            errors.append(
                f"Los sprints deben estar numerados {esperados}; se recibió {numeros}."
            )

    # Unión de IDs del plan vs IDs del backlog
    ids_backlog = {h.id for h in backlog.historias}
    ids_plan_flat: List[str] = []
    for s in plan.sprints:
        ids_plan_flat.extend(s.historias_ids)

    # Duplicados entre sprints (una historia aparece en dos sprints)
    dup_entre_sprints = _ids_duplicados(ids_plan_flat)
    if dup_entre_sprints:
        errors.append(
            f"Historias asignadas a más de un sprint: {dup_entre_sprints}. "
            "Cada historia debe estar en exactamente un sprint."
        )

    # IDs del plan que no existen en el backlog
    ids_plan_set = set(ids_plan_flat)
    ids_inventados = sorted(ids_plan_set - ids_backlog)
    if ids_inventados:
        errors.append(
            f"El plan referencia historias inexistentes en el backlog: "
            f"{ids_inventados}."
        )

    # IDs del backlog no cubiertos por ningún sprint
    ids_sin_asignar = sorted(ids_backlog - ids_plan_set)
    if ids_sin_asignar:
        errors.append(
            f"Historias del backlog sin asignar a ningún sprint: {ids_sin_asignar}."
        )

    if errors:
        raise ContenidoInsuficienteError("PlanSprints: " + " ".join(errors))


# ---------------------------------------------------------------------------
# 02 — Riesgos
# ---------------------------------------------------------------------------

def validate_riesgos_contenido(riesgos: Riesgos) -> None:
    """Valida el contenido mínimo de un `Riesgos`."""
    errors: List[str] = []

    n = len(riesgos.riesgos)
    if n < MIN_RIESGOS:
        errors.append(
            f"Hay {n} riesgos; el mínimo es {MIN_RIESGOS}. "
            f"Añade {MIN_RIESGOS - n} más."
        )

    dup = _ids_duplicados([r.id for r in riesgos.riesgos])
    if dup:
        errors.append(f"IDs duplicados en riesgos: {dup}.")

    if errors:
        raise ContenidoInsuficienteError("Riesgos: " + " ".join(errors))


# ---------------------------------------------------------------------------
# 03 — Diseño técnico
# ---------------------------------------------------------------------------

def validate_diseno_tecnico_contenido(diseno: DisenoTecnico) -> None:
    """
    Valida el contenido mínimo de un `DisenoTecnico`.

    Regla (Bloque 6 del spec): el campo `stack` debe mencionar
    explícitamente Django 3.2, SQLite y PayPal. La comparación se hace
    sobre el join concatenado de todos los bullets del stack, sin
    distinguir mayúsculas/minúsculas.
    """
    errors: List[str] = []

    stack_join = " ".join(diseno.stack).lower()
    faltan = [
        kw for kw in STACK_KEYWORDS_OBLIGATORIAS
        if kw.lower() not in stack_join
    ]
    if faltan:
        errors.append(
            f"El campo 'stack' no menciona: {faltan}. "
            "El spec exige mención explícita de Django 3.2, SQLite y PayPal."
        )

    if errors:
        raise ContenidoInsuficienteError("DisenoTecnico: " + " ".join(errors))


# ---------------------------------------------------------------------------
# 04-06 — Entrega de sprint
# ---------------------------------------------------------------------------

def validate_entrega_sprint_contenido(
    entrega: EntregaSprint,
    *,
    require_base_django: bool | None = None,
) -> None:
    """
    Valida el contenido mínimo de una `EntregaSprint`.

    Esta validación es intencionadamente ligera: no juzga si el producto
    cumple el backlog ni si Django arranca. Eso corresponde al review
    determinista y a `manage.py check` en subpasos posteriores.
    """
    errors: List[str] = []

    if require_base_django is None:
        require_base_django = entrega.numero_sprint in (0, 1)

    if entrega.numero_sprint not in (0, 1, 2, 3):
        errors.append(
            f"numero_sprint debe ser 0, 1, 2 o 3; se recibió {entrega.numero_sprint}."
        )

    if not entrega.archivos:
        errors.append("La entrega no contiene archivos.")

    paths = [archivo.path for archivo in entrega.archivos]
    duplicados = _ids_duplicados(paths)
    if duplicados:
        errors.append(f"Archivos duplicados en la entrega: {duplicados}.")

    rutas_invalidas: List[str] = []
    for path in paths:
        path_normalizado = path.replace("\\", "/").strip()
        if (
            not path_normalizado
            or path_normalizado.startswith("/")
            or path_normalizado.startswith("../")
            or "/../" in path_normalizado
            or path_normalizado == ".."
            or ":" in path_normalizado.split("/", 1)[0]
        ):
            rutas_invalidas.append(path)
    if rutas_invalidas:
        errors.append(
            "Hay rutas inválidas o fuera de codigo/: "
            f"{sorted(rutas_invalidas)}."
        )

    archivos_vacios = [
        archivo.path
        for archivo in entrega.archivos
        if (
            not archivo.contenido.strip()
            and not archivo.path.replace("\\", "/").endswith(("__init__.py", ".gitkeep"))
        )
    ]
    if archivos_vacios:
        errors.append(f"Archivos sin contenido: {sorted(archivos_vacios)}.")

    paths_lower = [path.replace("\\", "/").lower() for path in paths]
    if require_base_django and not any(path == "manage.py" for path in paths_lower):
        errors.append("La entrega del sprint 1 debe incluir manage.py.")

    if require_base_django and not any(path.endswith("/settings.py") for path in paths_lower):
        errors.append("La entrega del sprint 1 debe incluir un settings.py de proyecto Django.")

    if require_base_django and not any(
        path == "urls.py" or path.endswith("/urls.py")
        for path in paths_lower
    ):
        errors.append("La entrega del sprint 1 debe incluir un urls.py raíz o de proyecto.")

    if require_base_django:
        includes_sin_modulo = _includes_urls_sin_archivo(entrega)
        if includes_sin_modulo:
            errors.append(
                "Hay includes Django a modulos urls inexistentes: "
                f"{includes_sin_modulo}."
            )

    if errors:
        raise ContenidoInsuficienteError("EntregaSprint: " + " ".join(errors))


def _includes_urls_sin_archivo(entrega: EntregaSprint) -> List[str]:
    """Detecta include('app.urls') sin el archivo app/urls.py correspondiente."""
    paths = {
        archivo.path.replace("\\", "/").strip().lower()
        for archivo in entrega.archivos
    }
    faltantes: List[str] = []
    patron = re.compile(r"include\(\s*['\"]([a-zA-Z_][\w]*)\.urls['\"]")
    for archivo in entrega.archivos:
        path = archivo.path.replace("\\", "/").strip().lower()
        if not (path == "urls.py" or path.endswith("/urls.py")):
            continue
        for app_name in patron.findall(archivo.contenido):
            app_urls = f"{app_name.lower()}/urls.py"
            if app_urls not in paths:
                faltantes.append(app_urls)
    return sorted(set(faltantes))
