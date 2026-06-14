# src/pipeline/validation/schemas.py
"""
Esquemas Pydantic de los artefactos del pipeline Caso 02 (Hundidos).

Estos modelos definen el contrato ESTRUCTURAL de cada artefacto:
  - Qué campos existen.
  - De qué tipo son.
  - Qué valores cerrados se aceptan (Literal).

NO definen mínimos de cantidad, unicidad de IDs, ni validaciones cruzadas
entre modelos. Esas viven en `validators.py` y se aplican como capa
encima (Bloque 6 del spec, "Nivel 1" vs "Nivel 2").

Razón de la separación: los fallos de esquema y los fallos de contenido
mínimo se contabilizan distinto en la política de reintentos (Bloque 5).
Los primeros son errores técnicos (JSON malformado); los segundos, salidas
del LLM por debajo del listón que podemos regenerar con un prompt ajustado.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Literales / enumeraciones
# ---------------------------------------------------------------------------
# Prioridad (Alta/Media/Baja) se usa en RF, NFR y Backlog.
# Probabilidad e Impacto (minúsculas) se usan en Riesgos — el spec Bloque 6
# los define explícitamente en minúsculas, así que los respetamos literal.

Prioridad = Literal["Alta", "Media", "Baja"]
Probabilidad = Literal["baja", "media", "alta"]
Impacto = Literal["bajo", "medio", "alto"]


# ---------------------------------------------------------------------------
# Base común
# ---------------------------------------------------------------------------

class _StrictModel(BaseModel):
    """
    Base Pydantic con configuración estricta y común:
      - `extra='forbid'`: rechaza campos extra que el LLM añada por su cuenta.
        Preferimos romper explícito a tragar basura silenciosamente.
      - `str_strip_whitespace=True`: normaliza espacios en strings.
      - `validate_assignment=True`: si algo muta el modelo después de crearlo,
        valida de nuevo (útil cuando inyectamos `id_ejecucion` a posteriori).
    """
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


# ===========================================================================
# 01 — Registro de requisitos (Analista)
# ===========================================================================

class RequisitoFuncional(_StrictModel):
    id: str = Field(..., description="Identificador único del RF, p.ej. 'RF-01'.")
    descripcion: str = Field(..., description="Qué debe hacer el sistema, en 1-3 frases.")
    prioridad: Prioridad


class RequisitoNoFuncional(_StrictModel):
    id: str = Field(..., description="Identificador único del RNF, p.ej. 'RNF-01'.")
    categoria: str = Field(
        ...,
        description="Categoría del requisito (p.ej. 'Seguridad', 'Rendimiento', 'Usabilidad').",
    )
    condicion_metrica: str = Field(
        ...,
        description="Condición o métrica verificable (p.ej. 'la página principal carga en <2s').",
    )
    prioridad: Prioridad


class RegistroRequisitos(_StrictModel):
    """Artefacto de la fase 01, producido por el agente Analista."""
    id_ejecucion: str = Field(..., description="Run ID, inyectado por el Flow.")
    requisitos_funcionales: List[RequisitoFuncional]
    requisitos_no_funcionales: List[RequisitoNoFuncional]


# ===========================================================================
# 02 — Backlog (PM)
# ===========================================================================

class HistoriaUsuario(_StrictModel):
    id: str = Field(..., description="Identificador único de la historia, p.ej. 'HU-01'.")
    titulo: str = Field(..., description="Título corto y accionable.")
    descripcion: str = Field(
        ...,
        description="Narrativa de la historia en formato 'Como X, quiero Y, para Z' o equivalente.",
    )
    criterios_aceptacion: List[str] = Field(
        ...,
        description="Lista no vacía de criterios verificables.",
    )
    prioridad: Prioridad
    estimacion: str = Field(
        ...,
        description=(
            "Estimación de esfuerzo como texto libre (p.ej. 'S', 'M', 'L', "
            "'3 puntos', '2 días'). Dejamos string porque el spec no fija unidades."
        ),
    )


class Backlog(_StrictModel):
    """Artefacto de la fase 02 (parte 1), producido por el agente PM."""
    id_ejecucion: str
    historias: List[HistoriaUsuario]


# ===========================================================================
# 04-06 — Backlog derivado por sprint (script determinista)
# ===========================================================================

class BacklogSprint(_StrictModel):
    """
    Backlog filtrado de un sprint concreto.

    No lo produce un LLM: se deriva de forma determinista desde `Backlog` y
    `PlanSprints` ya aceptados. Se guarda para que el Desarrollador reciba
    solo las historias que corresponden al sprint activo.
    """
    id_ejecucion: str
    numero_sprint: int = Field(..., description="Número de sprint (1, 2 o 3).")
    historias: List[HistoriaUsuario]


# ===========================================================================
# 02 — Plan de sprints (PM)
# ===========================================================================

class Sprint(_StrictModel):
    numero: int = Field(..., description="Número de sprint (1, 2, 3).")
    objetivo: str = Field(..., description="Objetivo del sprint en 1-2 frases.")
    historias_ids: List[str] = Field(
        ...,
        description="IDs de las historias del backlog asignadas a este sprint.",
    )
    entregable_verificable: str = Field(
        ...,
        description="Qué se puede demostrar al cierre del sprint.",
    )


class PlanSprints(_StrictModel):
    """Artefacto de la fase 02 (parte 2), producido por el agente PM."""
    id_ejecucion: str
    sprints: List[Sprint]


# ===========================================================================
# 02 — Riesgos (PM)
# ===========================================================================

class Riesgo(_StrictModel):
    id: str = Field(..., description="Identificador único del riesgo, p.ej. 'R-01'.")
    descripcion: str = Field(..., description="Riesgo descrito en 1-2 frases.")
    probabilidad: Probabilidad
    impacto: Impacto
    mitigacion: str = Field(
        ...,
        description="Acción concreta para mitigar o responder al riesgo.",
    )


class Riesgos(_StrictModel):
    """Artefacto de la fase 02 (parte 3), producido por el agente PM."""
    id_ejecucion: str
    riesgos: List[Riesgo]


# ===========================================================================
# 03 — Diseño técnico (Arquitecto)
# ===========================================================================
# Definido aquí para que el Arquitecto tenga su contrato listo cuando
# lleguemos a su crew. No se usa en la crew de Requisitos (la del PMV).

class AppDjango(_StrictModel):
    nombre: str = Field(..., description="Nombre de la app Django, p.ej. 'catalog'.")
    proposito: str = Field(..., description="Responsabilidad de la app, en 1-2 frases.")
    archivos_principales: List[str] = Field(
        ...,
        description="Rutas relativas de los archivos clave (models.py, views.py, etc.).",
    )


class ModeloDjango(_StrictModel):
    nombre: str = Field(..., description="Nombre del modelo, p.ej. 'Boat'.")
    app: str = Field(..., description="App Django a la que pertenece.")
    campos: List[str] = Field(
        ...,
        description=(
            "Campos del modelo como lista de strings simples, "
            "p.ej. 'name:CharField(120)', 'price_per_day:DecimalField'."
        ),
    )


class Ruta(_StrictModel):
    path: str = Field(..., description="Ruta URL, p.ej. '/boats/<int:id>/'.")
    name: str = Field(..., description="Nombre de URL, p.ej. 'boats:detail'.")
    metodo: str = Field(..., description="GET, POST o combinación con '|'.")
    auth: str = Field(
        ...,
        description="'public' o 'login_required' o 'admin_required'.",
    )
    vista: str = Field(..., description="Vista que la sirve, p.ej. 'BoatDetailView'.")


class DisenoTecnico(_StrictModel):
    """Artefacto de la fase 03, producido por el agente Arquitecto."""
    id_ejecucion: str
    stack: List[str] = Field(
        ...,
        description=(
            "Bullets del stack técnico. DEBE mencionar explícitamente "
            "Django 3.2, SQLite y PayPal (spec Bloque 6)."
        ),
    )
    apps_django: List[AppDjango]
    modelos: List[ModeloDjango]
    rutas: List[Ruta]


# ===========================================================================
# 04-06 — Entrega de sprint (Desarrollador)
# ===========================================================================

class ArchivoCodigo(_StrictModel):
    """
    Archivo propuesto por el Desarrollador.

    `path` siempre es relativo a la carpeta `codigo/` del sprint activo.
    El Flow será quien escriba físicamente el archivo en disco, después de
    validar que la ruta no sale del workspace del Run.
    """
    path: str = Field(
        ...,
        description=(
            "Ruta relativa dentro de codigo/, p.ej. 'manage.py', "
            "'hundidos/settings.py' o 'catalog/models.py'."
        ),
    )
    contenido: str = Field(
        ...,
        description="Contenido completo del archivo de código.",
    )


class EntregaSprint(_StrictModel):
    """
    Artefacto de salida del Desarrollador para un sprint.

    No representa el estado completo del directorio en disco, sino los
    archivos que el modelo propone crear o sobrescribir en el sprint activo.
    """
    id_ejecucion: str
    numero_sprint: int = Field(..., description="Número de sprint (1, 2 o 3).")
    archivos: List[ArchivoCodigo]


# ===========================================================================
# 04-06 — Review automático de sprint (script determinista)
# ===========================================================================

EstadoCumplimiento = Literal["ok", "parcial", "ausente"]


class ArranqueResult(_StrictModel):
    """
    Resultado de ejecutar `python manage.py check` sobre la carpeta codigo/.
    """
    ok: bool
    returncode: int
    stdout_resumen: str
    stderr_resumen: str
    timeout_s: int
    timeout: bool = False


class ResultadoReviewRuta(_StrictModel):
    """
    Smoke test HTTP incremental de una ruta visible hasta el sprint activo.
    """
    path: str
    ejecutado: bool
    ok: bool
    status_code: Optional[int] = None
    final_url: str = ""
    error: str = ""
    detalle: str = ""
    motivo_no_ejecutado: str = ""


class ResultadoReviewTemplate(_StrictModel):
    """
    Comprobacion sintactica de template Django durante review de sprint.
    """
    template: str
    ejecutado: bool
    ok: bool
    error: str = ""
    motivo_no_ejecutado: str = ""


class ReviewSprint(_StrictModel):
    """
    Review automático y factual de un sprint.

    `cumplimiento` mapea cada historia pedida por ID a:
      - ok: hay señales claras en archivos/path/contenido.
      - parcial: hay alguna señal, pero débil.
      - ausente: no se detectan señales de implementación.
    """
    id_ejecucion: str
    sprint: int
    backlog_items_pedidos: List[str]
    archivos_entregados: List[str]
    cumplimiento: Dict[str, EstadoCumplimiento]
    arranque: ArranqueResult
    rutas: List[ResultadoReviewRuta] = Field(default_factory=list)
    templates: List[ResultadoReviewTemplate] = Field(default_factory=list)
    incidencias: List[str] = Field(default_factory=list)


# ===========================================================================
# 99 — Validacion final del producto (script determinista)
# ===========================================================================

ClasificacionValidacionFinal = Literal[
    "apto_para_revision_funcional",
    "parcial_con_incidencias",
    "bloqueado_arranque",
    "fallo_entorno_validacion",
]


class ResultadoComando(_StrictModel):
    """
    Resultado factual de ejecutar un comando acotado por timeout.

    `ejecutado=False` permite registrar checks planificados que no pudieron
    correr por un bloqueo anterior sin perder trazabilidad.
    """
    nombre: str
    comando: List[str]
    ejecutado: bool
    ok: bool
    returncode: Optional[int] = None
    stdout_resumen: str = ""
    stderr_resumen: str = ""
    timeout_s: int
    timeout: bool = False
    motivo_no_ejecutado: str = ""


class ResultadoMigraciones(_StrictModel):
    """
    Resultado de la inspeccion estatica de migraciones propias.
    """
    ok: bool
    apps_con_modelos: List[str]
    apps_con_migraciones: List[str]
    apps_sin_migraciones: List[str]


class ResultadoRuta(_StrictModel):
    """
    Resultado de una comprobacion HTTP minima contra una ruta.
    """
    path: str
    ejecutado: bool
    ok: bool
    status_code: Optional[int] = None
    final_url: str = ""
    error: str = ""
    motivo_no_ejecutado: str = ""


class ResultadoTemplate(_StrictModel):
    """
    Resultado de renderizar una plantilla critica de forma controlada.
    """
    template: str
    ejecutado: bool
    ok: bool
    error: str = ""
    motivo_no_ejecutado: str = ""


class ReviewFinal(_StrictModel):
    """
    Resumen comparable entre runs oficiales.

    Permite contar despues, de forma determinista, en cuantos runs se ejecuto
    cada comprobacion y si los fallos vienen del producto generado, del entorno
    de validacion o de una condicion previa no satisfecha.
    """
    protocolo_validacion: str
    checks_planificados: List[str]
    checks_ejecutados: List[str]
    checks_no_ejecutados: Dict[str, str]
    incidencias: List[str]
    factores_bloqueantes: List[str]
    clasificacion: ClasificacionValidacionFinal


class ValidacionFinal(_StrictModel):
    """
    Artefacto final de verificacion minima del producto generado.

    No corrige el producto. Registra evidencia factual para comparar runs.
    """
    id_ejecucion: str
    codigo_dir: str
    copia_validacion_dir: str
    ok_global: bool
    check: ResultadoComando
    migraciones: ResultadoMigraciones
    migrate: ResultadoComando
    seed_data: ResultadoComando
    runserver: ResultadoComando
    rutas: List[ResultadoRuta]
    templates: List[ResultadoTemplate]
    preparacion_manual_requerida: List[str]
    observaciones: List[str]
    review_final: ReviewFinal
