# src/pipeline/main.py
"""
Flow principal del pipeline Caso 02 (Hundidos).

VERSIÓN 1a — Fases 01, 02 y 03 con sus gates humanos.

Pasos del Flow:

    setup_run                 (@start)
        └─► ejecutar_fase_01_requisitos
                └─► ejecutar_fase_02_planificacion
                        └─► ejecutar_fase_03_arquitectura
                                └─► cerrar_run

`ejecutar_fase_01_requisitos`, `ejecutar_fase_02_planificacion` y
`ejecutar_fase_03_arquitectura` delegan en helpers privados
(`_kickoff_*_con_gate_humano`) que envuelven los reintentos automáticos
(Bloque 6) y las regeneraciones humanas (Bloque 5) en un único bucle
por fase. La estrategia de orquestación es
"early-return + flag en state", coherente con 8a/8c: el grafo del Flow
no expone los bucles, quedan encapsulados en los métodos de fase.

Decisión D.1 (cerrada en 8f): ninguna fase intermedia marca
`state.resultado_final = "completo"` cuando acepta su gate; solo se
marca `gate_decision = "aceptado"` y se deja `resultado_final` en
"pendiente". `cerrar_run` promueve "pendiente" a "completo" si llega al
cierre sin que ninguna fase haya marcado un estado terminal
(abortado_*, bloqueado_*).

Si cualquier fase falla o aborta, marca state.resultado_final con el
motivo y las fases siguientes hacen no-op; `cerrar_run` igualmente
escribe el run_summary.json para preservar trazabilidad.

Ejecución:
    crewai run
    python -m pipeline.main
"""

from __future__ import annotations

import sys
import shutil
import time
import traceback
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

from crewai.flow.flow import Flow, listen, start

from pipeline.closer.closer import render_lecciones_aprendidas, render_readme_cierre
from pipeline.crews.arquitectura_crew.arquitectura_crew import ArquitecturaCrew
from pipeline.crews.desarrollo_crew.desarrollo_crew import DesarrolloCrew
from pipeline.crews.planificacion_crew.planificacion_crew import PlanificacionCrew
from pipeline.crews.requisitos_crew.requisitos_crew import RequisitosCrew
from pipeline.gates.human_gate import GateError, GateResult, human_gate
from pipeline.state import Caso02State, FaseStatus, build_run_paths
from pipeline.utils.django_runner import ejecutar_manage_check
from pipeline.utils.final_validator import construir_validacion_final
from pipeline.utils.manifest import construir_manifest
from pipeline.utils.llm_factory import get_model_name
from pipeline.utils.io_utils import (
    ensure_dir,
    now_iso_madrid,
    sha256_file,
    write_json,
    write_text,
)
from pipeline.utils.renderers import (
    render_backlog_md,
    render_backlog_sprint_md,
    render_diseno_tecnico_md,
    render_frontmatter,
    render_plan_sprints_md,
    render_requisitos_md,
    render_review_final_md,
    render_review_sprint_md,
    render_riesgos_md,
)
from pipeline.utils.review_builder import construir_review_sprint, listar_archivos_codigo
from pipeline.utils.sprint_backlog_builder import derivar_sprint_backlogs
from pipeline.validation.schemas import (
    Backlog,
    BacklogSprint,
    DisenoTecnico,
    EntregaSprint,
    PlanSprints,
    RegistroRequisitos,
    ReviewSprint,
    Riesgos,
)
from pipeline.validation.validators import (
    ContenidoInsuficienteError,
    validate_backlog_contenido,
    validate_diseno_tecnico_contenido,
    validate_entrega_sprint_contenido,
    validate_plan_sprints_contenido,
    validate_requisitos_contenido,
    validate_riesgos_contenido,
)


# ---------------------------------------------------------------------------
# Rutas estándar del proyecto
# ---------------------------------------------------------------------------
# __file__ = .../src/pipeline/main.py
# parents[2] = raíz del proyecto (donde vive brief/, pipeline_specs.md, etc.)

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_BRIEF_PATH = _PROJECT_ROOT / "brief" / "brief.md"
_RUNS_DIR = _PROJECT_ROOT / "runs"
_PIPELINE_SPECS_PATH = _PROJECT_ROOT / "pipeline_specs.md"
_PIPELINE_CONFIG_PATH = _PROJECT_ROOT / "src" / "pipeline" / "config" / "pipeline_config.yaml"

# Nombre de la fase, usado como clave en fases_status y en rutas.
_FASE_01 = "01_requisitos"
_FASE_02 = "02_planificacion"
_FASE_03 = "03_arquitectura"
_FASE_03B = "03b_scaffold"
_FASE_04 = "04_sprint_1"
_FASE_05 = "05_sprint_2"
_FASE_06 = "06_sprint_3"
_FASE_99 = "99_cierre"

# Política de reintentos automáticos (Bloque 6 del spec). Misma para
# todas las fases del PMV.
# Se aplica POR REGENERACIÓN HUMANA: cada regeneración consume hasta
# `_MAX_REINTENTOS` automáticos, y los contadores se resetean al inicio
# de la siguiente regeneración (Bloque 5: "los dos son independientes y
# acumulables, hasta 12 generaciones en el peor caso").
_MAX_REINTENTOS = 3
_RATE_LIMIT_BACKOFF_S = 90


def _es_error_rate_limit(error: Exception) -> bool:
    """Detecta errores 429/rate limit de proveedores LLM sin acoplarse a SDK."""
    texto = f"{type(error).__name__}: {error}".lower()
    return (
        "ratelimit" in texto
        or "rate_limit" in texto
        or "rate limit" in texto
        or "error code: 429" in texto
    )


def _retry_after_s(error: Exception) -> int:
    """
    Extrae `retry-after` si el SDK lo expone; si no, usa una ventana segura.

    Los proveedores LLM aplican limites por ventanas temporales. Reintentar
    inmediatamente ante 429 consume el presupuesto de reintentos sin cambiar
    la condicion que causo el fallo.
    """
    headers = getattr(getattr(error, "response", None), "headers", None)
    if headers is not None:
        try:
            retry_after = headers.get("retry-after")
            if retry_after is not None:
                return max(1, int(float(retry_after)))
        except Exception:
            pass
    return _RATE_LIMIT_BACKOFF_S


def _leer_max_regeneraciones_humanas() -> int:
    """
    Lee `retries.human_regenerations` de pipeline_config.yaml.

    Se hace en runtime (no como constante) para que el config sea la
    única fuente de verdad: si la operadora cambia el valor, el cambio
    queda registrado en el hash del config y se respeta sin tocar código.
    """
    try:
        with _PIPELINE_CONFIG_PATH.open(encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return int(cfg["retries"]["human_regenerations"])
    except Exception:
        # Si el config falla, caemos al default del spec (Bloque 5: 3).
        # Deliberado: no queremos que un YAML malformado aborte el Run
        # antes incluso de empezar; eso se diagnostica con prints.
        print("[CONFIG] No se pudo leer retries.human_regenerations; "
              "usando default=3.")
        return 3


def _leer_timeout_django_check() -> int:
    """Lee `timeouts.django_check_s` de pipeline_config.yaml."""
    try:
        with _PIPELINE_CONFIG_PATH.open(encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return int(cfg["timeouts"]["django_check_s"])
    except Exception:
        print("[CONFIG] No se pudo leer timeouts.django_check_s; "
              "usando default=60.")
        return 60


# ===========================================================================
# Flow principal
# ===========================================================================

class Caso02Flow(Flow[Caso02State]):
    """
    Flow del Caso 02 (Hundidos).

    Orquesta las fases 01, 02 y 03 con sus gates humanos. Los bucles de
    reintentos automáticos y regeneraciones humanas viven dentro de cada
    helper de fase; el grafo del Flow mantiene solo los hitos principales.
    """

    # -----------------------------------------------------------------------
    # Paso 1 — Setup del Run
    # -----------------------------------------------------------------------

    @start()
    def setup_run(self) -> None:
        """
        Inicializa el state del Run: run_id, paths, brief en memoria,
        hashes de archivos globales. Crea las carpetas del Run en disco.

        Si algo falla aquí, marca resultado_final = 'bloqueado_arranque'
        y deja que el Flow continúe a cerrar_run para producir un
        run_summary.json del fallo en lugar de un traceback colgado.
        """
        print("=" * 70)
        print("Pipeline Caso 02 - Hundidos - Fases 01-03 + Gates (Flow)")
        print("=" * 70)

        try:
            self.state.run_id = _build_run_id()
            self.state.paths = build_run_paths(_RUNS_DIR, self.state.run_id)

            ensure_dir(self.state.paths.root)
            ensure_dir(self.state.paths.fase_01_requisitos)
            ensure_dir(self.state.paths.fase_02_planificacion)
            ensure_dir(self.state.paths.fase_03_arquitectura)
            ensure_dir(self.state.paths.fase_03b_scaffold)
            ensure_dir(self.state.paths.fase_04_sprint_1)
            ensure_dir(self.state.paths.fase_05_sprint_2)
            ensure_dir(self.state.paths.fase_06_sprint_3)
            ensure_dir(self.state.paths.fase_99_cierre)
            ensure_dir(self.state.paths.logs)
            ensure_dir(self.state.paths.attempts)

            if not _BRIEF_PATH.exists():
                raise FileNotFoundError(
                    f"No se encuentra el brief en {_BRIEF_PATH}. "
                    "Verifica que 'brief/brief.md' existe en la raíz del proyecto."
                )
            self.state.brief_texto = _BRIEF_PATH.read_text(encoding="utf-8")

            # Hashes de archivos globales (los hashes por crew-yaml vendrán
            # con el manifest completo en una iteración posterior).
            self.state.hashes.brief = sha256_file(_BRIEF_PATH)
            self.state.hashes.pipeline_specs = sha256_file(_PIPELINE_SPECS_PATH)
            self.state.hashes.pipeline_config = sha256_file(_PIPELINE_CONFIG_PATH)
        except Exception as e:
            print(f"\n[SETUP] Fallo al preparar el Run: {e}")
            traceback.print_exc()
            self.state.resultado_final = "bloqueado_arranque"
            return

        print(f"\nrun_id: {self.state.run_id}")
        assert self.state.paths is not None
        print(f"Run folder: {self.state.paths.root}")
        print(
            f"Brief: {len(self.state.brief_texto)} caracteres, "
            f"hash {self.state.hashes.brief[:16]}..."
        )

    # -----------------------------------------------------------------------
    # Paso 2 — Fase 01: Requisitos + Gate 1
    # -----------------------------------------------------------------------

    @listen(setup_run)
    def ejecutar_fase_01_requisitos(self) -> None:
        """
        Ejecuta la fase 01 con su gate humano.

        Si setup_run falló, este paso es no-op: detecta el resultado
        adverso y devuelve sin tocar nada.

        La lógica de reintentos automáticos + bucle de regeneraciones
        humanas vive en `_kickoff_requisitos_con_gate_humano`. Este
        método solo decide si arrancar la fase y delega.
        """
        if self.state.resultado_final != "pendiente":
            print(f"\n[Fase 01] Saltada (resultado={self.state.resultado_final}).")
            return

        # Inicializa el slot de FaseStatus si no existe (idempotente).
        self.state.fases_status.setdefault(_FASE_01, FaseStatus())

        self._kickoff_requisitos_con_gate_humano()

    # -----------------------------------------------------------------------
    # Paso 3 — Fase 02: Planificación + Gate 2
    # -----------------------------------------------------------------------

    @listen(ejecutar_fase_01_requisitos)
    def ejecutar_fase_02_planificacion(self) -> None:
        """
        Ejecuta la fase 02 con su gate humano.

        Si setup_run falló o la fase 01 abortó, este paso es no-op:
        detecta el resultado_final terminal y devuelve sin tocar nada.

        D.1 (cerrada en 8f): la fase 01 NO marca resultado_final="completo"
        cuando acepta el gate. Si está aceptada y nada falló antes, el
        state llega aquí con resultado_final="pendiente". Solo abortamos
        este paso si el resultado_final ya es terminal (los estados
        abortado_* o bloqueado_*).

        La lógica de reintentos automáticos + bucle de regeneraciones
        humanas vive en `_kickoff_planificacion_con_gate_humano`. Este
        método solo decide si arrancar la fase y delega.
        """
        if self.state.resultado_final != "pendiente":
            print(f"\n[Fase 02] Saltada (resultado={self.state.resultado_final}).")
            return

        # Defensa: si por alguna razón fase 01 no produjo el registro
        # (p.ej. cambio futuro en el orden de fases que rompa esta
        # dependencia), no arrancamos fase 02 sin input.
        if self.state.registro_requisitos is None:
            print("\n[Fase 02] No hay registro de requisitos en el state. "
                  "Imposible arrancar fase 02 sin input. Marcando Run "
                  "como abortado_por_limite.")
            self.state.resultado_final = "abortado_por_limite"
            return

        # Inicializa el slot de FaseStatus si no existe (idempotente).
        self.state.fases_status.setdefault(_FASE_02, FaseStatus())

        self._kickoff_planificacion_con_gate_humano()

    # -----------------------------------------------------------------------
    # Paso 4 — Fase 03: Arquitectura + Gate 3
    # -----------------------------------------------------------------------

    @listen(ejecutar_fase_02_planificacion)
    def ejecutar_fase_03_arquitectura(self) -> None:
        """
        Ejecuta la fase 03 con su gate humano.

        Si alguna fase previa abortó, este paso es no-op. La fase 03
        depende de los cuatro artefactos aceptados hasta ahora:
        registro de requisitos, backlog, plan de sprints y riesgos.
        """
        if self.state.resultado_final != "pendiente":
            print(f"\n[Fase 03] Saltada (resultado={self.state.resultado_final}).")
            return

        if (
            self.state.registro_requisitos is None
            or self.state.backlog is None
            or self.state.plan_sprints is None
            or self.state.riesgos is None
        ):
            print("\n[Fase 03] Faltan artefactos previos en el state. "
                  "Imposible arrancar arquitectura sin requisitos, backlog, "
                  "plan de sprints y riesgos. Marcando Run como "
                  "abortado_por_limite.")
            self.state.resultado_final = "abortado_por_limite"
            return

        self.state.fases_status.setdefault(_FASE_03, FaseStatus())

        self._kickoff_arquitectura_con_gate_humano()

    # -----------------------------------------------------------------------
    # Paso 5 — Sprint 1
    # -----------------------------------------------------------------------

    @listen(ejecutar_fase_03_arquitectura)
    def ejecutar_scaffold_base(self) -> None:
        """Genera una base Django minima antes de los sprints funcionales."""
        if self.state.resultado_final != "pendiente":
            print(f"\n[Scaffold] Saltado (resultado={self.state.resultado_final}).")
            return

        if self.state.diseno_tecnico is None:
            print("\n[Scaffold] No hay diseno tecnico en state.")
            self.state.resultado_final = "abortado_por_limite"
            return

        self.state.fases_status.setdefault(_FASE_03B, FaseStatus())
        self._ejecutar_scaffold_base()

    @listen(ejecutar_scaffold_base)
    def ejecutar_sprint_1(self) -> None:
        """Ejecuta el sprint 1 sin gate humano."""
        self._ejecutar_sprint(1)

    # -----------------------------------------------------------------------
    # Paso 6 — Sprint 2
    # -----------------------------------------------------------------------

    @listen(ejecutar_sprint_1)
    def ejecutar_sprint_2(self) -> None:
        """Ejecuta el sprint 2 sin gate humano."""
        self._ejecutar_sprint(2)

    # -----------------------------------------------------------------------
    # Paso 7 — Sprint 3
    # -----------------------------------------------------------------------

    @listen(ejecutar_sprint_2)
    def ejecutar_sprint_3(self) -> None:
        """Ejecuta el sprint 3 sin gate humano."""
        self._ejecutar_sprint(3)

    # -----------------------------------------------------------------------
    # Paso 8 — Cierre del Run
    # -----------------------------------------------------------------------

    @listen(ejecutar_sprint_3)
    def ejecutar_validacion_final(self) -> None:
        """Ejecuta la validacion final determinista del producto generado."""
        if self.state.resultado_final != "pendiente":
            print(f"\n[Validacion final] Saltada "
                  f"(resultado={self.state.resultado_final}).")
            return

        if self.state.paths is None:
            print("\n[Validacion final] Sin paths del Run.")
            self.state.resultado_final = "bloqueado_arranque"
            return

        fase_dir = ensure_dir(self.state.paths.fase_99_cierre)
        codigo_dir = self.state.paths.fase_06_sprint_3 / "codigo"
        status = self.state.fases_status.setdefault(_FASE_99, FaseStatus())
        timeout_s = _leer_timeout_django_check()
        t0 = time.monotonic()

        try:
            validacion = construir_validacion_final(
                id_ejecucion=self.state.run_id,
                codigo_dir=codigo_dir,
                salida_dir=fase_dir,
                timeout_s=timeout_s,
            )
        except Exception as e:
            print(f"\n[Validacion final] Fallo tecnico ejecutando validador: {e}")
            traceback.print_exc()
            self.state.resultado_final = "abortado_por_limite"
            return
        finally:
            status.duracion_s_ejec += time.monotonic() - t0

        self.state.validacion_final = validacion
        write_json(
            fase_dir / "validacion_final.json",
            validacion.model_dump(),
        )
        write_text(
            fase_dir / "review_final.md",
            render_review_final_md(validacion),
        )

        print("\n[Validacion final] Completada.")
        print(f"[Validacion final] ok_global={validacion.ok_global}, "
              f"clasificacion={validacion.review_final.clasificacion}.")
        print(f"[Validacion final] Incidencias: "
              f"{len(validacion.review_final.incidencias)}")

    @listen(ejecutar_validacion_final)
    def cerrar_run(self) -> None:
        """
        Escribe el run_summary.json e imprime el resumen por consola.
        Se ejecuta siempre, tanto en éxito como en fallo de alguna fase.
        """
        # Caso de fallo en setup_run: ni siquiera tenemos paths para
        # escribir un summary. Solo imprimimos el motivo.
        if self.state.paths is None:
            print(f"\n[Cierre] resultado_final = {self.state.resultado_final}")
            print("[Cierre] Sin paths del Run; no se escribe run_summary.json.")
            return

        # D.1 (cerrada en 8f): ninguna fase intermedia marca
        # resultado_final="completo"; lo decide cerrar_run aquí. Si al
        # llegar al cierre ningún paso lo movió a un estado terminal
        # (abortado_*, bloqueado_*), el Run terminó OK y promovemos
        # "pendiente" a "completo". Si ya está en un estado terminal,
        # respetamos lo que se haya marcado.
        if self.state.resultado_final == "pendiente":
            self.state.resultado_final = "completo"

        mensaje = self._mensaje_resumen()
        self._escribir_resumen_run(mensaje)
        self._escribir_cierre_documental()

        print("\n" + "=" * 70)
        print(f"Run cerrado — resultado_final = {self.state.resultado_final}")
        print("=" * 70)

        # E.2 (cerrada en 8f): resumen por fase iterando fases_status, en
        # vez de bloque hardcodeado por fase. El orden de iteración es el
        # orden de inserción del dict (insertion order, Python ≥ 3.7), que
        # coincide con el orden cronológico en que las fases fueron
        # registrando su FaseStatus. Así fase 03 entra automáticamente
        # cuando se enchufe.
        for nombre_fase, status in self.state.fases_status.items():
            self._imprimir_resumen_fase(nombre_fase, status)

    # =======================================================================
    # Helpers internos del Flow
    # =======================================================================

    # -----------------------------------------------------------------------
    # Helpers de sprints 04-06
    # -----------------------------------------------------------------------

    def _ejecutar_scaffold_base(self) -> None:
        """
        Ejecuta un scaffold Django minimo antes del sprint 1.

        El scaffold no implementa historias de usuario. Su objetivo es crear
        una base ejecutable para que los sprints 1-3 se concentren en
        funcionalidad incremental.
        """
        assert self.state.paths is not None
        assert self.state.diseno_tecnico is not None

        fase_dir = self.state.paths.fase_03b_scaffold
        codigo_dir = ensure_dir(fase_dir / "codigo")

        entrega, mensaje = self._kickoff_scaffold_con_reintentos(codigo_dir=codigo_dir)
        if entrega is None:
            self.state.resultado_final = "abortado_por_limite"
            print(f"\n[Scaffold] {mensaje}")
            print(f"Artefactos parciales en: {self.state.paths.attempts}")
            return

        self.state.entregas_sprint[0] = entrega
        try:
            self._escribir_y_aplicar_entrega(
                fase_dir=fase_dir,
                codigo_dir=codigo_dir,
                entrega=entrega,
                nombre_archivo="entrega_scaffold.json",
            )
        except Exception as e:
            print(f"\n[Scaffold] Fallo escribiendo codigo: {e}")
            traceback.print_exc()
            self.state.resultado_final = "abortado_por_limite"
            return

        timeout_s = _leer_timeout_django_check()
        arranque = ejecutar_manage_check(codigo_dir, timeout_s=timeout_s)
        write_json(
            fase_dir / "scaffold_check.json",
            arranque.model_dump(),
        )

        print(f"\n[Scaffold] {mensaje}")
        print(f"[Scaffold] manage.py check ok={arranque.ok}, "
              f"returncode={arranque.returncode}.")
        if not arranque.ok:
            print("[Scaffold] La base Django no arranca; se aborta antes del Sprint 1.")
            self.state.resultado_final = "abortado_por_limite"

    def _kickoff_scaffold_con_reintentos(
        self,
        *,
        codigo_dir: Path,
    ) -> tuple[Optional[EntregaSprint], str]:
        """Ejecuta DesarrolloCrew para crear el scaffold base."""
        assert self.state.diseno_tecnico is not None

        status = self.state.fases_status[_FASE_03B]
        crew_obj = DesarrolloCrew().crew()
        ultimo_error = ""

        for intento in range(1, _MAX_REINTENTOS + 1):
            print(f"\n[Scaffold] Intento {intento}/{_MAX_REINTENTOS}...")
            t0 = time.monotonic()

            try:
                result = crew_obj.kickoff(
                    inputs={
                        "run_id": self.state.run_id,
                        "numero_sprint": 0,
                        "diseno_tecnico_json": self.state.diseno_tecnico.model_dump_json(indent=2),
                        "backlog_sprint_json": "{}",
                        "codigo_previo_texto": "NO HAY CODIGO PREVIO. Genera solo el scaffold Django base.",
                        "review_anterior_json": "{}",
                    }
                )
            except Exception as e:
                ultimo_error = f"Excepcion en kickoff: {type(e).__name__}: {e}"
                print(f"[Scaffold] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_03B,
                    intento=intento,
                    error=ultimo_error,
                    raw="",
                )
                if _es_error_rate_limit(e) and intento < _MAX_REINTENTOS:
                    espera_s = _retry_after_s(e)
                    print(
                        f"[Scaffold] Rate limit del proveedor. "
                        f"Esperando {espera_s}s antes de reintentar..."
                    )
                    time.sleep(espera_s)
                continue

            status.duracion_s_ejec += time.monotonic() - t0

            entrega = self._recoger_output_desarrollo(result)
            if entrega is None:
                raw = getattr(result, "raw", "") or str(result)
                ultimo_error = (
                    "La salida de la crew no contiene una EntregaSprint "
                    "valida recogible por isinstance."
                )
                print(f"[Scaffold] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_03B,
                    intento=intento,
                    error=ultimo_error,
                    raw=raw,
                )
                continue

            try:
                validate_entrega_sprint_contenido(entrega)
            except ContenidoInsuficienteError as e:
                ultimo_error = f"Contenido insuficiente: {e}"
                print(f"[Scaffold] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_03B,
                    intento=intento,
                    error=ultimo_error,
                    raw=entrega.model_dump_json(indent=2),
                )
                continue

            print(f"[Scaffold] Intento {intento} OK.")
            return entrega, "Scaffold base completado correctamente."

        return None, (
            f"Scaffold agoto {_MAX_REINTENTOS} reintentos. "
            f"Ultimo error: {ultimo_error}"
        )

    def _ejecutar_sprint(self, numero_sprint: int) -> None:
        """
        Ejecuta un sprint completo:
          1. Prepara `codigo/` copiando el sprint anterior si procede.
          2. Llama a DesarrolloCrew con reintentos automáticos.
          3. Escribe/aplica la EntregaSprint.
          4. Ejecuta `manage.py check`.
          5. Construye y escribe review_sprint_N.json/md.

        No hay gate humano. Si la generación de la EntregaSprint agota
        reintentos, el Run aborta por límite. Si `manage.py check` falla,
        el Run continúa y la incidencia queda en el review.
        """
        if self.state.resultado_final != "pendiente":
            print(f"\n[Sprint {numero_sprint}] Saltado "
                  f"(resultado={self.state.resultado_final}).")
            return

        fase = _fase_sprint(numero_sprint)
        fase_dir = self._fase_dir_sprint(numero_sprint)
        codigo_dir = fase_dir / "codigo"
        status = self.state.fases_status.setdefault(fase, FaseStatus())

        try:
            sprint_backlog = self._obtener_backlog_sprint(numero_sprint)
        except Exception as e:
            print(f"\n[Sprint {numero_sprint}] No se pudo obtener backlog: {e}")
            traceback.print_exc()
            self.state.resultado_final = "abortado_por_limite"
            return

        if self.state.diseno_tecnico is None:
            print(f"\n[Sprint {numero_sprint}] No hay diseño técnico en state.")
            self.state.resultado_final = "abortado_por_limite"
            return

        try:
            self._preparar_codigo_sprint(numero_sprint)
        except Exception as e:
            print(f"\n[Sprint {numero_sprint}] Fallo preparando codigo/: {e}")
            traceback.print_exc()
            self.state.resultado_final = "abortado_por_limite"
            return

        entrega, mensaje = self._kickoff_sprint_con_reintentos(
            numero_sprint=numero_sprint,
            sprint_backlog=sprint_backlog,
            codigo_dir=codigo_dir,
        )
        if entrega is None:
            self.state.resultado_final = "abortado_por_limite"
            print(f"\n[Sprint {numero_sprint}] {mensaje}")
            print(f"Artefactos parciales en: {self.state.paths.attempts if self.state.paths else '(sin paths)'}")
            return

        self.state.entregas_sprint[numero_sprint] = entrega
        try:
            self._escribir_y_aplicar_entrega_sprint(
                numero_sprint=numero_sprint,
                entrega=entrega,
                codigo_dir=codigo_dir,
            )
        except Exception as e:
            print(f"\n[Sprint {numero_sprint}] Fallo escribiendo código: {e}")
            traceback.print_exc()
            self.state.resultado_final = "abortado_por_limite"
            return

        timeout_s = _leer_timeout_django_check()
        arranque = ejecutar_manage_check(codigo_dir, timeout_s=timeout_s)
        review = construir_review_sprint(
            sprint_backlog=sprint_backlog,
            codigo_dir=codigo_dir,
            arranque=arranque,
        )
        self.state.reviews_sprint[numero_sprint] = review

        try:
            self._escribir_review_sprint(
                numero_sprint=numero_sprint,
                review=review,
            )
        except Exception as e:
            print(f"\n[Sprint {numero_sprint}] Fallo escribiendo review: {e}")
            traceback.print_exc()
            self.state.resultado_final = "abortado_por_limite"
            return

        print(f"\n[Sprint {numero_sprint}] {mensaje}")
        print(f"[Sprint {numero_sprint}] manage.py check ok={arranque.ok}, "
              f"returncode={arranque.returncode}.")
        print(f"[Sprint {numero_sprint}] Review escrito en "
              f"{fase_dir / f'review_sprint_{numero_sprint}.md'}")

    def _kickoff_sprint_con_reintentos(
        self,
        *,
        numero_sprint: int,
        sprint_backlog: BacklogSprint,
        codigo_dir: Path,
    ) -> tuple[Optional[EntregaSprint], str]:
        """Ejecuta DesarrolloCrew para un sprint con reintentos automáticos."""
        assert self.state.diseno_tecnico is not None

        fase = _fase_sprint(numero_sprint)
        status = self.state.fases_status[fase]
        crew_obj = DesarrolloCrew().crew()

        review_anterior = self.state.reviews_sprint.get(numero_sprint - 1)
        review_anterior_json = (
            review_anterior.model_dump_json(indent=2)
            if review_anterior is not None
            else "{}"
        )
        codigo_previo_texto = self._serializar_codigo_para_llm(codigo_dir)
        if not codigo_previo_texto.strip():
            codigo_previo_texto = "NO HAY CÓDIGO PREVIO PARA ESTE SPRINT."

        ultimo_error = ""

        for intento in range(1, _MAX_REINTENTOS + 1):
            print(f"\n[Sprint {numero_sprint}] Intento {intento}/{_MAX_REINTENTOS}...")
            t0 = time.monotonic()

            try:
                result = crew_obj.kickoff(
                    inputs={
                        "run_id": self.state.run_id,
                        "numero_sprint": numero_sprint,
                        "diseno_tecnico_json": self.state.diseno_tecnico.model_dump_json(indent=2),
                        "backlog_sprint_json": sprint_backlog.model_dump_json(indent=2),
                        "codigo_previo_texto": codigo_previo_texto,
                        "review_anterior_json": review_anterior_json,
                    }
                )
            except Exception as e:
                ultimo_error = f"Excepción en kickoff: {type(e).__name__}: {e}"
                print(f"[Sprint {numero_sprint}] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=fase,
                    intento=intento,
                    error=ultimo_error,
                    raw="",
                )
                if _es_error_rate_limit(e) and intento < _MAX_REINTENTOS:
                    espera_s = _retry_after_s(e)
                    print(
                        f"[Sprint {numero_sprint}] Rate limit del proveedor. "
                        f"Esperando {espera_s}s antes de reintentar..."
                    )
                    time.sleep(espera_s)
                continue

            status.duracion_s_ejec += time.monotonic() - t0

            entrega = self._recoger_output_desarrollo(result)
            if entrega is None:
                raw = getattr(result, "raw", "") or str(result)
                ultimo_error = (
                    "La salida de la crew no contiene una EntregaSprint "
                    "válida recogible por isinstance."
                )
                print(f"[Sprint {numero_sprint}] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=fase,
                    intento=intento,
                    error=ultimo_error,
                    raw=raw,
                )
                continue

            try:
                require_base_django = not self._codigo_tiene_base_django(codigo_dir)
                validate_entrega_sprint_contenido(
                    entrega,
                    require_base_django=require_base_django,
                )
            except ContenidoInsuficienteError as e:
                ultimo_error = f"Contenido insuficiente: {e}"
                print(f"[Sprint {numero_sprint}] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=fase,
                    intento=intento,
                    error=ultimo_error,
                    raw=entrega.model_dump_json(indent=2),
                )
                continue

            print(f"[Sprint {numero_sprint}] Intento {intento} OK.")
            return entrega, f"Sprint {numero_sprint} completado correctamente."

        return None, (
            f"Sprint {numero_sprint} agotó {_MAX_REINTENTOS} reintentos. "
            f"Último error: {ultimo_error}"
        )

    def _recoger_output_desarrollo(self, result: object) -> Optional[EntregaSprint]:
        """
        Recoge una `EntregaSprint` por isinstance sobre tasks_output.
        Mantiene el patrón defensivo usado en planificación y arquitectura.
        """
        tasks_output = getattr(result, "tasks_output", None)
        if not tasks_output:
            modelo_directo = getattr(result, "pydantic", None)
            if isinstance(modelo_directo, EntregaSprint):
                return modelo_directo
            print("[Desarrollo] result.tasks_output vacío o ausente.")
            return None

        entrega: Optional[EntregaSprint] = None
        for idx, t_out in enumerate(tasks_output):
            modelo = getattr(t_out, "pydantic", None)
            if modelo is None:
                print(f"[Desarrollo] tasks_output[{idx}].pydantic es None.")
                continue
            if isinstance(modelo, EntregaSprint):
                if entrega is not None:
                    print(f"[Desarrollo] EntregaSprint duplicada en tasks_output[{idx}].")
                    return None
                entrega = modelo
            else:
                print(f"[Desarrollo] tasks_output[{idx}] tiene tipo inesperado: "
                      f"{type(modelo).__name__}.")

        return entrega

    def _preparar_codigo_sprint(self, numero_sprint: int) -> None:
        """Crea codigo/ y copia el sprint anterior cuando corresponde."""
        fase_dir = self._fase_dir_sprint(numero_sprint)
        codigo_dir = ensure_dir(fase_dir / "codigo")

        if numero_sprint == 1:
            assert self.state.paths is not None
            codigo_scaffold = self.state.paths.fase_03b_scaffold / "codigo"
            if codigo_scaffold.exists():
                shutil.copytree(codigo_scaffold, codigo_dir, dirs_exist_ok=True)
            return

        codigo_anterior = self._fase_dir_sprint(numero_sprint - 1) / "codigo"
        if not codigo_anterior.exists():
            raise FileNotFoundError(
                f"No existe codigo/ del sprint anterior: {codigo_anterior}"
            )

        shutil.copytree(codigo_anterior, codigo_dir, dirs_exist_ok=True)

    def _escribir_y_aplicar_entrega_sprint(
        self,
        *,
        numero_sprint: int,
        entrega: EntregaSprint,
        codigo_dir: Path,
    ) -> None:
        """Escribe entrega_sprint_N.json y aplica archivos en codigo/."""
        fase_dir = self._fase_dir_sprint(numero_sprint)
        self._escribir_y_aplicar_entrega(
            fase_dir=fase_dir,
            codigo_dir=codigo_dir,
            entrega=entrega,
            nombre_archivo=f"entrega_sprint_{numero_sprint}.json",
        )

    def _escribir_y_aplicar_entrega(
        self,
        *,
        fase_dir: Path,
        codigo_dir: Path,
        entrega: EntregaSprint,
        nombre_archivo: str,
    ) -> None:
        """Escribe un artefacto EntregaSprint y aplica sus archivos."""
        write_json(fase_dir / nombre_archivo, entrega.model_dump())
        for archivo in entrega.archivos:
            destino = self._resolver_path_codigo(codigo_dir, archivo.path)
            write_text(destino, archivo.contenido)

    def _codigo_tiene_base_django(self, codigo_dir: Path) -> bool:
        """Comprueba si codigo/ ya contiene los archivos base Django."""
        if not (codigo_dir / "manage.py").exists():
            return False
        archivos = listar_archivos_codigo(codigo_dir)
        paths_lower = [path.relative_to(codigo_dir).as_posix().lower() for path in archivos]
        tiene_settings = any(path.endswith("/settings.py") for path in paths_lower)
        tiene_urls = any(path == "urls.py" or path.endswith("/urls.py") for path in paths_lower)
        return tiene_settings and tiene_urls

    def _escribir_review_sprint(
        self,
        *,
        numero_sprint: int,
        review: ReviewSprint,
    ) -> None:
        """Escribe review_sprint_N.json/md."""
        fase = _fase_sprint(numero_sprint)
        fase_dir = self._fase_dir_sprint(numero_sprint)

        write_json(
            fase_dir / f"review_sprint_{numero_sprint}.json",
            review.model_dump(),
        )
        frontmatter = render_frontmatter(
            run_id=self.state.run_id,
            fase=fase,
            agente="Script",
            modelo="deterministico",
            timestamp=now_iso_madrid(),
            hash_brief=self.state.hashes.brief,
            regeneraciones_previas=0,
        )
        write_text(
            fase_dir / f"review_sprint_{numero_sprint}.md",
            frontmatter + render_review_sprint_md(review),
        )

    def _obtener_backlog_sprint(self, numero_sprint: int) -> BacklogSprint:
        """Devuelve el BacklogSprint derivado para el sprint indicado."""
        backlog_sprint = self.state.sprint_backlogs.get(numero_sprint)
        if backlog_sprint is None:
            raise ValueError(
                f"No hay BacklogSprint {numero_sprint} en state. "
                "Debe derivarse tras Gate 3 aceptado."
            )
        return backlog_sprint

    def _serializar_codigo_para_llm(
        self,
        codigo_dir: Path,
        *,
        max_chars_total: int = 160_000,
        max_chars_por_archivo: int = 20_000,
    ) -> str:
        """
        Serializa el código actual para pasarlo al Desarrollador.
        Se limita el tamaño para evitar prompts descontrolados.
        """
        if not codigo_dir.exists():
            return ""

        partes: list[str] = []
        total = 0
        for path in listar_archivos_codigo(codigo_dir):
            rel = path.relative_to(codigo_dir).as_posix()
            try:
                contenido = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                contenido = ""
            bloque = (
                f"\n--- FILE: {rel} ---\n"
                f"{contenido[:max_chars_por_archivo]}"
            )
            if total + len(bloque) > max_chars_total:
                partes.append("\n...[código truncado por límite de contexto]...")
                break
            partes.append(bloque)
            total += len(bloque)

        return "\n".join(partes)

    def _resolver_path_codigo(self, codigo_dir: Path, path_relativo: str) -> Path:
        """
        Resuelve una ruta relativa dentro de codigo/ y bloquea escapes.
        """
        path_limpio = path_relativo.replace("\\", "/").strip()
        destino = (codigo_dir / path_limpio).resolve()
        raiz = codigo_dir.resolve()
        if destino == raiz or raiz not in destino.parents:
            raise ValueError(f"Ruta fuera de codigo/: {path_relativo}")
        return destino

    def _fase_dir_sprint(self, numero_sprint: int) -> Path:
        """Devuelve la carpeta de fase para un sprint."""
        assert self.state.paths is not None
        if numero_sprint == 1:
            return self.state.paths.fase_04_sprint_1
        if numero_sprint == 2:
            return self.state.paths.fase_05_sprint_2
        if numero_sprint == 3:
            return self.state.paths.fase_06_sprint_3
        raise ValueError(f"Sprint no soportado: {numero_sprint}")

    # -----------------------------------------------------------------------
    # Helpers de fase 03
    # -----------------------------------------------------------------------

    def _kickoff_arquitectura_con_gate_humano(self) -> None:
        """
        Orquesta fase 03 + gate humano sobre un único artefacto
        (`diseno_tecnico.md`), hasta convergencia o agotamiento del
        presupuesto de regeneraciones.
        """
        assert self.state.paths is not None
        max_regeneraciones = _leer_max_regeneraciones_humanas()
        status = self.state.fases_status[_FASE_03]

        feedback_humano = ""

        while True:
            diseno, mensaje = self._kickoff_arquitectura_con_reintentos(
                feedback_humano=feedback_humano,
            )

            if diseno is None:
                self.state.resultado_final = "abortado_por_limite"
                print(f"\n[Fase 03] {mensaje}")
                print(f"Artefactos parciales en: {self.state.paths.attempts}")
                return

            self.state.diseno_tecnico = diseno
            try:
                self._escribir_artefactos_arquitectura(diseno)
            except Exception as e:
                print(f"\n[Fase 03] Fallo al escribir artefactos: {e}")
                traceback.print_exc()
                self.state.resultado_final = "abortado_por_limite"
                return

            print(f"\n[Fase 03] {mensaje}")

            fase_dir = self.state.paths.fase_03_arquitectura
            try:
                resultado_gate = human_gate(
                    fase=_FASE_03,
                    fase_dir=fase_dir,
                    artefactos_md=[fase_dir / "diseno_tecnico.md"],
                    numero_gate=3,
                    regeneraciones_consumidas=status.regeneraciones_humanas,
                    max_regeneraciones=max_regeneraciones,
                )
            except GateError as e:
                print(f"\n[Gate 3] Error técnico: {e}")
                self.state.resultado_final = "abortado_por_limite"
                return

            status.duracion_s_gate_humano += resultado_gate.duracion_s

            if resultado_gate.decision == "aceptado":
                status.gate_decision = "aceptado"
                obs_resumen = (resultado_gate.observaciones or "").strip()
                if obs_resumen:
                    print(f"[Gate 3] Aceptado con observaciones: "
                          f"{obs_resumen[:200]}"
                          f"{'...' if len(obs_resumen) > 200 else ''}")
                else:
                    print("[Gate 3] Aceptado sin observaciones.")
                try:
                    self._derivar_sprint_backlogs()
                except Exception as e:
                    print(f"\n[Fase 03] Fallo al derivar backlogs por sprint: {e}")
                    traceback.print_exc()
                    self.state.resultado_final = "abortado_por_limite"
                return

            if resultado_gate.decision == "abortado":
                status.gate_decision = "abortado"
                self.state.resultado_final = "abortado_en_gate"
                print("[Gate 3] Abortado por la operadora.")
                return

            if resultado_gate.decision == "rechazado":
                if status.regeneraciones_humanas >= max_regeneraciones:
                    status.gate_decision = "rechazado"
                    self.state.resultado_final = "abortado_por_limite"
                    print(f"[Gate 3] Rechazado y presupuesto agotado "
                          f"({status.regeneraciones_humanas}/"
                          f"{max_regeneraciones} regeneraciones consumidas). "
                          f"Run abortado.")
                    return

                status.regeneraciones_humanas += 1
                status.reintentos_automaticos = 0
                feedback_humano = _formatear_feedback_humano(
                    resultado_gate=resultado_gate,
                    numero_regeneracion=status.regeneraciones_humanas,
                    max_regeneraciones=max_regeneraciones,
                )
                print(f"[Gate 3] Rechazado. Iniciando regeneración "
                      f"{status.regeneraciones_humanas}/{max_regeneraciones}...")
                continue

            raise RuntimeError(
                f"Decisión de gate desconocida: {resultado_gate.decision!r}"
            )

    def _kickoff_arquitectura_con_reintentos(
        self,
        *,
        feedback_humano: str = "",
    ) -> tuple[Optional[DisenoTecnico], str]:
        """
        Ejecuta la arquitectura_crew con hasta `_MAX_REINTENTOS` intentos.
        Valida el `DisenoTecnico` al final del kickoff con reglas
        deterministas de contenido mínimo.
        """
        assert self.state.registro_requisitos is not None
        assert self.state.backlog is not None
        assert self.state.plan_sprints is not None
        assert self.state.riesgos is not None

        crew_obj = ArquitecturaCrew().crew()
        status = self.state.fases_status[_FASE_03]

        registro_json = self.state.registro_requisitos.model_dump_json(indent=2)
        backlog_json = self.state.backlog.model_dump_json(indent=2)
        plan_json = self.state.plan_sprints.model_dump_json(indent=2)
        riesgos_json = self.state.riesgos.model_dump_json(indent=2)

        ultimo_error: str = ""

        for intento in range(1, _MAX_REINTENTOS + 1):
            print(f"\n[Fase 03] Intento {intento}/{_MAX_REINTENTOS}...")
            t0 = time.monotonic()

            try:
                result = crew_obj.kickoff(
                    inputs={
                        "run_id": self.state.run_id,
                        "registro_requisitos_json": registro_json,
                        "backlog_json": backlog_json,
                        "plan_sprints_json": plan_json,
                        "riesgos_json": riesgos_json,
                        "feedback_humano": feedback_humano,
                    }
                )
            except Exception as e:
                ultimo_error = f"Excepción en kickoff: {type(e).__name__}: {e}"
                print(f"[Fase 03] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_03,
                    intento=intento,
                    error=ultimo_error,
                    raw="",
                )
                if _es_error_rate_limit(e) and intento < _MAX_REINTENTOS:
                    espera_s = _retry_after_s(e)
                    print(
                        f"[Fase 03] Rate limit del proveedor. "
                        f"Esperando {espera_s}s antes de reintentar..."
                    )
                    time.sleep(espera_s)
                continue

            status.duracion_s_ejec += time.monotonic() - t0

            diseno = self._recoger_output_arquitectura(result)
            if diseno is None:
                raw = getattr(result, "raw", "") or str(result)
                ultimo_error = (
                    "La salida de la crew no contiene un DisenoTecnico "
                    "válido recogible por isinstance."
                )
                print(f"[Fase 03] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_03,
                    intento=intento,
                    error=ultimo_error,
                    raw=raw,
                )
                continue

            try:
                validate_diseno_tecnico_contenido(diseno)
            except ContenidoInsuficienteError as e:
                ultimo_error = f"Contenido insuficiente: {e}"
                print(f"[Fase 03] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_03,
                    intento=intento,
                    error=ultimo_error,
                    raw=diseno.model_dump_json(indent=2),
                )
                continue

            print(f"[Fase 03] Intento {intento} OK.")
            return diseno, "Fase 03 completada correctamente."

        return None, (
            f"Fase 03 agotó {_MAX_REINTENTOS} reintentos. "
            f"Último error: {ultimo_error}"
        )

    def _recoger_output_arquitectura(
        self,
        result: object,
    ) -> Optional[DisenoTecnico]:
        """
        Recoge el `DisenoTecnico` por isinstance sobre tasks_output.
        Aunque fase 03 tiene una sola task, mantenemos la defensa B.2:
        no depender del índice posicional del output.
        """
        tasks_output = getattr(result, "tasks_output", None)
        if not tasks_output:
            modelo_directo = getattr(result, "pydantic", None)
            if isinstance(modelo_directo, DisenoTecnico):
                return modelo_directo
            print("[Fase 03] result.tasks_output vacío o ausente.")
            return None

        diseno: Optional[DisenoTecnico] = None
        for idx, t_out in enumerate(tasks_output):
            modelo = getattr(t_out, "pydantic", None)
            if modelo is None:
                print(f"[Fase 03] tasks_output[{idx}].pydantic es None.")
                continue

            if isinstance(modelo, DisenoTecnico):
                if diseno is not None:
                    print(f"[Fase 03] DisenoTecnico duplicado en "
                          f"tasks_output[{idx}].")
                    return None
                diseno = modelo
            else:
                print(f"[Fase 03] tasks_output[{idx}] tiene tipo inesperado: "
                      f"{type(modelo).__name__}.")

        return diseno

    def _escribir_artefactos_arquitectura(
        self,
        diseno: DisenoTecnico,
    ) -> None:
        """
        Escribe los artefactos canónicos de la fase 03:
          - diseno_tecnico.json
          - diseno_tecnico.md
        """
        assert self.state.paths is not None
        fase_dir = self.state.paths.fase_03_arquitectura
        status = self.state.fases_status[_FASE_03]

        frontmatter = render_frontmatter(
            run_id=self.state.run_id,
            fase=_FASE_03,
            agente="Arquitecto",
            modelo=get_model_name("architect"),
            timestamp=now_iso_madrid(),
            hash_brief=self.state.hashes.brief,
            regeneraciones_previas=status.regeneraciones_humanas,
        )

        write_json(fase_dir / "diseno_tecnico.json", diseno.model_dump())
        write_text(
            fase_dir / "diseno_tecnico.md",
            frontmatter + render_diseno_tecnico_md(diseno),
        )

    def _derivar_sprint_backlogs(self) -> None:
        """
        Deriva y escribe `backlog_sprint_N.json/md` para los tres sprints.

        Es un paso determinista: usa el backlog y el plan aceptados por
        Gate 2. Se ejecuta después de Gate 3 aceptado para no preparar
        artefactos de desarrollo si el diseño técnico queda rechazado o
        abortado.
        """
        assert self.state.paths is not None
        assert self.state.backlog is not None
        assert self.state.plan_sprints is not None

        sprint_backlogs = derivar_sprint_backlogs(
            backlog=self.state.backlog,
            plan=self.state.plan_sprints,
            run_id=self.state.run_id,
        )

        dirs_por_sprint = {
            1: self.state.paths.fase_04_sprint_1,
            2: self.state.paths.fase_05_sprint_2,
            3: self.state.paths.fase_06_sprint_3,
        }

        for backlog_sprint in sprint_backlogs:
            fase_dir = dirs_por_sprint.get(backlog_sprint.numero_sprint)
            if fase_dir is None:
                raise ValueError(
                    "Número de sprint no soportado al escribir backlog: "
                    f"{backlog_sprint.numero_sprint}."
                )

            self.state.sprint_backlogs[backlog_sprint.numero_sprint] = backlog_sprint

            nombre_base = f"backlog_sprint_{backlog_sprint.numero_sprint}"
            write_json(fase_dir / f"{nombre_base}.json", backlog_sprint.model_dump())

            frontmatter = render_frontmatter(
                run_id=self.state.run_id,
                fase=f"{backlog_sprint.numero_sprint + 3:02d}_sprint_{backlog_sprint.numero_sprint}",
                agente="Script",
                modelo="deterministico",
                timestamp=now_iso_madrid(),
                hash_brief=self.state.hashes.brief,
                regeneraciones_previas=0,
            )
            write_text(
                fase_dir / f"{nombre_base}.md",
                frontmatter + render_backlog_sprint_md(backlog_sprint),
            )

        print("[Sprints] Backlogs por sprint derivados correctamente.")

    # -----------------------------------------------------------------------
    # Helpers de fase 02
    # -----------------------------------------------------------------------

    def _kickoff_planificacion_con_gate_humano(self) -> None:
        """
        Orquesta fase 02 + gate humano único sobre los tres artefactos
        (backlog + plan_sprints + riesgos), hasta convergencia o
        agotamiento del presupuesto de regeneraciones.

        Estrategia idéntica a la de fase 01, con dos diferencias:
          - El kickoff devuelve TRES modelos Pydantic, no uno (recogidos
            por isinstance: decisión B.2).
          - El gate humano se invoca con los tres MD a la vez vía la
            firma generalizada `artefactos_md: list[Path]` (decisión A.1).

        D.1 (cerrada en 8f): la rama "aceptado" solo marca
        gate_decision="aceptado". El resultado_final del Run lo decide
        cerrar_run cuando todas las fases hayan terminado sin abortar.

        Acumula `duracion_s_gate_humano` entre regeneraciones (mismo
        criterio que fase 01: refleja tiempo humano total).
        """
        assert self.state.paths is not None  # garantizado por setup_run
        max_regeneraciones = _leer_max_regeneraciones_humanas()
        status = self.state.fases_status[_FASE_02]

        feedback_humano = ""

        while True:
            # ---- Paso 1: generar los tres artefactos -----------------------
            backlog, plan, riesgos, mensaje = (
                self._kickoff_planificacion_con_reintentos(
                    feedback_humano=feedback_humano,
                )
            )

            if backlog is None or plan is None or riesgos is None:
                # Reintentos automáticos agotados. No abrimos el gate.
                self.state.resultado_final = "abortado_por_limite"
                print(f"\n[Fase 02] {mensaje}")
                print(f"Artefactos parciales en: {self.state.paths.attempts}")
                return

            # ---- Paso 2: escribir artefactos canónicos (6 archivos) --------
            self.state.backlog = backlog
            self.state.plan_sprints = plan
            self.state.riesgos = riesgos
            try:
                self._escribir_artefactos_planificacion(backlog, plan, riesgos)
            except Exception as e:
                print(f"\n[Fase 02] Fallo al escribir artefactos: {e}")
                traceback.print_exc()
                self.state.resultado_final = "abortado_por_limite"
                return

            print(f"\n[Fase 02] {mensaje}")

            # ---- Paso 3: gate humano único sobre los tres MD ---------------
            fase_dir = self.state.paths.fase_02_planificacion
            try:
                resultado_gate = human_gate(
                    fase=_FASE_02,
                    fase_dir=fase_dir,
                    artefactos_md=[
                        fase_dir / "backlog.md",
                        fase_dir / "plan_sprints.md",
                        fase_dir / "riesgos.md",
                    ],
                    numero_gate=2,
                    regeneraciones_consumidas=status.regeneraciones_humanas,
                    max_regeneraciones=max_regeneraciones,
                )
            except GateError as e:
                print(f"\n[Gate 2] Error técnico: {e}")
                self.state.resultado_final = "abortado_por_limite"
                return

            status.duracion_s_gate_humano += resultado_gate.duracion_s

            # ---- Paso 4: ramificar según la decisión -----------------------
            if resultado_gate.decision == "aceptado":
                # D.1: solo marcamos gate_decision; resultado_final lo
                # decide cerrar_run.
                status.gate_decision = "aceptado"
                obs_resumen = (resultado_gate.observaciones or "").strip()
                if obs_resumen:
                    print(f"[Gate 2] Aceptado con observaciones: "
                          f"{obs_resumen[:200]}"
                          f"{'...' if len(obs_resumen) > 200 else ''}")
                else:
                    print("[Gate 2] Aceptado sin observaciones.")
                return

            if resultado_gate.decision == "abortado":
                status.gate_decision = "abortado"
                self.state.resultado_final = "abortado_en_gate"
                print("[Gate 2] Abortado por la operadora.")
                return

            # ---- Caso rechazado --------------------------------------------
            if resultado_gate.decision == "rechazado":
                if status.regeneraciones_humanas >= max_regeneraciones:
                    status.gate_decision = "rechazado"
                    self.state.resultado_final = "abortado_por_limite"
                    print(f"[Gate 2] Rechazado y presupuesto agotado "
                          f"({status.regeneraciones_humanas}/"
                          f"{max_regeneraciones} regeneraciones consumidas). "
                          f"Run abortado.")
                    return

                status.regeneraciones_humanas += 1
                # Reset de reintentos automáticos: cada regeneración humana
                # arranca con presupuesto fresco (mismo criterio que fase 01).
                status.reintentos_automaticos = 0
                feedback_humano = _formatear_feedback_humano(
                    resultado_gate=resultado_gate,
                    numero_regeneracion=status.regeneraciones_humanas,
                    max_regeneraciones=max_regeneraciones,
                )
                print(f"[Gate 2] Rechazado. Iniciando regeneración "
                      f"{status.regeneraciones_humanas}/{max_regeneraciones}...")
                continue

            raise RuntimeError(
                f"Decisión de gate desconocida: {resultado_gate.decision!r}"
            )

    def _kickoff_planificacion_con_reintentos(
        self,
        *,
        feedback_humano: str = "",
    ) -> tuple[
        Optional[Backlog],
        Optional[PlanSprints],
        Optional[Riesgos],
        str,
    ]:
        """
        Ejecuta la planificacion_crew con hasta `_MAX_REINTENTOS` intentos.
        No propaga excepciones: las traduce a (None, None, None, mensaje)
        si agota el presupuesto.

        D.4: el registro de requisitos se inyecta vía
        `inputs={"registro_requisitos_json": ...}` solo en la primera
        task (construir_backlog); las otras dos lo reciben transitivamente
        vía context declarado en PlanificacionCrew.

        D.6: el feedback humano de regeneración se inyecta como mismo
        string en las tres tasks (G confirmada).

        D.2: validación al final del kickoff sobre los tres artefactos
        en orden backlog → plan → riesgos, con cortocircuito al primer
        fallo (C.1). Si alguna validación falla, el intento entero
        cuenta como reintento automático.

        Args:
            feedback_humano: bloque de texto para el placeholder
                {feedback_humano}. En primera generación es "", en
                regeneraciones contiene el bloque "INSTRUCCIONES DE
                REGENERACIÓN" formateado por `_formatear_feedback_humano`.
        """
        assert self.state.registro_requisitos is not None
        crew_obj = PlanificacionCrew().crew()
        status = self.state.fases_status[_FASE_02]

        # Serialización del registro: model_dump_json devuelve una cadena
        # JSON. En Pydantic v2 el default emite caracteres no-ASCII tal
        # cual ('código', no 'c\u00f3digo'), así que no hace falta tocar
        # nada para que el prompt sea legible para el modelo.
        registro_json = self.state.registro_requisitos.model_dump_json(
            indent=2,
        )

        ultimo_error: str = ""

        for intento in range(1, _MAX_REINTENTOS + 1):
            print(f"\n[Fase 02] Intento {intento}/{_MAX_REINTENTOS}...")
            t0 = time.monotonic()

            try:
                result = crew_obj.kickoff(
                    inputs={
                        "run_id": self.state.run_id,
                        "registro_requisitos_json": registro_json,
                        "feedback_humano": feedback_humano,
                    }
                )
            except Exception as e:
                ultimo_error = f"Excepción en kickoff: {type(e).__name__}: {e}"
                print(f"[Fase 02] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_02,
                    intento=intento,
                    error=ultimo_error,
                    raw="",
                )
                if _es_error_rate_limit(e) and intento < _MAX_REINTENTOS:
                    espera_s = _retry_after_s(e)
                    print(
                        f"[Fase 02] Rate limit del proveedor. "
                        f"Esperando {espera_s}s antes de reintentar..."
                    )
                    time.sleep(espera_s)
                continue

            status.duracion_s_ejec += time.monotonic() - t0

            # ---- Recoger los tres outputs por isinstance (decisión B.2) ----
            backlog, plan, riesgos = self._recoger_outputs_planificacion(result)
            if backlog is None or plan is None or riesgos is None:
                raw = getattr(result, "raw", "") or str(result)
                ultimo_error = (
                    "La salida de la crew no contiene los tres modelos "
                    "esperados (Backlog, PlanSprints, Riesgos). "
                    f"Recibidos: backlog={type(backlog).__name__}, "
                    f"plan={type(plan).__name__}, "
                    f"riesgos={type(riesgos).__name__}."
                )
                print(f"[Fase 02] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_02,
                    intento=intento,
                    error=ultimo_error,
                    raw=raw,
                )
                continue

            # ---- Validación de contenido en orden, con cortocircuito ------
            # backlog → plan (necesita backlog para cobertura) → riesgos.
            try:
                validate_backlog_contenido(backlog)
                validate_plan_sprints_contenido(plan, backlog)
                validate_riesgos_contenido(riesgos)
            except ContenidoInsuficienteError as e:
                ultimo_error = f"Contenido insuficiente: {e}"
                print(f"[Fase 02] {ultimo_error}")
                status.reintentos_automaticos += 1
                # Guardamos el JSON concatenado de los tres como raw del
                # attempt, para que la operadora pueda inspeccionar qué
                # produjo el LLM en el intento fallido.
                raw_concat = (
                    "---- backlog ----\n"
                    f"{backlog.model_dump_json(indent=2)}\n\n"
                    "---- plan_sprints ----\n"
                    f"{plan.model_dump_json(indent=2)}\n\n"
                    "---- riesgos ----\n"
                    f"{riesgos.model_dump_json(indent=2)}\n"
                )
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_02,
                    intento=intento,
                    error=ultimo_error,
                    raw=raw_concat,
                )
                continue

            print(f"[Fase 02] Intento {intento} OK.")
            return backlog, plan, riesgos, "Fase 02 completada correctamente."

        return None, None, None, (
            f"Fase 02 agotó {_MAX_REINTENTOS} reintentos. "
            f"Último error: {ultimo_error}"
        )

    def _recoger_outputs_planificacion(
        self,
        result: object,
    ) -> tuple[Optional[Backlog], Optional[PlanSprints], Optional[Riesgos]]:
        """
        Toma el CrewOutput devuelto por `PlanificacionCrew().crew().kickoff()`
        y devuelve (backlog, plan_sprints, riesgos), recogidos por isinstance
        sobre el atributo `.pydantic` de cada `tasks_output[i]`.

        Decisión B.2 (cerrada en 8f): no confiamos en el orden posicional.
        Recorremos `tasks_output` y asignamos al slot que cuadre por tipo.
        Si algún slot queda sin rellenar o se rellena dos veces, devolvemos
        (None, None, None) y el llamante lo trata como reintento automático.

        Esta defensa cubre tres escenarios:
          - LLM falla una task: tasks_output puede tener menos de 3 elementos
            o un .pydantic = None.
          - Reordenación accidental de las @task en PlanificacionCrew.
          - Cambios futuros de CrewAI en cómo se mapean tasks → outputs.
        """
        tasks_output = getattr(result, "tasks_output", None)
        if not tasks_output:
            print("[Fase 02] result.tasks_output vacío o ausente.")
            return None, None, None

        backlog: Optional[Backlog] = None
        plan: Optional[PlanSprints] = None
        riesgos: Optional[Riesgos] = None

        for idx, t_out in enumerate(tasks_output):
            modelo = getattr(t_out, "pydantic", None)
            if modelo is None:
                print(f"[Fase 02] tasks_output[{idx}].pydantic es None.")
                continue

            if isinstance(modelo, Backlog):
                if backlog is not None:
                    print(f"[Fase 02] Backlog duplicado en tasks_output[{idx}].")
                    return None, None, None
                backlog = modelo
            elif isinstance(modelo, PlanSprints):
                if plan is not None:
                    print(f"[Fase 02] PlanSprints duplicado en tasks_output[{idx}].")
                    return None, None, None
                plan = modelo
            elif isinstance(modelo, Riesgos):
                if riesgos is not None:
                    print(f"[Fase 02] Riesgos duplicado en tasks_output[{idx}].")
                    return None, None, None
                riesgos = modelo
            else:
                print(f"[Fase 02] tasks_output[{idx}] tiene tipo inesperado: "
                      f"{type(modelo).__name__}.")

        return backlog, plan, riesgos

    def _escribir_artefactos_planificacion(
        self,
        backlog: Backlog,
        plan: PlanSprints,
        riesgos: Riesgos,
    ) -> None:
        """
        Escribe los seis artefactos canónicos de la fase 02 en disco:
          - backlog.json + backlog.md
          - plan_sprints.json + plan_sprints.md
          - riesgos.json + riesgos.md

        Cada MD lleva el frontmatter estándar (Bloque 3 del spec) con
        agente="PM" y el modelo configurado para el perfil `pm`. Mismo
        criterio que `_escribir_artefactos_requisitos`: sobreescribe el
        contenido anterior; los intentos previos quedan en `_attempts/`
        si se conservaron.
        """
        assert self.state.paths is not None
        fase_dir = self.state.paths.fase_02_planificacion
        status = self.state.fases_status[_FASE_02]

        # Frontmatter común a los tres MD: misma fase, mismo agente, mismo
        # timestamp (el del momento en que escribimos los artefactos tras
        # el kickoff aceptado).
        timestamp = now_iso_madrid()
        regen = status.regeneraciones_humanas
        frontmatter = render_frontmatter(
            run_id=self.state.run_id,
            fase=_FASE_02,
            agente="PM",
            modelo=get_model_name("pm"),
            timestamp=timestamp,
            hash_brief=self.state.hashes.brief,
            regeneraciones_previas=regen,
        )

        # ---- Backlog ----
        write_json(fase_dir / "backlog.json", backlog.model_dump())
        write_text(fase_dir / "backlog.md", frontmatter + render_backlog_md(backlog))

        # ---- Plan de sprints ----
        write_json(fase_dir / "plan_sprints.json", plan.model_dump())
        write_text(
            fase_dir / "plan_sprints.md",
            frontmatter + render_plan_sprints_md(plan),
        )

        # ---- Riesgos ----
        write_json(fase_dir / "riesgos.json", riesgos.model_dump())
        write_text(
            fase_dir / "riesgos.md",
            frontmatter + render_riesgos_md(riesgos),
        )

    # -----------------------------------------------------------------------
    # Helper común de cierre (E.2)
    # -----------------------------------------------------------------------

    def _imprimir_resumen_fase(self, nombre_fase: str, status: FaseStatus) -> None:
        """
        Imprime el bloque de resumen de una fase para el cierre del Run.

        Decisión E.2 (cerrada en 8f): el cierre itera fases_status y llama
        a este helper por fase, en vez de tener bloques hardcodeados por
        fase. Cuando se enchufe fase 03, no hay que volver a tocar
        cerrar_run.

        Los detalles específicos de cada fase (cuáles artefactos, cuántos
        items en cada uno) se leen del state.
        """
        assert self.state.paths is not None
        print(f"\n--- Fase {nombre_fase} ---")
        print(f"Reintentos automáticos consumidos (última regeneración): "
              f"{status.reintentos_automaticos}")
        print(f"Regeneraciones humanas consumidas: "
              f"{status.regeneraciones_humanas}")
        print(f"Decisión del gate: {status.gate_decision}")
        print(f"Duración acumulada del gate humano: "
              f"{status.duracion_s_gate_humano:.1f}s")

        if nombre_fase == _FASE_01:
            registro = self.state.registro_requisitos
            if registro is not None:
                print(f"Requisitos funcionales: "
                      f"{len(registro.requisitos_funcionales)}")
                print(f"Requisitos no funcionales: "
                      f"{len(registro.requisitos_no_funcionales)}")
                print("Artefactos:")
                fase_dir = self.state.paths.fase_01_requisitos
                print(f"  {fase_dir / 'registro_requisitos.json'}")
                print(f"  {fase_dir / 'registro_requisitos.md'}")
        elif nombre_fase == _FASE_02:
            backlog = self.state.backlog
            plan = self.state.plan_sprints
            riesgos = self.state.riesgos
            if backlog is not None:
                print(f"Historias de usuario: {len(backlog.historias)}")
            if plan is not None:
                print(f"Sprints planificados: {len(plan.sprints)}")
            if riesgos is not None:
                print(f"Riesgos identificados: {len(riesgos.riesgos)}")
            if backlog is not None or plan is not None or riesgos is not None:
                print("Artefactos:")
                fase_dir = self.state.paths.fase_02_planificacion
                for nombre in ("backlog", "plan_sprints", "riesgos"):
                    print(f"  {fase_dir / f'{nombre}.json'}")
                    print(f"  {fase_dir / f'{nombre}.md'}")
        elif nombre_fase == _FASE_03:
            diseno = self.state.diseno_tecnico
            if diseno is not None:
                print(f"Apps Django: {len(diseno.apps_django)}")
                print(f"Modelos: {len(diseno.modelos)}")
                print(f"Rutas: {len(diseno.rutas)}")
                print("Artefactos:")
                fase_dir = self.state.paths.fase_03_arquitectura
                print(f"  {fase_dir / 'diseno_tecnico.json'}")
                print(f"  {fase_dir / 'diseno_tecnico.md'}")
        elif nombre_fase == _FASE_03B:
            entrega = self.state.entregas_sprint.get(0)
            if entrega is not None:
                print(f"Archivos de scaffold propuestos: {len(entrega.archivos)}")
            print("Artefactos:")
            fase_dir = self.state.paths.fase_03b_scaffold
            print(f"  {fase_dir / 'entrega_scaffold.json'}")
            print(f"  {fase_dir / 'scaffold_check.json'}")
            print(f"  {fase_dir / 'codigo'}")
        elif nombre_fase in (_FASE_04, _FASE_05, _FASE_06):
            numero_sprint = int(nombre_fase[:2]) - 3
            entrega = self.state.entregas_sprint.get(numero_sprint)
            review = self.state.reviews_sprint.get(numero_sprint)
            backlog_sprint = self.state.sprint_backlogs.get(numero_sprint)
            if backlog_sprint is not None:
                print(f"Historias del sprint: {len(backlog_sprint.historias)}")
            if entrega is not None:
                print(f"Archivos propuestos por el Desarrollador: "
                      f"{len(entrega.archivos)}")
            if review is not None:
                estados = review.cumplimiento.values()
                print(f"Historias ok: {sum(1 for e in estados if e == 'ok')}")
                estados = review.cumplimiento.values()
                print(f"Historias parciales: "
                      f"{sum(1 for e in estados if e == 'parcial')}")
                estados = review.cumplimiento.values()
                print(f"Historias ausentes: "
                      f"{sum(1 for e in estados if e == 'ausente')}")
                print(f"manage.py check OK: {review.arranque.ok}")
            print("Artefactos:")
            fase_dir = self._fase_dir_sprint(numero_sprint)
            print(f"  {fase_dir / f'backlog_sprint_{numero_sprint}.json'}")
            print(f"  {fase_dir / f'backlog_sprint_{numero_sprint}.md'}")
            print(f"  {fase_dir / f'entrega_sprint_{numero_sprint}.json'}")
            print(f"  {fase_dir / f'review_sprint_{numero_sprint}.json'}")
            print(f"  {fase_dir / f'review_sprint_{numero_sprint}.md'}")
            print(f"  {fase_dir / 'codigo'}")
        elif nombre_fase == _FASE_99:
            validacion = self.state.validacion_final
            if validacion is not None:
                print(f"Validacion final OK global: {validacion.ok_global}")
                print("Clasificacion: "
                      f"{validacion.review_final.clasificacion}")
                print("Incidencias detectadas: "
                      f"{len(validacion.review_final.incidencias)}")
                print("Checks ejecutados: "
                      f"{len(validacion.review_final.checks_ejecutados)}/"
                      f"{len(validacion.review_final.checks_planificados)}")
            print("Artefactos:")
            fase_dir = self.state.paths.fase_99_cierre
            print(f"  {fase_dir / 'validacion_final.json'}")
            print(f"  {fase_dir / 'review_final.md'}")

    # -----------------------------------------------------------------------
    # Helpers de fase 01
    # -----------------------------------------------------------------------

    def _kickoff_requisitos_con_gate_humano(self) -> None:
        """
        Orquesta fase 01 + gate humano hasta convergencia o agotamiento
        del presupuesto de regeneraciones.

        Estrategia:
          1. Genera el registro (con reintentos automáticos internos).
          2. Si la generación falla → state.resultado_final =
             'abortado_por_limite' y termina.
          3. Si la generación produce registro → escribe artefactos en
             disco y abre el gate humano.
          4. Según GateResult.decision:
             - aceptado → gate_decision='aceptado', termina (D.1: el
               resultado_final del Run lo decide cerrar_run al final).
             - abortado → resultado_final='abortado_en_gate', termina.
             - rechazado → si quedan regeneraciones, incrementa contador,
                           resetea reintentos automáticos a 0 y vuelve al 1
                           pasando GateResult.accion como feedback. Si no
                           quedan, resultado_final='abortado_por_limite'.

        Acumula `duracion_s_gate_humano` entre regeneraciones (decisión
        confirmada en 8c).
        """
        assert self.state.paths is not None  # garantizado por setup_run
        max_regeneraciones = _leer_max_regeneraciones_humanas()
        status = self.state.fases_status[_FASE_01]

        feedback_humano = ""

        while True:
            # ---- Paso 1: generar el registro -------------------------------
            registro, mensaje = self._kickoff_requisitos_con_reintentos(
                feedback_humano=feedback_humano,
            )

            if registro is None:
                # Reintentos automáticos agotados. No abrimos el gate.
                self.state.resultado_final = "abortado_por_limite"
                # gate_decision queda en su valor por defecto ("N/A"):
                # nunca llegamos a celebrar el gate.
                print(f"\n[Fase 01] {mensaje}")
                print(f"Artefactos parciales en: {self.state.paths.attempts}")
                return

            # ---- Paso 2: escribir artefactos canónicos ---------------------
            self.state.registro_requisitos = registro
            try:
                self._escribir_artefactos_requisitos(registro)
            except Exception as e:
                print(f"\n[Fase 01] Fallo al escribir artefactos: {e}")
                traceback.print_exc()
                self.state.resultado_final = "abortado_por_limite"
                return

            print(f"\n[Fase 01] {mensaje}")

            # ---- Paso 3: gate humano ---------------------------------------
            try:
                resultado_gate = human_gate(
                    fase=_FASE_01,
                    fase_dir=self.state.paths.fase_01_requisitos,
                    artefactos_md=[
                        self.state.paths.fase_01_requisitos / "registro_requisitos.md"
                    ],
                    numero_gate=1,
                    regeneraciones_consumidas=status.regeneraciones_humanas,
                    max_regeneraciones=max_regeneraciones,
                )
            except GateError as e:
                # Error técnico no recuperable (p.ej. fase_dir desaparecido).
                # No es decisión humana; lo tratamos como abortado_por_limite
                # con motivo técnico, igual que un fallo de I/O.
                print(f"\n[Gate 1] Error técnico: {e}")
                self.state.resultado_final = "abortado_por_limite"
                return

            # Acumulamos duración del gate (por decisión: sumamos entre
            # regeneraciones para reflejar tiempo humano total invertido).
            status.duracion_s_gate_humano += resultado_gate.duracion_s

            # ---- Paso 4: ramificar según la decisión -----------------------
            if resultado_gate.decision == "aceptado":
                # D.1 (cerrada en 8f): la rama "aceptado" solo marca el
                # gate_decision de la fase. El resultado_final del Run lo
                # decide cerrar_run cuando todas las fases hayan terminado
                # sin abortar ni bloquearse. Así fase 02 no necesita
                # rescatar resultado_final="completo" para arrancar.
                status.gate_decision = "aceptado"
                obs_resumen = (resultado_gate.observaciones or "").strip()
                if obs_resumen:
                    print(f"[Gate 1] Aceptado con observaciones: "
                          f"{obs_resumen[:200]}"
                          f"{'...' if len(obs_resumen) > 200 else ''}")
                else:
                    print("[Gate 1] Aceptado sin observaciones.")
                return

            if resultado_gate.decision == "abortado":
                status.gate_decision = "abortado"
                self.state.resultado_final = "abortado_en_gate"
                print("[Gate 1] Abortado por la operadora.")
                return

            # ---- Caso rechazado --------------------------------------------
            if resultado_gate.decision == "rechazado":
                if status.regeneraciones_humanas >= max_regeneraciones:
                    # Presupuesto agotado.
                    status.gate_decision = "rechazado"
                    self.state.resultado_final = "abortado_por_limite"
                    print(f"[Gate 1] Rechazado y presupuesto agotado "
                          f"({status.regeneraciones_humanas}/"
                          f"{max_regeneraciones} regeneraciones consumidas). "
                          f"Run abortado.")
                    return

                # Hay presupuesto: preparamos la siguiente regeneración.
                status.regeneraciones_humanas += 1
                # Reset de reintentos automáticos (decisión confirmada en 8c:
                # los dos contadores son independientes; cada regeneración
                # humana arranca con presupuesto fresco de auto-retries).
                status.reintentos_automaticos = 0
                feedback_humano = _formatear_feedback_humano(
                    resultado_gate=resultado_gate,
                    numero_regeneracion=status.regeneraciones_humanas,
                    max_regeneraciones=max_regeneraciones,
                )
                print(f"[Gate 1] Rechazado. Iniciando regeneración "
                      f"{status.regeneraciones_humanas}/{max_regeneraciones}...")
                continue

            # No debería llegar aquí: GateResult.decision es Literal.
            # Si llega, es bug del módulo del gate.
            raise RuntimeError(
                f"Decisión de gate desconocida: {resultado_gate.decision!r}"
            )

    def _kickoff_requisitos_con_reintentos(
        self,
        *,
        feedback_humano: str = "",
    ) -> tuple[Optional[RegistroRequisitos], str]:
        """
        Ejecuta la requisitos_crew con hasta `_MAX_REINTENTOS` intentos.
        No propaga excepciones: las traduce a (None, mensaje) si agota
        el presupuesto.

        Args:
            feedback_humano: bloque de texto a inyectar en el prompt vía
                el placeholder {feedback_humano} de tasks.yaml. En la
                primera generación es "" (placeholder inerte). En
                regeneraciones, contiene el bloque de instrucciones de
                la operadora del gate previo.
        """
        crew_obj = RequisitosCrew().crew()
        # NOTA: no usamos setdefault aquí — el slot ya existe (lo creó
        # `ejecutar_fase_01_requisitos`). Lo recuperamos y mutamos.
        status = self.state.fases_status[_FASE_01]

        ultimo_error: str = ""

        for intento in range(1, _MAX_REINTENTOS + 1):
            print(f"\n[Fase 01] Intento {intento}/{_MAX_REINTENTOS}...")
            t0 = time.monotonic()

            try:
                result = crew_obj.kickoff(
                    inputs={
                        "brief": self.state.brief_texto,
                        "run_id": self.state.run_id,
                        "feedback_humano": feedback_humano,
                    }
                )
            except Exception as e:
                ultimo_error = f"Excepción en kickoff: {type(e).__name__}: {e}"
                print(f"[Fase 01] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_01,
                    intento=intento,
                    error=ultimo_error,
                    raw="",
                )
                if _es_error_rate_limit(e) and intento < _MAX_REINTENTOS:
                    espera_s = _retry_after_s(e)
                    print(
                        f"[Fase 01] Rate limit del proveedor. "
                        f"Esperando {espera_s}s antes de reintentar..."
                    )
                    time.sleep(espera_s)
                continue

            status.duracion_s_ejec += time.monotonic() - t0

            registro = getattr(result, "pydantic", None)
            if not isinstance(registro, RegistroRequisitos):
                raw = getattr(result, "raw", "") or str(result)
                ultimo_error = (
                    "La salida de la crew no es un RegistroRequisitos "
                    f"(tipo recibido: {type(registro).__name__})."
                )
                print(f"[Fase 01] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_01,
                    intento=intento,
                    error=ultimo_error,
                    raw=raw,
                )
                continue

            try:
                validate_requisitos_contenido(registro)
            except ContenidoInsuficienteError as e:
                ultimo_error = f"Contenido insuficiente: {e}"
                print(f"[Fase 01] {ultimo_error}")
                status.reintentos_automaticos += 1
                self._guardar_intento_fallido(
                    nombre_fase=_FASE_01,
                    intento=intento,
                    error=ultimo_error,
                    raw=registro.model_dump_json(indent=2),
                )
                continue

            print(f"[Fase 01] Intento {intento} OK.")
            return registro, "Fase 01 completada correctamente."

        return None, (
            f"Fase 01 agotó {_MAX_REINTENTOS} reintentos. "
            f"Último error: {ultimo_error}"
        )

    def _guardar_intento_fallido(
        self,
        *,
        nombre_fase: str,
        intento: int,
        error: str,
        raw: str,
    ) -> None:
        """
        Guarda raw + error de un intento fallido en `_attempts/`.

        Generalizado en 8f (decisión b) para soportar múltiples fases. El
        prefijo del archivo deriva del nombre de la fase: '01_requisitos'
        → 'fase01', '02_planificacion' → 'fase02'. Así los attempts de
        cada fase no se pisan entre sí.
        """
        assert self.state.paths is not None
        # Prefijo del archivo: 'fase01', 'fase02', ... Construido como
        # 'fase' + los dos primeros caracteres del nombre_fase, que por
        # convención del proyecto son siempre dígitos ('01_', '02_').
        if nombre_fase == _FASE_03B:
            prefijo = "fase03b"
        else:
            prefijo = f"fase{nombre_fase[:2]}"
        # Suffix para no pisar attempts entre regeneraciones humanas.
        # Formato: <prefijo>_regen<N>_intento<M>.txt
        regen = self.state.fases_status[nombre_fase].regeneraciones_humanas
        archivo = (
            self.state.paths.attempts
            / f"{prefijo}_regen{regen}_intento{intento}.txt"
        )
        contenido = (
            f"# Intento fallido fase {nombre_fase}\n"
            f"# regeneración humana: {regen}\n"
            f"# intento dentro de la regeneración: {intento}\n"
            f"# error: {error}\n\n"
            f"---- raw ----\n"
            f"{raw}\n"
        )
        try:
            write_text(archivo, contenido)
        except Exception as e:
            # No queremos que un I/O del attempts mate la fase.
            print(f"[Fase {nombre_fase}] No se pudo guardar attempt: {e}")

    def _escribir_artefactos_requisitos(
        self,
        registro: RegistroRequisitos,
    ) -> None:
        """
        Escribe los artefactos canónicos de la fase 01 en disco:
          - registro_requisitos.json (fuente de verdad)
          - registro_requisitos.md   (con frontmatter, para el gate)

        Se llama tanto en la generación inicial como tras cada
        regeneración. Sobreescribe el contenido anterior: la fuente de
        verdad es el último intento aceptable (los previos quedan en
        `_attempts/` si se conservaron).
        """
        assert self.state.paths is not None
        fase_dir = self.state.paths.fase_01_requisitos

        # JSON canónico
        write_json(
            fase_dir / "registro_requisitos.json",
            registro.model_dump(),
        )

        # MD con frontmatter
        status = self.state.fases_status[_FASE_01]
        frontmatter = render_frontmatter(
            run_id=self.state.run_id,
            fase=_FASE_01,
            agente="Analista",
            modelo=get_model_name("default"),
            timestamp=now_iso_madrid(),
            hash_brief=self.state.hashes.brief,
            regeneraciones_previas=status.regeneraciones_humanas,
        )
        cuerpo = render_requisitos_md(registro)
        write_text(
            fase_dir / "registro_requisitos.md",
            frontmatter + cuerpo,
        )

    def _mensaje_resumen(self) -> str:
        """Texto corto del resumen del Run, para el run_summary.json."""
        return f"Run finalizado con resultado_final = {self.state.resultado_final}"

    def _escribir_resumen_run(self, mensaje: str) -> None:
        """
        Escribe `run_summary.json` con una síntesis operativa del Run.

        Reescrito en 8f (decisión E.2): el campo `fase_01` se sustituye
        por un dict `fases` con una entrada por fase del Run, alineándose
        con la estructura `fases[]` del manifest del Bloque 7. Cuando se
        enchufe fase 03, su FaseStatus aparecerá automáticamente sin
        tocar este método.
        """
        assert self.state.paths is not None

        fases_summary: dict[str, dict[str, object]] = {}
        duracion_s_ejec_total = 0.0
        duracion_s_gate_humano_total = 0.0
        for nombre_fase, status in self.state.fases_status.items():
            duracion_s_ejec_total += status.duracion_s_ejec
            duracion_s_gate_humano_total += status.duracion_s_gate_humano
            fases_summary[nombre_fase] = {
                "reintentos_automaticos": status.reintentos_automaticos,
                "regeneraciones_humanas": status.regeneraciones_humanas,
                "gate_decision": status.gate_decision,
                "duracion_s_ejec": status.duracion_s_ejec,
                "duracion_s_gate_humano": status.duracion_s_gate_humano,
            }

        summary = {
            "run_id": self.state.run_id,
            "resultado_final": self.state.resultado_final,
            "mensaje": mensaje,
            "timestamp_cierre": now_iso_madrid(),
            "fases": fases_summary,
            "duracion_s_ejec_total": duracion_s_ejec_total,
            "duracion_s_gate_humano_total": duracion_s_gate_humano_total,
            "duracion_s_total_contabilizada": (
                duracion_s_ejec_total + duracion_s_gate_humano_total
            ),
            "validacion_final": self._resumen_validacion_final(),
        }
        write_json(self.state.paths.root / "run_summary.json", summary)

    def _resumen_validacion_final(self) -> dict[str, object]:
        """Resumen compacto de la validacion final para `run_summary.json`."""
        validacion = self.state.validacion_final
        if validacion is None:
            return {
                "ejecutada": False,
                "ok_global": None,
                "clasificacion": None,
                "checks_planificados_total": 0,
                "checks_ejecutados_total": 0,
                "checks_no_ejecutados_total": 0,
                "incidencias_total": 0,
                "factores_bloqueantes_total": 0,
            }

        review = validacion.review_final
        return {
            "ejecutada": True,
            "ok_global": validacion.ok_global,
            "clasificacion": review.clasificacion,
            "checks_planificados_total": len(review.checks_planificados),
            "checks_ejecutados_total": len(review.checks_ejecutados),
            "checks_no_ejecutados_total": len(review.checks_no_ejecutados),
            "incidencias_total": len(review.incidencias),
            "factores_bloqueantes_total": len(review.factores_bloqueantes),
        }

    def _escribir_cierre_documental(self) -> None:
        """
        Escribe manifest y documentos de cierre deterministas.

        Si el cierre documental falla, no se silencia: se escriben artefactos
        mínimos de error en la carpeta de cierre y en logs/.
        """
        assert self.state.paths is not None
        fase_dir = ensure_dir(self.state.paths.fase_99_cierre)
        logs_dir = ensure_dir(self.state.paths.logs)

        try:
            manifest = construir_manifest(
                state=self.state,
                project_root=_PROJECT_ROOT,
                pipeline_specs_path=_PIPELINE_SPECS_PATH,
                pipeline_config_path=_PIPELINE_CONFIG_PATH,
            )
            write_json(self.state.paths.manifest, manifest)
            write_text(
                fase_dir / "readme.md",
                render_readme_cierre(state=self.state, manifest=manifest),
            )
            write_text(
                fase_dir / "lecciones_aprendidas.md",
                render_lecciones_aprendidas(state=self.state, manifest=manifest),
            )
            print(f"[Cierre] Manifest escrito en: {self.state.paths.manifest}")
            print(f"[Cierre] Documentos escritos en: {fase_dir}")
        except Exception as e:
            print(f"[Cierre] Error escribiendo cierre documental: {e}")
            traceback.print_exc()
            self._escribir_cierre_documental_error(
                fase_dir=fase_dir,
                logs_dir=logs_dir,
                error=e,
            )

    def _escribir_cierre_documental_error(
        self,
        *,
        fase_dir: Path,
        logs_dir: Path,
        error: Exception,
    ) -> None:
        """Escribe artefactos mínimos cuando falla el cierre documental."""
        assert self.state.paths is not None
        error_payload = {
            "tipo": type(error).__name__,
            "mensaje": str(error),
            "traceback": traceback.format_exc(),
        }
        manifest_error = {
            "schema_version": "manifest_error_v1",
            "generated_at": now_iso_madrid(),
            "run_id": self.state.run_id,
            "resultado_final": self.state.resultado_final,
            "error_cierre_documental": error_payload,
        }
        readme_error = (
            "# Cierre documental con error explícito\n\n"
            f"Run: `{self.state.run_id}`\n\n"
            f"Resultado final: `{self.state.resultado_final}`\n\n"
            "El cierre documental determinista no pudo completarse. "
            "Este archivo se escribe como fallback para dejar evidencia "
            "explícita del fallo.\n\n"
            f"**Error**: `{type(error).__name__}: {error}`\n"
        )
        lecciones_error = (
            "# Lecciones aprendidas no disponibles\n\n"
            "El documento de lecciones aprendidas no pudo generarse porque "
            "falló el cierre documental. Revisar `logs/cierre_documental_error.json`."
            "\n"
        )

        try:
            write_json(self.state.paths.manifest, manifest_error)
            write_text(fase_dir / "readme.md", readme_error)
            write_text(fase_dir / "lecciones_aprendidas.md", lecciones_error)
            write_json(logs_dir / "cierre_documental_error.json", error_payload)
            print(
                "[Cierre] Se escribieron artefactos fallback de cierre "
                f"en: {fase_dir}"
            )
        except Exception as fallback_error:
            print(
                "[Cierre] Fallo tambien el fallback documental: "
                f"{type(fallback_error).__name__}: {fallback_error}"
            )


# ===========================================================================
# Helpers a nivel de módulo
# ===========================================================================

def _fase_sprint(numero_sprint: int) -> str:
    """Nombre canónico de fase para un sprint."""
    if numero_sprint == 1:
        return _FASE_04
    if numero_sprint == 2:
        return _FASE_05
    if numero_sprint == 3:
        return _FASE_06
    raise ValueError(f"Sprint no soportado: {numero_sprint}")


def _formatear_feedback_humano(
    *,
    resultado_gate: GateResult,
    numero_regeneracion: int,
    max_regeneraciones: int,
) -> str:
    """
    Construye el bloque de texto que se inyecta en el prompt del Analista
    en una regeneración. Se delimita claramente para que el modelo lo
    perciba como instrucción adicional, no como parte del brief.

    Diseñado en 8c. Decisión metodológica: el feedback humano se añade
    al prompt original sin sustituirlo. Las reglas de cobertura,
    vocabulario y formato del tasks.yaml siguen vigentes; la operadora
    aporta correcciones específicas.
    """
    accion = (resultado_gate.accion or "").strip()
    observaciones = (resultado_gate.observaciones or "").strip()

    bloques: list[str] = []
    bloques.append(
        f"------ INSTRUCCIONES DE REGENERACIÓN (operadora humana) ------"
    )
    bloques.append(
        f"Esta es la regeneración {numero_regeneracion} de "
        f"{max_regeneraciones}. La generación anterior fue rechazada "
        f"en el gate humano."
    ) 
    if observaciones:
        bloques.append("")
        bloques.append("Observaciones de la operadora sobre la generación anterior:")
        bloques.append(observaciones)
    if accion:
        bloques.append("")
        bloques.append(
            "Corrige específicamente lo siguiente, sin perder cobertura "
            "del resto del brief:"
        )
        bloques.append(accion)
    bloques.append("")
    bloques.append("Mantén intactas todas las reglas del prompt original "
                   "(cobertura por subsecciones, vocabulario literal del "
                   "brief, esquema JSON estricto).")
    bloques.append("------ FIN INSTRUCCIONES DE REGENERACIÓN ------")

    return "\n".join(bloques)


def _build_run_id() -> str:
    """
    Construye el run_id con la zona horaria de Madrid.

    Resolución al minuto: dos Runs lanzados con menos de un minuto
    de diferencia colisionan. Asumible en PMV.
    """
    now = datetime.now(ZoneInfo("Europe/Madrid"))
    return f"run_{now.strftime('%Y-%m-%d_%H-%M')}"


def _exit_code_from_state(state: Caso02State) -> int:
    """Traduce el resultado_final del Run a exit code para el shell."""
    return 0 if state.resultado_final == "completo" else 1


# ===========================================================================
# Entry point — registrado en pyproject.toml como `pipeline.main:kickoff`
# ===========================================================================

def kickoff() -> int:
    """
    Punto de entrada del pipeline. Lo invoca tanto `crewai run` como
    `python -m pipeline.main`. Devuelve exit code (0 = OK, 1 = fallo).
    """
    flow = Caso02Flow()
    flow.kickoff()
    return _exit_code_from_state(flow.state)


if __name__ == "__main__":
    sys.exit(kickoff())
