# scripts/verify_pipeline.py
"""
Script de verificación incremental del pipeline.

Se ejecuta con:  python scripts/verify_pipeline.py

Prueba importaciones y caminos de éxito/fallo de los módulos escritos
hasta el momento. Cada fase imprime OK o el error, y el script para en
el primer fallo para que se vea claro.
"""

from __future__ import annotations

import os
import sys
import traceback


def step(title: str) -> None:
    print(f"\n--- {title} ---")


def ok(msg: str = "") -> None:
    print(f"[OK] {msg}".rstrip())


def fail(msg: str, exc: Exception | None = None) -> None:
    print(f"[FAIL] {msg}")
    if exc is not None:
        traceback.print_exception(type(exc), exc, exc.__traceback__)
    sys.exit(1)


# ---------------------------------------------------------------------------
# 1. Importaciones básicas
# ---------------------------------------------------------------------------

step("1. Importar schemas y validators")
try:
    from pipeline.validation.schemas import (
        Backlog,
        BacklogSprint,
        ArchivoCodigo,
        ArranqueResult,
        DisenoTecnico,
        EntregaSprint,
        HistoriaUsuario,
        PlanSprints,
        RegistroRequisitos,
        RequisitoFuncional,
        RequisitoNoFuncional,
        ResultadoComando,
        ResultadoMigraciones,
        ResultadoRuta,
        ResultadoTemplate,
        ReviewSprint,
        ReviewFinal,
        Riesgo,
        Riesgos,
        ValidacionFinal,
        Sprint,
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
    from pipeline.utils.renderers import (
        render_backlog_md,
        render_backlog_sprint_md,
        render_diseno_tecnico_md,
        render_plan_sprints_md,
        render_requisitos_md,
        render_review_final_md,
        render_review_sprint_md,
        render_riesgos_md,
    )
    ok("Todos los módulos se importan")
except Exception as e:
    fail("No se pudo importar algún módulo", e)


# ---------------------------------------------------------------------------
# 2. Camino de fallo: requisitos insuficientes
# ---------------------------------------------------------------------------

step("2. Requisitos insuficientes → debe lanzar ContenidoInsuficienteError")
try:
    registro = RegistroRequisitos(
        id_ejecucion="run_test",
        requisitos_funcionales=[
            RequisitoFuncional(id="RF-01", descripcion="test", prioridad="Alta"),
        ],
        requisitos_no_funcionales=[
            RequisitoNoFuncional(
                id="RNF-01",
                categoria="Seguridad",
                condicion_metrica="x",
                prioridad="Alta",
            ),
        ],
    )
    validate_requisitos_contenido(registro)
    fail("No lanzó excepción: esperábamos ContenidoInsuficienteError")
except ContenidoInsuficienteError as e:
    ok(f"Excepción correcta: {str(e)[:180]}")
except Exception as e:
    fail("Excepción incorrecta", e)


# ---------------------------------------------------------------------------
# 3. Camino de éxito: plan de sprints bien formado sobre backlog mínimo
# ---------------------------------------------------------------------------

step("3. Plan de sprints válido contra backlog de 3 historias")
try:
    backlog = Backlog(
        id_ejecucion="run_test",
        historias=[
            HistoriaUsuario(
                id=f"HU-{i:02d}",
                titulo="título",
                descripcion="descripción",
                criterios_aceptacion=["criterio"],
                prioridad="Media",
                estimacion="M",
            )
            for i in range(1, 4)
        ],
    )
    plan = PlanSprints(
        id_ejecucion="run_test",
        sprints=[
            Sprint(numero=1, objetivo="o", historias_ids=["HU-01"], entregable_verificable="e"),
            Sprint(numero=2, objetivo="o", historias_ids=["HU-02"], entregable_verificable="e"),
            Sprint(numero=3, objetivo="o", historias_ids=["HU-03"], entregable_verificable="e"),
        ],
    )
    validate_plan_sprints_contenido(plan, backlog)
    ok("Plan de sprints válido")
except Exception as e:
    fail("El plan debería haber validado", e)


# ---------------------------------------------------------------------------
# 4. Camino de fallo: plan referencia historia inexistente
# ---------------------------------------------------------------------------

step("4. Plan con historia inventada → debe lanzar ContenidoInsuficienteError")
try:
    plan_malo = PlanSprints(
        id_ejecucion="run_test",
        sprints=[
            Sprint(numero=1, objetivo="o", historias_ids=["HU-01"], entregable_verificable="e"),
            Sprint(numero=2, objetivo="o", historias_ids=["HU-02"], entregable_verificable="e"),
            Sprint(numero=3, objetivo="o", historias_ids=["HU-99"], entregable_verificable="e"),
        ],
    )
    validate_plan_sprints_contenido(plan_malo, backlog)
    fail("No lanzó excepción: esperábamos que detectara HU-99 inventada y HU-03 sin cubrir")
except ContenidoInsuficienteError as e:
    ok(f"Excepción correcta: {str(e)[:180]}")
except Exception as e:
    fail("Excepción incorrecta", e)


# ---------------------------------------------------------------------------
# 5. Camino de éxito: render MD de un registro mínimo
# ---------------------------------------------------------------------------

step("5. Render MD de un RegistroRequisitos (mínimo, sin validar contenido)")
try:
    md = render_requisitos_md(registro)
    if "RF-01" in md and "RNF-01" in md and "| ID |" in md:
        ok(f"Markdown generado ({len(md)} caracteres), contiene RF-01, RNF-01 y cabecera de tabla")
    else:
        fail(f"Markdown generado pero sin los campos esperados. Preview:\n{md[:400]}")
except Exception as e:
    fail("Render falló", e)


# ---------------------------------------------------------------------------
# 6. Diseño técnico: falta "Django 3.2" en el stack
# ---------------------------------------------------------------------------

step("6. DisenoTecnico sin Django 3.2 → debe lanzar ContenidoInsuficienteError")
try:
    diseno = DisenoTecnico(
        id_ejecucion="run_test",
        stack=["Python", "SQLite", "PayPal"],  # falta Django 3.2 a propósito
        apps_django=[],
        modelos=[],
        rutas=[],
    )
    validate_diseno_tecnico_contenido(diseno)
    fail("No lanzó excepción: esperábamos que detectara la falta de 'Django 3.2'")
except ContenidoInsuficienteError as e:
    ok(f"Excepción correcta: {str(e)[:180]}")
except Exception as e:
    fail("Excepción incorrecta", e)


# ---------------------------------------------------------------------------
# 7. State: construcción básica y asignación de artefactos
# ---------------------------------------------------------------------------

step("7. Caso02State: construcción vacía, asignación de paths y artefactos")
try:
    from pathlib import Path

    from pipeline.state import Caso02State, build_run_paths, FaseStatus

    # Construcción vacía con defaults
    state = Caso02State()
    assert state.run_id == ""
    assert state.registro_requisitos is None
    assert state.resultado_final == "pendiente"

    # Asignar run_id y paths
    state.run_id = "run_test"
    state.paths = build_run_paths(Path("runs"), "run_test")
    assert state.paths.fase_01_requisitos == Path("runs/run_test/01_requisitos")
    assert state.paths.manifest == Path("runs/run_test/99_cierre/manifest.json")

    # Asignar un artefacto tipado (el `registro` ya lo creamos en el paso 2)
    state.registro_requisitos = registro
    assert state.registro_requisitos is not None
    assert len(state.registro_requisitos.requisitos_funcionales) == 1

    # Contador de fase
    state.fases_status["01_requisitos"] = FaseStatus(gate_decision="aceptado")
    assert state.fases_status["01_requisitos"].gate_decision == "aceptado"

    # `extra='forbid'` debe rechazar un campo inventado
    try:
        state.campo_inventado = 123  # type: ignore[attr-defined]
        fail("El state aceptó un campo inventado (extra='forbid' no está activo)")
    except Exception:
        pass  # esperado

    ok("State construido, rutas correctas, artefacto tipado asignado, extra='forbid' activo")
except Exception as e:
    fail("State falló", e)

# ---------------------------------------------------------------------------
# 8. LLM factory: perfiles Anthropic sin llamar al proveedor
# ---------------------------------------------------------------------------

step("8. llm_factory: perfiles default, pm, architect y developer sin llamar a proveedores")
try:
    from pipeline.utils.llm_factory import get_llm, get_model_name

    llm_default = get_llm("default")
    assert llm_default.model == "claude-haiku-4-5", (
        f"Modelo default inesperado: {llm_default.model}"
    )

    pm_model = get_model_name("pm")
    assert pm_model == "anthropic/claude-haiku-4-5", (
        f"Modelo PM inesperado: {pm_model}"
    )
    architect_model = get_model_name("architect")
    assert architect_model == "anthropic/claude-haiku-4-5", (
        f"Modelo Arquitecto inesperado: {architect_model}"
    )
    developer_model = get_model_name("developer")
    assert developer_model == "anthropic/claude-haiku-4-5", (
        f"Modelo Desarrollador inesperado: {developer_model}"
    )

    # Construir los LLM cloud no debe llamar a Anthropic ni consumir saldo.
    # Si ANTHROPIC_API_KEY no está en el entorno, CrewAI/Anthropic fallará
    # solo al hacer kickoff real.
    llm_pm = get_llm("pm")
    assert "claude-haiku-4-5" in llm_pm.model, (
        f"LLM PM inesperado: {llm_pm.model}"
    )
    llm_architect = get_llm("architect")
    assert "claude-haiku-4-5" in llm_architect.model, (
        f"LLM Arquitecto inesperado: {llm_architect.model}"
    )
    llm_developer = get_llm("developer")
    assert "claude-haiku-4-5" in llm_developer.model, (
        f"LLM Desarrollador inesperado: {llm_developer.model}"
    )

    ok(
        f"LLMs construidos: default={llm_default.model}, "
        f"pm={llm_pm.model}, architect={llm_architect.model}, "
        f"developer={llm_developer.model}"
    )
except Exception as e:
    fail("get_llm falló", e)


# ---------------------------------------------------------------------------
# 9. RequisitosCrew: instancia y construcción (sin kickoff)
# ---------------------------------------------------------------------------

step("9. RequisitosCrew: instanciación y Crew build sin ejecutar")
try:
    from pipeline.crews.requisitos_crew.requisitos_crew import RequisitosCrew

    crew_obj = RequisitosCrew()
    built = crew_obj.crew()
    # Debe tener 1 agente y 1 task
    assert len(built.agents) == 1, f"Esperaba 1 agente, hay {len(built.agents)}"
    assert len(built.tasks) == 1, f"Esperaba 1 task, hay {len(built.tasks)}"
    # El agente debe tener el role del YAML
    agent_role = built.agents[0].role
    assert "Analista" in agent_role, f"Role inesperado: {agent_role}"
    # La task debe tener output_pydantic apuntando a RegistroRequisitos
    task_output_type = built.tasks[0].output_pydantic
    assert task_output_type is not None, "La task no tiene output_pydantic"
    assert task_output_type.__name__ == "RegistroRequisitos", (
        f"output_pydantic incorrecto: {task_output_type.__name__}"
    )
    ok(f"Crew construido: 1 agente ({agent_role[:50]}...), 1 task con output_pydantic=RegistroRequisitos")
except Exception as e:
    fail("RequisitosCrew falló", e)

# ---------------------------------------------------------------------------
# 10. Caso02Flow: importación, instanciación y forma del grafo
# ---------------------------------------------------------------------------

step("10. Caso02Flow: importación, instanciación y forma del grafo")
try:
    from pipeline.main import Caso02Flow, kickoff as kickoff_fn

    # Instanciación: no debe consumir Ollama, no debe crear carpetas.
    flow = Caso02Flow()

    # CrewAI envuelve flow.state en un StateProxy que delega al modelo
    # Pydantic real. No comprobamos isinstance(state, Caso02State) por
    # ese wrapper; comprobamos que los campos esperados existen con
    # sus defaults y que extra='forbid' sigue activo.
    assert flow.state is not None, "El Flow no expone state."

    # Defaults heredados de Caso02State.
    assert flow.state.run_id == "", f"run_id por defecto inesperado: {flow.state.run_id!r}"
    assert flow.state.brief_texto == ""
    assert flow.state.paths is None
    assert flow.state.registro_requisitos is None
    assert flow.state.resultado_final == "pendiente", (
        f"resultado_final por defecto inesperado: {flow.state.resultado_final!r}"
    )
    # fases_status arranca como dict vacío (Field(default_factory=dict)).
    assert flow.state.fases_status == {}

    # extra='forbid' debe seguir activo aun a través del proxy.
    try:
        flow.state.campo_inventado = 123  # type: ignore[attr-defined]
        fail("El state aceptó un campo inventado a través del proxy")
    except Exception:
        pass  # esperado

    # Los pasos del Flow están definidos como atributos de la clase. En 8f
    # se enchufa fase 02 al grafo, así que ahora deben existir los cuatro.
    for nombre_metodo in (
        "setup_run",
        "ejecutar_fase_01_requisitos",
        "ejecutar_fase_02_planificacion",
        "ejecutar_fase_03_arquitectura",
        "ejecutar_sprint_1",
        "ejecutar_sprint_2",
        "ejecutar_sprint_3",
        "cerrar_run",
    ):
        assert hasattr(Caso02Flow, nombre_metodo), (
            f"Caso02Flow no tiene el método {nombre_metodo}"
        )

    # La función `kickoff` módulo-nivel existe y es invocable.
    # No la llamamos: invocaría el Flow real y arrancaría Ollama.
    assert callable(kickoff_fn), "pipeline.main.kickoff no es invocable"

    ok("Caso02Flow instanciado, state con defaults correctos, extra='forbid' activo, métodos presentes (incl. sprints), kickoff exportado")
except Exception as e:
    fail("Caso02Flow falló", e)

# ---------------------------------------------------------------------------
# 11. human_gate: cinco caminos (aceptado, rechazado válido, rechazado sin
#     acción, decisión inválida, abort directo) sin input humano real.
#
#     8f: la firma del gate cambió a `artefactos_md: list[Path]` para
#     soportar el gate 2 sobre los tres MD de planificación. Aquí se
#     prueba pasando una lista de un solo elemento, que es como queda
#     la llamada para gates con un único artefacto (gate 1, gate 3).
# ---------------------------------------------------------------------------

step("11. human_gate: parser y validación sin input humano (firma 8f con lista)")
try:
    import builtins
    import tempfile
    from pathlib import Path

    from pipeline.gates.human_gate import human_gate, GateError

    # ----- Helper: monkeypatch de input con respuestas pre-cargadas -----
    class _InputQueue:
        """
        Reemplazo de builtins.input que devuelve respuestas en orden.
        Si se agotan, lanza AssertionError (significa que el gate pidió
        más inputs de los previstos por el test).
        """
        def __init__(self, respuestas):
            self._iter = iter(respuestas)

        def __call__(self, prompt=""):  # firma compatible con input()
            try:
                return next(self._iter)
            except StopIteration:
                raise AssertionError(
                    "El gate pidió más inputs de los esperados por el test."
                )

    # ----- Helper: escribe gate_humano.md en una carpeta temporal -----
    def _escribir_gate(fase_dir: Path, contenido: str) -> None:
        (fase_dir / "gate_humano.md").write_text(contenido, encoding="utf-8")

    # Plantillas mínimas
    GATE_ACEPTADO = """---
gate: 1
fase: 01_requisitos
timestamp_inicio: 2026-05-08T12:03:00+02:00
timestamp_fin: 2026-05-08T12:18:00+02:00
decision: aceptado
---

## Observaciones

Cobertura buena de la sección 3 del brief.

## Acción

Aceptado. Continuar a fase 02.
"""

    GATE_RECHAZADO_OK = """---
gate: 1
fase: 01_requisitos
timestamp_inicio: 2026-05-07T23:50:00+02:00
timestamp_fin: 2026-05-08T00:05:00+02:00
decision: rechazado
---

## Observaciones

RNF-04 invierte el sentido del brief sobre contraseñas.

## Acción

Regenerar respetando que las contraseñas no se almacenan en texto plano.
"""

    GATE_RECHAZADO_SIN_ACCION = """---
gate: 1
fase: 01_requisitos
timestamp_inicio: 2026-05-08T10:00:00+02:00
timestamp_fin: 2026-05-08T10:05:00+02:00
decision: rechazado
---

## Observaciones

Falta cobertura de la sección 4.

## Acción

"""

    GATE_DECISION_INVALIDA = """---
gate: 1
fase: 01_requisitos
timestamp_inicio: 2026-05-08T10:00:00+02:00
timestamp_fin: 2026-05-08T10:05:00+02:00
decision: maybe
---

## Observaciones

texto

## Acción

texto
"""

    # Guardamos el input original para restaurarlo siempre.
    _input_original = builtins.input

    try:
        # ---- 11.a: aceptado ----
        with tempfile.TemporaryDirectory() as tmp:
            fase_dir = Path(tmp)
            _escribir_gate(fase_dir, GATE_ACEPTADO)
            builtins.input = _InputQueue(["ok"])
            res = human_gate(
                fase="01_requisitos",
                fase_dir=fase_dir,
                artefactos_md=[fase_dir / "registro_requisitos.md"],
                numero_gate=1,
                regeneraciones_consumidas=0,
            )
            assert res.decision == "aceptado", res.decision
            assert "sección 3" in res.observaciones
            assert res.accion is not None and "fase 02" in res.accion

        # ---- 11.b: rechazado con acción válida ----
        with tempfile.TemporaryDirectory() as tmp:
            fase_dir = Path(tmp)
            _escribir_gate(fase_dir, GATE_RECHAZADO_OK)
            builtins.input = _InputQueue(["ok"])
            res = human_gate(
                fase="01_requisitos",
                fase_dir=fase_dir,
                artefactos_md=[fase_dir / "registro_requisitos.md"],
                numero_gate=1,
                regeneraciones_consumidas=1,
            )
            assert res.decision == "rechazado", res.decision
            assert res.accion is not None and "texto plano" in res.accion

        # ---- 11.c: rechazado sin acción → reentra y aceptamos abort ----
        with tempfile.TemporaryDirectory() as tmp:
            fase_dir = Path(tmp)
            _escribir_gate(fase_dir, GATE_RECHAZADO_SIN_ACCION)
            # Primer 'ok' falla validación, segundo turno aborta limpio.
            builtins.input = _InputQueue(["ok", "abort"])
            res = human_gate(
                fase="01_requisitos",
                fase_dir=fase_dir,
                artefactos_md=[fase_dir / "registro_requisitos.md"],
                numero_gate=1,
                regeneraciones_consumidas=0,
            )
            assert res.decision == "abortado", res.decision

        # ---- 11.d: decisión inválida → reentra y aceptamos abort ----
        with tempfile.TemporaryDirectory() as tmp:
            fase_dir = Path(tmp)
            _escribir_gate(fase_dir, GATE_DECISION_INVALIDA)
            builtins.input = _InputQueue(["ok", "abort"])
            res = human_gate(
                fase="01_requisitos",
                fase_dir=fase_dir,
                artefactos_md=[fase_dir / "registro_requisitos.md"],
                numero_gate=1,
                regeneraciones_consumidas=0,
            )
            assert res.decision == "abortado", res.decision

        # ---- 11.e: abort directo sin tocar disco ----
        with tempfile.TemporaryDirectory() as tmp:
            fase_dir = Path(tmp)
            # OJO: no escribimos gate_humano.md. abort no debe leerlo.
            builtins.input = _InputQueue(["abort"])
            res = human_gate(
                fase="01_requisitos",
                fase_dir=fase_dir,
                artefactos_md=[fase_dir / "registro_requisitos.md"],
                numero_gate=1,
                regeneraciones_consumidas=0,
            )
            assert res.decision == "abortado", res.decision
            assert res.observaciones == ""
            assert res.accion is None

        # ---- 11.f: fase_dir inexistente → GateError (no recuperable) ----
        builtins.input = _InputQueue([])  # no debe pedir input siquiera
        try:
            human_gate(
                fase="01_requisitos",
                fase_dir=Path("/_no_existe_seguro_seguro_"),
                artefactos_md=[Path("/_no_existe_seguro_seguro_/x.md")],
                numero_gate=1,
                regeneraciones_consumidas=0,
            )
            fail("human_gate aceptó un fase_dir inexistente")
        except GateError:
            pass  # esperado

        # ---- 11.g: artefactos_md vacío → GateError (defensa de la nueva firma) ----
        with tempfile.TemporaryDirectory() as tmp:
            fase_dir = Path(tmp)
            builtins.input = _InputQueue([])  # no debe pedir input
            try:
                human_gate(
                    fase="01_requisitos",
                    fase_dir=fase_dir,
                    artefactos_md=[],
                    numero_gate=1,
                    regeneraciones_consumidas=0,
                )
                fail("human_gate aceptó artefactos_md vacío")
            except GateError:
                pass  # esperado

    finally:
        builtins.input = _input_original

    ok("human_gate: 5 caminos OK + GateError por fase_dir inválido + GateError por lista vacía")
except Exception as e:
    fail("human_gate falló", e)


# ---------------------------------------------------------------------------
# 12. Fase 02: PlanificacionCrew, métodos de Caso02Flow, listener de
#     cerrar_run, y _recoger_outputs_planificacion con CrewOutput mock.
#
#     No ejecuta kickoff (no consume Ollama). Solo verifica construcción
#     estática del grafo y la lógica de recogida por isinstance (B.2).
# ---------------------------------------------------------------------------

step("12. Fase 02: PlanificacionCrew, Caso02Flow ampliado, _recoger_outputs_planificacion")
try:
    from types import SimpleNamespace

    from pipeline.crews.planificacion_crew.planificacion_crew import (
        PlanificacionCrew,
    )
    from pipeline.main import Caso02Flow

    # ---- 12.a: PlanificacionCrew se construye con 1 agente y 3 tasks ----
    plan_crew_obj = PlanificacionCrew()
    plan_built = plan_crew_obj.crew()

    assert len(plan_built.agents) == 1, (
        f"PlanificacionCrew: esperaba 1 agente, hay {len(plan_built.agents)}"
    )
    assert "claude-haiku-4-5" in plan_built.agents[0].llm.model, (
        f"El PM debe usar Anthropic Haiku; usa {plan_built.agents[0].llm.model}"
    )
    pm_role = plan_built.agents[0].role
    # El agente del YAML 8d se ancla al rol de PM. Comprobamos que su rol
    # menciona "PM" o "Project Manager" (criterio laxo, los YAML pueden
    # variar el casing).
    assert ("PM" in pm_role) or ("Project Manager" in pm_role.title()), (
        f"Role del agente PM inesperado: {pm_role}"
    )

    assert len(plan_built.tasks) == 3, (
        f"PlanificacionCrew: esperaba 3 tasks, hay {len(plan_built.tasks)}"
    )

    # ---- 12.b: orden de tasks por output_pydantic (decisión P12-A) ----
    # El orden importa: _kickoff_planificacion_con_reintentos asume que
    # las tres tasks producen tipos distintos para que el isinstance los
    # distinga. Si dos tasks compartiesen output_pydantic la recogida por
    # isinstance fallaría con "duplicado".
    output_types = [t.output_pydantic for t in plan_built.tasks]
    nombres_tipos = [tt.__name__ if tt is not None else "None" for tt in output_types]
    assert nombres_tipos == ["Backlog", "PlanSprints", "Riesgos"], (
        f"Orden o tipos de output_pydantic inesperados: {nombres_tipos}. "
        f"Esperado: ['Backlog', 'PlanSprints', 'Riesgos']."
    )

    # ---- 12.c: Caso02Flow tiene los helpers de fase 02 ----
    helpers_fase_02 = (
        "_kickoff_planificacion_con_gate_humano",
        "_kickoff_planificacion_con_reintentos",
        "_recoger_outputs_planificacion",
        "_escribir_artefactos_planificacion",
        "_imprimir_resumen_fase",
    )
    for nombre in helpers_fase_02:
        assert hasattr(Caso02Flow, nombre), (
            f"Caso02Flow no tiene el helper {nombre}"
        )

    # ---- 12.d: _recoger_outputs_planificacion con mock SimpleNamespace ----
    # Probamos que la recogida por isinstance funciona en orden cualquiera.
    flow = Caso02Flow()

    # Construimos los tres modelos mínimos válidos.
    backlog_mock = Backlog(
        id_ejecucion="run_test",
        historias=[
            HistoriaUsuario(
                id="HU-01",
                titulo="t",
                descripcion="d",
                criterios_aceptacion=["c"],
                prioridad="Media",
                estimacion="M",
            ),
        ],
    )
    plan_mock = PlanSprints(
        id_ejecucion="run_test",
        sprints=[
            Sprint(numero=1, objetivo="o", historias_ids=["HU-01"], entregable_verificable="e"),
        ],
    )
    riesgos_mock = Riesgos(
        id_ejecucion="run_test",
        riesgos=[
            Riesgo(
                id="R-01",
                descripcion="d",
                probabilidad="media",
                impacto="medio",
                mitigacion="m",
            ),
        ],
    )

    # 12.d.1: orden natural (Backlog, Plan, Riesgos)
    fake_result_natural = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=backlog_mock),
            SimpleNamespace(pydantic=plan_mock),
            SimpleNamespace(pydantic=riesgos_mock),
        ]
    )
    b, p, r = flow._recoger_outputs_planificacion(fake_result_natural)
    assert b is backlog_mock and p is plan_mock and r is riesgos_mock, (
        "Recogida en orden natural falló"
    )

    # 12.d.2: orden invertido (Riesgos, Plan, Backlog) — debe seguir funcionando
    fake_result_invertido = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=riesgos_mock),
            SimpleNamespace(pydantic=plan_mock),
            SimpleNamespace(pydantic=backlog_mock),
        ]
    )
    b, p, r = flow._recoger_outputs_planificacion(fake_result_invertido)
    assert b is backlog_mock and p is plan_mock and r is riesgos_mock, (
        "Recogida en orden invertido falló (B.2 debería ser orden-agnóstico)"
    )

    # 12.d.3: duplicado de Backlog → devuelve (None, None, None)
    fake_result_dup = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=backlog_mock),
            SimpleNamespace(pydantic=backlog_mock),  # duplicado intencional
            SimpleNamespace(pydantic=riesgos_mock),
        ]
    )
    b, p, r = flow._recoger_outputs_planificacion(fake_result_dup)
    assert (b, p, r) == (None, None, None), (
        f"Recogida con duplicado debía devolver (None, None, None), devolvió: "
        f"({type(b).__name__}, {type(p).__name__}, {type(r).__name__})"
    )

    # 12.d.4: una task con .pydantic = None → devuelve (None, ...) parcial
    # _recoger_outputs salta los None pero el llamante chequea que los
    # tres slots se rellenen. Aquí debe faltar PlanSprints.
    fake_result_none = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=backlog_mock),
            SimpleNamespace(pydantic=None),
            SimpleNamespace(pydantic=riesgos_mock),
        ]
    )
    b, p, r = flow._recoger_outputs_planificacion(fake_result_none)
    assert b is backlog_mock and p is None and r is riesgos_mock, (
        f"Recogida con un .pydantic None inesperada: "
        f"({type(b).__name__}, {type(p).__name__}, {type(r).__name__})"
    )

    # 12.d.5: tasks_output ausente → (None, None, None)
    fake_result_vacio = SimpleNamespace(tasks_output=[])
    b, p, r = flow._recoger_outputs_planificacion(fake_result_vacio)
    assert (b, p, r) == (None, None, None), (
        "Recogida con tasks_output vacío debía devolver (None, None, None)"
    )

    ok("Fase 02 OK: PlanificacionCrew (1 agente PM + 3 tasks ordenadas), "
       "5 helpers presentes, _recoger_outputs robusto a 5 escenarios")
except Exception as e:
    fail("Fase 02 falló", e)


# ---------------------------------------------------------------------------
# 13. Fase 03: ArquitecturaCrew, Caso02Flow ampliado,
#     render_diseno_tecnico_md y _recoger_output_arquitectura.
#
#     No ejecuta kickoff real ni llama al modelo cloud. Verifica que la
#     fase 03 queda enchufada mecánicamente al Flow y que el output único
#     se recoge por isinstance, manteniendo la defensa B.2.
# ---------------------------------------------------------------------------

step("13. Fase 03: ArquitecturaCrew, Caso02Flow ampliado, renderer y recogida")
try:
    from types import SimpleNamespace

    from pipeline.crews.arquitectura_crew.arquitectura_crew import (
        ArquitecturaCrew,
    )
    from pipeline.main import Caso02Flow

    # ---- 13.a: ArquitecturaCrew se construye con 1 agente y 1 task ----
    arch_crew_obj = ArquitecturaCrew()
    arch_built = arch_crew_obj.crew()

    assert len(arch_built.agents) == 1, (
        f"ArquitecturaCrew: esperaba 1 agente, hay {len(arch_built.agents)}"
    )
    assert "claude-haiku-4-5" in arch_built.agents[0].llm.model, (
        f"El Arquitecto debe usar Anthropic Haiku; usa "
        f"{arch_built.agents[0].llm.model}"
    )
    architect_role = arch_built.agents[0].role
    assert "Arquitecto" in architect_role, (
        f"Role del agente Arquitecto inesperado: {architect_role}"
    )

    assert len(arch_built.tasks) == 1, (
        f"ArquitecturaCrew: esperaba 1 task, hay {len(arch_built.tasks)}"
    )
    task_output_type = arch_built.tasks[0].output_pydantic
    assert task_output_type is not None, "La task de arquitectura no tiene output_pydantic"
    assert task_output_type.__name__ == "DisenoTecnico", (
        f"output_pydantic incorrecto: {task_output_type.__name__}"
    )

    # ---- 13.b: Caso02Flow tiene listener y helpers de fase 03 ----
    helpers_fase_03 = (
        "ejecutar_fase_03_arquitectura",
        "_kickoff_arquitectura_con_gate_humano",
        "_kickoff_arquitectura_con_reintentos",
        "_recoger_output_arquitectura",
        "_escribir_artefactos_arquitectura",
    )
    for nombre in helpers_fase_03:
        assert hasattr(Caso02Flow, nombre), (
            f"Caso02Flow no tiene el helper/método {nombre}"
        )

    # ---- 13.c: render_diseno_tecnico_md cubre las secciones esperadas ----
    diseno_mock = DisenoTecnico(
        id_ejecucion="run_test",
        stack=[
            "Python con Django 3.2 como framework web.",
            "SQLite como base de datos.",
            "PayPal Sandbox para pagos.",
        ],
        apps_django=[
            {
                "nombre": "catalog",
                "proposito": "Gestionar catálogo y ficha de barco.",
                "archivos_principales": [
                    "catalog/models.py",
                    "catalog/views.py",
                    "templates/catalog/list.html",
                ],
            }
        ],
        modelos=[
            {
                "nombre": "Barco",
                "app": "catalog",
                "campos": [
                    "nombre: CharField(max_length=120)",
                    "precio_dia: DecimalField(max_digits=8, decimal_places=2)",
                ],
            }
        ],
        rutas=[
            {
                "path": "/barcos/",
                "name": "catalog:barco_list",
                "metodo": "GET",
                "auth": "public",
                "vista": "BarcoListView",
            }
        ],
    )
    md_diseno = render_diseno_tecnico_md(diseno_mock)
    for texto in (
        "# 03",
        "Stack",
        "Apps Django",
        "Modelos",
        "Rutas",
        "catalog:barco_list",
    ):
        assert texto in md_diseno, (
            f"render_diseno_tecnico_md no contiene {texto!r}. Preview:\n"
            f"{md_diseno[:400]}"
        )

    # ---- 13.d: _recoger_output_arquitectura con mocks ----
    flow = Caso02Flow()

    fake_result_task = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=diseno_mock),
        ]
    )
    recogido = flow._recoger_output_arquitectura(fake_result_task)
    assert recogido is diseno_mock, "Recogida desde tasks_output falló"

    fake_result_directo = SimpleNamespace(
        tasks_output=[],
        pydantic=diseno_mock,
    )
    recogido = flow._recoger_output_arquitectura(fake_result_directo)
    assert recogido is diseno_mock, "Recogida directa desde result.pydantic falló"

    fake_result_dup = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=diseno_mock),
            SimpleNamespace(pydantic=diseno_mock),
        ]
    )
    recogido = flow._recoger_output_arquitectura(fake_result_dup)
    assert recogido is None, "Recogida con DisenoTecnico duplicado debía devolver None"

    fake_result_none = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=None),
        ]
    )
    recogido = flow._recoger_output_arquitectura(fake_result_none)
    assert recogido is None, "Recogida con .pydantic None debía devolver None"

    ok("Fase 03 OK: ArquitecturaCrew (1 agente + 1 task), helpers presentes, "
       "renderer activo y _recoger_output robusto a 4 escenarios")
except Exception as e:
    fail("Fase 03 falló", e)


# ---------------------------------------------------------------------------
# 14. Backlogs por sprint: derivación determinista tras Gate 3.
#
#     No usa LLM ni ejecuta un Run real. Verifica que el builder aplica la
#     partición aceptada en PlanSprints, conserva las historias del Backlog y
#     falla rápido ante planes inconsistentes.
# ---------------------------------------------------------------------------

step("14. Backlogs por sprint: builder determinista, renderer y helper Flow")
try:
    from pipeline.main import Caso02Flow
    from pipeline.utils.sprint_backlog_builder import derivar_sprint_backlogs

    backlog_derivacion = Backlog(
        id_ejecucion="run_test",
        historias=[
            HistoriaUsuario(
                id="HU-01",
                titulo="Catálogo público",
                descripcion="Como visitante quiero consultar barcos disponibles.",
                criterios_aceptacion=["Se muestra un listado de barcos."],
                prioridad="Alta",
                estimacion="M",
            ),
            HistoriaUsuario(
                id="HU-02",
                titulo="Ficha de barco",
                descripcion="Como visitante quiero ver el detalle de un barco.",
                criterios_aceptacion=["La ficha muestra precio y descripción."],
                prioridad="Alta",
                estimacion="M",
            ),
            HistoriaUsuario(
                id="HU-03",
                titulo="Reserva",
                descripcion="Como cliente quiero reservar un barco.",
                criterios_aceptacion=["La reserva queda registrada."],
                prioridad="Alta",
                estimacion="L",
            ),
            HistoriaUsuario(
                id="HU-04",
                titulo="Pago",
                descripcion="Como cliente quiero pagar una reserva.",
                criterios_aceptacion=["El pago se confirma en Sandbox."],
                prioridad="Media",
                estimacion="L",
            ),
        ],
    )
    plan_derivacion = PlanSprints(
        id_ejecucion="run_test",
        sprints=[
            Sprint(
                numero=1,
                objetivo="Base ejecutable y catálogo.",
                historias_ids=["HU-01", "HU-02"],
                entregable_verificable="Proyecto Django arranca y muestra catálogo.",
            ),
            Sprint(
                numero=2,
                objetivo="Reserva funcional.",
                historias_ids=["HU-03"],
                entregable_verificable="Flujo básico de reserva.",
            ),
            Sprint(
                numero=3,
                objetivo="Pago y cierre.",
                historias_ids=["HU-04"],
                entregable_verificable="Pago Sandbox integrado.",
            ),
        ],
    )

    sprint_backlogs = derivar_sprint_backlogs(
        backlog=backlog_derivacion,
        plan=plan_derivacion,
        run_id="run_test",
    )
    assert len(sprint_backlogs) == 3, (
        f"Esperaba 3 BacklogSprint, recibí {len(sprint_backlogs)}"
    )
    assert all(isinstance(item, BacklogSprint) for item in sprint_backlogs), (
        "La derivación no devuelve instancias BacklogSprint"
    )
    assert [item.numero_sprint for item in sprint_backlogs] == [1, 2, 3], (
        "Los BacklogSprint no están ordenados por número de sprint"
    )
    assert [[h.id for h in item.historias] for item in sprint_backlogs] == [
        ["HU-01", "HU-02"],
        ["HU-03"],
        ["HU-04"],
    ], "La partición de historias por sprint no coincide con el plan"

    md_sprint_1 = render_backlog_sprint_md(sprint_backlogs[0])
    for texto in ("Sprint 1", "HU-01", "HU-02", "Catálogo público"):
        assert texto in md_sprint_1, (
            f"render_backlog_sprint_md no contiene {texto!r}. Preview:\n"
            f"{md_sprint_1[:400]}"
        )

    plan_duplicado = PlanSprints(
        id_ejecucion="run_test",
        sprints=[
            Sprint(numero=1, objetivo="o", historias_ids=["HU-01"], entregable_verificable="e"),
            Sprint(numero=2, objetivo="o", historias_ids=["HU-01", "HU-03"], entregable_verificable="e"),
            Sprint(numero=3, objetivo="o", historias_ids=["HU-02", "HU-04"], entregable_verificable="e"),
        ],
    )
    try:
        derivar_sprint_backlogs(
            backlog=backlog_derivacion,
            plan=plan_duplicado,
            run_id="run_test",
        )
        fail("No detectó una historia duplicada entre sprints")
    except ValueError as e:
        assert "HU-01" in str(e), (
            f"Error por duplicado inesperado: {e}"
        )

    plan_inexistente = PlanSprints(
        id_ejecucion="run_test",
        sprints=[
            Sprint(numero=1, objetivo="o", historias_ids=["HU-01", "HU-02"], entregable_verificable="e"),
            Sprint(numero=2, objetivo="o", historias_ids=["HU-03"], entregable_verificable="e"),
            Sprint(numero=3, objetivo="o", historias_ids=["HU-99"], entregable_verificable="e"),
        ],
    )
    try:
        derivar_sprint_backlogs(
            backlog=backlog_derivacion,
            plan=plan_inexistente,
            run_id="run_test",
        )
        fail("No detectó una historia inexistente en el plan")
    except ValueError as e:
        assert "HU-99" in str(e), (
            f"Error por historia inexistente inesperado: {e}"
        )

    assert hasattr(Caso02Flow, "_derivar_sprint_backlogs"), (
        "Caso02Flow no tiene el helper _derivar_sprint_backlogs"
    )

    ok("Subpaso 1b OK: BacklogSprint, builder determinista, renderer y helper Flow")
except Exception as e:
    fail("Backlogs por sprint fallaron", e)


# ---------------------------------------------------------------------------
# 15. DesarrolloCrew aislada: agente Desarrollador, task única y contrato
#     EntregaSprint.
#
#     No integra los sprints al Flow ni ejecuta kickoff real. Verifica que
#     la crew se construye, que usa el perfil developer y que el contrato
#     mínimo de archivos detecta entregas inválidas.
# ---------------------------------------------------------------------------

step("15. DesarrolloCrew aislada: agente, task y contrato EntregaSprint")
try:
    from pipeline.crews.desarrollo_crew.desarrollo_crew import DesarrolloCrew

    entrega_valida = EntregaSprint(
        id_ejecucion="run_test",
        numero_sprint=1,
        archivos=[
            ArchivoCodigo(
                path="manage.py",
                contenido="import os\nimport sys\n",
            ),
            ArchivoCodigo(
                path="hundidos/settings.py",
                contenido="SECRET_KEY = 'test'\nINSTALLED_APPS = []\n",
            ),
            ArchivoCodigo(
                path="hundidos/urls.py",
                contenido="from django.urls import path\nurlpatterns = []\n",
            ),
        ],
    )
    validate_entrega_sprint_contenido(entrega_valida)

    entrega_path_invalido = EntregaSprint(
        id_ejecucion="run_test",
        numero_sprint=1,
        archivos=[
            ArchivoCodigo(path="../manage.py", contenido="x"),
            ArchivoCodigo(path="hundidos/settings.py", contenido="x"),
            ArchivoCodigo(path="hundidos/urls.py", contenido="x"),
        ],
    )
    try:
        validate_entrega_sprint_contenido(entrega_path_invalido)
        fail("No detectó una ruta fuera de codigo/")
    except ContenidoInsuficienteError as e:
        assert "../manage.py" in str(e), (
            f"Error por ruta inválida inesperado: {e}"
        )

    entrega_sprint_2_incremental = EntregaSprint(
        id_ejecucion="run_test",
        numero_sprint=2,
        archivos=[
            ArchivoCodigo(path="reservations/models.py", contenido="x"),
        ],
    )
    validate_entrega_sprint_contenido(entrega_sprint_2_incremental)

    entrega_marcadores_vacios = EntregaSprint(
        id_ejecucion="run_test",
        numero_sprint=2,
        archivos=[
            ArchivoCodigo(path="catalog/__init__.py", contenido=""),
            ArchivoCodigo(path="static/.gitkeep", contenido=""),
        ],
    )
    validate_entrega_sprint_contenido(
        entrega_marcadores_vacios,
        require_base_django=False,
    )

    entrega_funcional_vacia = EntregaSprint(
        id_ejecucion="run_test",
        numero_sprint=2,
        archivos=[
            ArchivoCodigo(path="catalog/views.py", contenido=""),
        ],
    )
    try:
        validate_entrega_sprint_contenido(
            entrega_funcional_vacia,
            require_base_django=False,
        )
        fail("No detectÃ³ un archivo funcional vacÃ­o")
    except ContenidoInsuficienteError as e:
        assert "catalog/views.py" in str(e), (
            f"Error por archivo funcional vacÃ­o inesperado: {e}"
        )

    entrega_sprint_1_sin_base = EntregaSprint(
        id_ejecucion="run_test",
        numero_sprint=1,
        archivos=[
            ArchivoCodigo(path="catalog/models.py", contenido="x"),
        ],
    )
    try:
        validate_entrega_sprint_contenido(entrega_sprint_1_sin_base)
        fail("No detectó la falta de archivos base Django en sprint 1")
    except ContenidoInsuficienteError as e:
        assert "manage.py" in str(e) and "settings.py" in str(e), (
            f"Error por base Django incompleta inesperado: {e}"
        )

    desarrollo_crew_obj = DesarrolloCrew()
    desarrollo_built = desarrollo_crew_obj.crew()

    assert len(desarrollo_built.agents) == 1, (
        f"DesarrolloCrew: esperaba 1 agente, hay {len(desarrollo_built.agents)}"
    )
    assert "claude-haiku-4-5" in desarrollo_built.agents[0].llm.model, (
        f"El Desarrollador debe usar Anthropic Haiku; usa "
        f"{desarrollo_built.agents[0].llm.model}"
    )
    developer_role = desarrollo_built.agents[0].role
    assert "Desarrollador" in developer_role, (
        f"Role del agente Desarrollador inesperado: {developer_role}"
    )

    assert len(desarrollo_built.tasks) == 1, (
        f"DesarrolloCrew: esperaba 1 task, hay {len(desarrollo_built.tasks)}"
    )
    task_output_type = desarrollo_built.tasks[0].output_pydantic
    assert task_output_type is not None, "La task de desarrollo no tiene output_pydantic"
    assert task_output_type.__name__ == "EntregaSprint", (
        f"output_pydantic incorrecto: {task_output_type.__name__}"
    )

    ok("Subpaso 1c OK: DesarrolloCrew (1 agente + 1 task), perfil developer "
       "y validate_entrega_sprint_contenido activos")
except Exception as e:
    fail("DesarrolloCrew falló", e)


# ---------------------------------------------------------------------------
# 16. Validación de arranque y review automático determinista.
#
#     No requiere Django instalado ni .venv_Test operativo: fuerza
#     DJANGO_CHECK_PYTHON al intérprete que ejecuta este script y usa un
#     manage.py mínimo de prueba para comprobar que el runner captura
#     returncode/stdout/stderr y que el review clasifica historias cubiertas
#     o ausentes según señales en código.
# ---------------------------------------------------------------------------

step("16. Arranque post-sprint y review automático determinista")
try:
    import tempfile
    from pathlib import Path

    from pipeline.utils.django_runner import ejecutar_manage_check
    from pipeline.utils.review_builder import construir_review_sprint

    django_check_python_anterior = os.environ.get("DJANGO_CHECK_PYTHON")
    os.environ["DJANGO_CHECK_PYTHON"] = sys.executable

    with tempfile.TemporaryDirectory() as tmp:
        codigo_dir = Path(tmp) / "codigo"
        codigo_dir.mkdir(parents=True)

        (codigo_dir / "manage.py").write_text(
            "import sys\n"
            "if __name__ == '__main__' and sys.argv[1:] == ['check']:\n"
            "    print('System check identified no issues (0 silenced).')\n"
            "    raise SystemExit(0)\n"
            "raise SystemExit(1)\n",
            encoding="utf-8",
        )
        (codigo_dir / "catalog").mkdir()
        (codigo_dir / "catalog" / "views.py").write_text(
            "def catalogo_barcos_listado(request):\n"
            "    # catálogo barcos listado disponible\n"
            "    return None\n",
            encoding="utf-8",
        )

        arranque = ejecutar_manage_check(codigo_dir, timeout_s=10)
        assert isinstance(arranque, ArranqueResult), (
            "ejecutar_manage_check no devuelve ArranqueResult"
        )
        assert arranque.ok is True, (
            f"manage.py check de prueba debía ser OK: {arranque}"
        )
        assert arranque.returncode == 0, (
            f"returncode inesperado: {arranque.returncode}"
        )
        assert "System check" in arranque.stdout_resumen, (
            f"stdout no capturado: {arranque.stdout_resumen}"
        )

        backlog_review = BacklogSprint(
            id_ejecucion="run_test",
            numero_sprint=1,
            historias=[
                HistoriaUsuario(
                    id="HU-01",
                    titulo="Catálogo de barcos",
                    descripcion="Como visitante quiero consultar barcos disponibles.",
                    criterios_aceptacion=["Se muestra un listado de barcos."],
                    prioridad="Alta",
                    estimacion="M",
                ),
                HistoriaUsuario(
                    id="HU-02",
                    titulo="Pago PayPal",
                    descripcion="Como cliente quiero pagar una reserva con PayPal.",
                    criterios_aceptacion=["El pago queda confirmado."],
                    prioridad="Media",
                    estimacion="L",
                ),
            ],
        )

        review = construir_review_sprint(
            sprint_backlog=backlog_review,
            codigo_dir=codigo_dir,
            arranque=arranque,
        )
        assert isinstance(review, ReviewSprint), (
            "construir_review_sprint no devuelve ReviewSprint"
        )
        assert review.cumplimiento["HU-01"] == "ok", (
            f"HU-01 debía quedar ok; quedó {review.cumplimiento['HU-01']}"
        )
        assert review.cumplimiento["HU-02"] == "ausente", (
            f"HU-02 debía quedar ausente; quedó {review.cumplimiento['HU-02']}"
        )
        assert "catalog/views.py" in review.archivos_entregados, (
            f"Archivos inspeccionados inesperados: {review.archivos_entregados}"
        )

        md_review = render_review_sprint_md(review)
        for texto in ("Review automático", "HU-01", "HU-02", "catalog/views.py"):
            assert texto in md_review, (
                f"render_review_sprint_md no contiene {texto!r}. Preview:\n"
                f"{md_review[:500]}"
            )

        arranque_sin_manage = ejecutar_manage_check(Path(tmp) / "sin_manage", timeout_s=10)
        assert arranque_sin_manage.ok is False, (
            "La ausencia de manage.py/codigo_dir debía quedar como ok=False"
        )

        os.environ["DJANGO_CHECK_PYTHON"] = str(Path(tmp) / "python_inexistente.exe")
        arranque_python_inexistente = ejecutar_manage_check(codigo_dir, timeout_s=10)
        assert arranque_python_inexistente.ok is False, (
            "Un DJANGO_CHECK_PYTHON inexistente debía quedar como ok=False"
        )
        assert "DJANGO_CHECK_PYTHON" in arranque_python_inexistente.stderr_resumen, (
            "El error por interprete inexistente debe mencionar DJANGO_CHECK_PYTHON"
        )

    if django_check_python_anterior is None:
        os.environ.pop("DJANGO_CHECK_PYTHON", None)
    else:
        os.environ["DJANGO_CHECK_PYTHON"] = django_check_python_anterior

    ok("Subpaso 1d OK: ejecutar_manage_check, ReviewSprint, heurística de cobertura "
       "y renderer activos")
except Exception as e:
    fail("Review automático falló", e)


# ---------------------------------------------------------------------------
# 17. Integración estática de sprints en Caso02Flow.
#
#     No ejecuta LLM ni corre un Run real. Verifica que existen los listeners
#     de sprint, los helpers principales, la recogida defensiva de
#     EntregaSprint y la protección de rutas dentro de codigo/.
# ---------------------------------------------------------------------------

step("17. Sprints integrados al Flow: listeners, helpers y recogida")
try:
    from types import SimpleNamespace
    import tempfile
    from pathlib import Path

    from pipeline.main import Caso02Flow
    from pipeline.state import build_run_paths

    helpers_sprints = (
        "ejecutar_scaffold_base",
        "_ejecutar_scaffold_base",
        "_kickoff_scaffold_con_reintentos",
        "ejecutar_sprint_1",
        "ejecutar_sprint_2",
        "ejecutar_sprint_3",
        "_ejecutar_sprint",
        "ejecutar_validacion_final",
        "_kickoff_sprint_con_reintentos",
        "_recoger_output_desarrollo",
        "_preparar_codigo_sprint",
        "_escribir_y_aplicar_entrega_sprint",
        "_escribir_y_aplicar_entrega",
        "_escribir_review_sprint",
        "_serializar_codigo_para_llm",
        "_resolver_path_codigo",
        "_codigo_tiene_base_django",
    )
    for nombre in helpers_sprints:
        assert hasattr(Caso02Flow, nombre), (
            f"Caso02Flow no tiene el método/helper {nombre}"
        )

    flow = Caso02Flow()
    entrega_mock = EntregaSprint(
        id_ejecucion="run_test",
        numero_sprint=1,
        archivos=[
            ArchivoCodigo(path="manage.py", contenido="x"),
            ArchivoCodigo(path="hundidos/settings.py", contenido="x"),
            ArchivoCodigo(path="hundidos/urls.py", contenido="x"),
        ],
    )

    fake_result_task = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=entrega_mock),
        ]
    )
    recogida = flow._recoger_output_desarrollo(fake_result_task)
    assert recogida is entrega_mock, "Recogida de EntregaSprint desde tasks_output falló"

    fake_result_directo = SimpleNamespace(
        tasks_output=[],
        pydantic=entrega_mock,
    )
    recogida = flow._recoger_output_desarrollo(fake_result_directo)
    assert recogida is entrega_mock, "Recogida directa de EntregaSprint falló"

    fake_result_dup = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=entrega_mock),
            SimpleNamespace(pydantic=entrega_mock),
        ]
    )
    recogida = flow._recoger_output_desarrollo(fake_result_dup)
    assert recogida is None, "Recogida con EntregaSprint duplicada debía devolver None"

    fake_result_none = SimpleNamespace(
        tasks_output=[
            SimpleNamespace(pydantic=None),
        ]
    )
    recogida = flow._recoger_output_desarrollo(fake_result_none)
    assert recogida is None, "Recogida con .pydantic None debía devolver None"

    with tempfile.TemporaryDirectory() as tmp:
        runs_dir = Path(tmp) / "runs"
        flow.state.run_id = "run_test"
        flow.state.paths = build_run_paths(runs_dir, "run_test")

        codigo_scaffold = flow.state.paths.fase_03b_scaffold / "codigo"
        (codigo_scaffold / "hundidos").mkdir(parents=True)
        (codigo_scaffold / "manage.py").write_text("print('scaffold')\n", encoding="utf-8")
        (codigo_scaffold / "hundidos" / "settings.py").write_text("SECRET_KEY='x'\n", encoding="utf-8")
        (codigo_scaffold / "hundidos" / "urls.py").write_text("urlpatterns=[]\n", encoding="utf-8")

        flow._preparar_codigo_sprint(1)
        codigo_sprint_1 = flow.state.paths.fase_04_sprint_1 / "codigo"
        assert (codigo_sprint_1 / "manage.py").exists(), (
            "Sprint 1 no copiÃ³ codigo/ desde 03b_scaffold"
        )
        assert flow._codigo_tiene_base_django(codigo_sprint_1) is True, (
            "La detecciÃ³n de base Django en codigo/ de Sprint 1 debÃ­a ser True"
        )

        codigo_1 = flow.state.paths.fase_04_sprint_1 / "codigo"
        (codigo_1 / "manage.py").write_text("print('s1')\n", encoding="utf-8")

        flow._preparar_codigo_sprint(2)
        codigo_2 = flow.state.paths.fase_05_sprint_2 / "codigo"
        assert (codigo_2 / "manage.py").exists(), (
            "Sprint 2 no copió codigo/ del sprint 1"
        )

        destino = flow._resolver_path_codigo(codigo_2, "app/models.py")
        assert destino.name == "models.py", (
            f"Ruta válida resuelta de forma inesperada: {destino}"
        )
        try:
            flow._resolver_path_codigo(codigo_2, "../escape.py")
            fail("No bloqueó una ruta con .. fuera de codigo/")
        except ValueError:
            pass

        resumen_codigo = flow._serializar_codigo_para_llm(codigo_2)
        assert "manage.py" in resumen_codigo and "s1" in resumen_codigo, (
            f"Serialización de código inesperada: {resumen_codigo[:200]}"
        )

    ok("Subpaso 1e estático OK: listeners de sprint, copia incremental, "
       "recogida defensiva y rutas seguras")
except Exception as e:
    fail("Integración estática de sprints falló", e)


# ---------------------------------------------------------------------------
# 18. Validacion final deterministica aislada.
# ---------------------------------------------------------------------------

step("18. Validacion final deterministica aislada")
try:
    import tempfile
    from pathlib import Path

    from pipeline.utils.final_validator import construir_validacion_final

    django_check_python_anterior = os.environ.get("DJANGO_CHECK_PYTHON")
    os.environ["DJANGO_CHECK_PYTHON"] = sys.executable

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        codigo_dir = root / "codigo"
        salida_dir = root / "99_cierre"
        app_dir = codigo_dir / "catalog"
        migrations_dir = app_dir / "migrations"
        commands_dir = codigo_dir / "core" / "management" / "commands"
        app_dir.mkdir(parents=True)
        migrations_dir.mkdir(parents=True)
        commands_dir.mkdir(parents=True)

        (app_dir / "models.py").write_text(
            "from django.db import models\n\n"
            "class Barco(models.Model):\n"
            "    nombre = models.CharField(max_length=120)\n",
            encoding="utf-8",
        )
        (migrations_dir / "__init__.py").write_text("", encoding="utf-8")
        (migrations_dir / "0001_initial.py").write_text("# fake migration\n", encoding="utf-8")
        (commands_dir / "seed_data.py").write_text("# fake command\n", encoding="utf-8")

        (codigo_dir / "manage.py").write_text(
            "import http.server\n"
            "import sys\n"
            "\n"
            "args = sys.argv[1:]\n"
            "if args == ['check']:\n"
            "    print('System check identified no issues (0 silenced).')\n"
            "    raise SystemExit(0)\n"
            "if args == ['migrate', '--noinput']:\n"
            "    print('migrated')\n"
            "    raise SystemExit(0)\n"
            "if args == ['seed_data']:\n"
            "    print('seeded')\n"
            "    raise SystemExit(0)\n"
            "if args[:2] == ['shell', '-c']:\n"
            "    raise SystemExit(0)\n"
            "if args and args[0] == 'runserver':\n"
            "    host, port = args[1].split(':')\n"
            "    class Handler(http.server.BaseHTTPRequestHandler):\n"
            "        def do_GET(self):\n"
            "            self.send_response(200)\n"
            "            self.end_headers()\n"
            "            self.wfile.write(b'ok')\n"
            "        def log_message(self, *a):\n"
            "            pass\n"
            "    http.server.HTTPServer((host, int(port)), Handler).serve_forever()\n"
            "raise SystemExit(1)\n",
            encoding="utf-8",
        )

        validacion = construir_validacion_final(
            id_ejecucion="run_test",
            codigo_dir=codigo_dir,
            salida_dir=salida_dir,
            timeout_s=10,
            runserver_timeout_s=10,
        )

        assert isinstance(validacion, ValidacionFinal), (
            "construir_validacion_final no devuelve ValidacionFinal"
        )
        assert validacion.ok_global is True, (
            f"La validacion fake debia ser OK: {validacion.review_final.incidencias}"
        )
        assert validacion.migraciones.ok is True, (
            f"Migraciones inesperadas: {validacion.migraciones}"
        )
        assert "check" in validacion.review_final.checks_ejecutados
        assert "migrate" in validacion.review_final.checks_ejecutados
        assert "ruta:/barcos/" in validacion.review_final.checks_ejecutados
        assert validacion.review_final.clasificacion == "apto_para_revision_funcional"

        md_final = render_review_final_md(validacion)
        for texto in ("Review final", "run_test", "checks", "/barcos/"):
            assert texto in md_final, (
                f"render_review_final_md no contiene {texto!r}. Preview:\n"
                f"{md_final[:500]}"
            )

    if django_check_python_anterior is None:
        os.environ.pop("DJANGO_CHECK_PYTHON", None)
    else:
        os.environ["DJANGO_CHECK_PYTHON"] = django_check_python_anterior

    ok("Validacion final aislada OK: JSON, review final y checks comparables")
except Exception as e:
    fail("Validacion final aislada fallo", e)


print("\n=== Todas las verificaciones pasaron ===")
