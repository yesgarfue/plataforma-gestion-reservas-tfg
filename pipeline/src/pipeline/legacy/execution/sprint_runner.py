from __future__ import annotations

import os
import json
import re
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from crewai import Crew, Process
from crewai.flow.flow import Flow, and_, listen, start
from caso02.runner_exec import extract_freeze_id
from caso02.runner_exec import extract_sprint_block

# Rutas del proyecto
PROJECT_ROOT     = Path(__file__).resolve().parents[3]
OUTPUTS_JSON_DIR = PROJECT_ROOT / "outputs" / "json"
EXECUTION_DIR    = OUTPUTS_JSON_DIR / "execution"
ATTEMPTS_DIR     = PROJECT_ROOT / "outputs" / "_attempts"

# Imports internos
from caso02.runner_exec import ExecutionRunner          # reutilizamos el CLI existente
from caso02.execution.utils.freeze_guard import assert_freeze_valid
from caso02.execution.contract_validator import ContractValidator, ValidationReport
from caso02.execution.agents import (
    build_closed_prompt_context,
    create_developer_agent,
    create_frontend_agent,
    build_python_task,
    build_template_task,
)
from caso02.execution.human_gate import (
    display_artifacts,
    display_validation,
    human_gate,
)
from caso02.io_utils import strip_markdown_fences   # ya existe en tu proyecto


# ══════════════════════════════════════════════════════════════════════
# Estado del Flow
# ══════════════════════════════════════════════════════════════════════

class SprintState(BaseModel):
    sprint_id           : str  = ""
    sprint_contract     : dict = Field(default_factory=dict)
    stack               : dict = Field(default_factory=dict)
    routes_contract     : dict = Field(default_factory=dict)
    entities_contract   : dict = Field(default_factory=dict)
    sprint_type         : str  = "full"   # python_only | templates_only | full
    prompt_context      : str  = ""

    generated_python    : Optional[dict] = None
    generated_templates : Optional[dict] = None
    merged_artifacts    : dict = Field(default_factory=dict)
    validation_report   : dict = Field(default_factory=dict)

    human_decision      : str  = ""
    regeneration_count  : int  = 0
    MAX_REGENERATIONS   : int  = 2


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════

def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _parse_model_output(raw: str) -> dict:
    """
    Extrae JSON del output del modelo de forma robusta.
    El modelo a veces añade texto o fences markdown.
    """
    # Intento 1: parse directo
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Intento 2: strip fences (usa tu io_utils existente)
    try:
        return json.loads(strip_markdown_fences(raw))
    except (json.JSONDecodeError, Exception):
        pass

    # Intento 3: extraer el primer bloque {...} que sea JSON válido
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"[PARSER] No se pudo extraer JSON válido del output del modelo.\n"
        f"Primeros 500 chars:\n{raw[:500]}"
    )


def _run_generation_crew(task_factory, agent_factory) -> dict:
    """Ejecuta un Crew de un solo agente con retry sobre parse error."""
    agent = agent_factory()
    task  = task_factory(agent)
    crew  = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
    result = crew.kickoff()

    # Extraer raw del output
    raw = ""
    if getattr(task, "output", None):
        if getattr(task.output, "json_dict", None):
            return task.output.json_dict   # ya parseado
        raw = getattr(task.output, "raw", "") or str(result)
    else:
        raw = str(result)

    return _parse_model_output(raw)


# ══════════════════════════════════════════════════════════════════════
# Flow principal
# ══════════════════════════════════════════════════════════════════════

class SprintExecutionFlow(Flow[SprintState]):

    # ── 1. Carga y validación del freeze ──────────────────────────────

    @start()
    def load_and_validate_freeze(self):
        print(f"\n[SPRINT RUNNER] ▶ Iniciando sprint '{self.state.sprint_id}'...")

        # Cargar contratos base (read-only, nunca se escriben aquí)
        self.state.stack             = _load(OUTPUTS_JSON_DIR / "09_stack_y_restricciones.json")
        self.state.routes_contract   = _load(OUTPUTS_JSON_DIR / "09a_routes_required.json")
        self.state.entities_contract = _load(OUTPUTS_JSON_DIR / "09b_domain_entities_required.json")
        design_data                  = _load(OUTPUTS_JSON_DIR / "10_diseno_tecnico.json")
        sprint_map                   = _load(OUTPUTS_JSON_DIR / "10a_sprint_contract_map.json")

        # Verificar freeze (usa ExecutionRunner para extraer freeze_id del JSON)
        runner         = ExecutionRunner(OUTPUTS_JSON_DIR, PROJECT_ROOT)
        expected_fid = extract_freeze_id(design_data) or self.state.stack.get("freeze_id", "")
        assert_freeze_valid(expected_fid)

        # Extraer subcontrato del sprint (reutiliza runner_exec)
        sprint_num = int(self.state.sprint_id.replace("sprint_", ""))
        sprint_block = extract_sprint_block(sprint_map, sprint_num)
        sprint_block["freeze_id"] = expected_fid   # inyectar freeze_id en el subcontrato

        self.state.sprint_contract = sprint_block
        self.state.sprint_type     = sprint_block.get("type", "full")
        self.state.prompt_context  = build_closed_prompt_context(sprint_block, self.state.stack)

        # Guardar subcontrato derivado (artefacto 11)
        sprint_dir = EXECUTION_DIR / self.state.sprint_id
        _save(sprint_dir / "11_sprint_contract.json", sprint_block)
        print(f"[RUNNER] ✓ Subcontrato del sprint guardado en {sprint_dir / '11_sprint_contract.json'}")
        print(f"[RUNNER] Tipo de sprint: {self.state.sprint_type}")

    # ── 2a. Generación Python (rama paralela) ─────────────────────────

    @listen(load_and_validate_freeze)
    def generate_python_artifacts(self):
        if self.state.sprint_type not in ("python_only", "full"):
            print("[RUNNER] Sprint sin artefactos Python → rama omitida.")
            self.state.generated_python = {"artifacts": []}
            return

        print("[RUNNER] ▶ Generando artefactos Python con LLM...")

        ctx = self.state.prompt_context
        sc  = self.state.sprint_contract

        result = _run_generation_crew(
            task_factory  = lambda agent: build_python_task(agent, ctx, sc),
            agent_factory = create_developer_agent,
        )
        self.state.generated_python = result
        print(f"[RUNNER] ✓ Python: {len(result.get('artifacts', []))} artefactos generados.")

    # ── 2b. Generación Templates (rama paralela) ──────────────────────

    @listen(load_and_validate_freeze)
    def generate_templates(self):
        if self.state.sprint_type not in ("templates_only", "full"):
            print("[RUNNER] Sprint sin templates → rama omitida.")
            self.state.generated_templates = {"artifacts": []}
            return

        print("[RUNNER] ▶ Generando templates HTML con LLM...")

        ctx = self.state.prompt_context
        sc  = self.state.sprint_contract

        result = _run_generation_crew(
            task_factory  = lambda agent: build_template_task(agent, ctx, sc),
            agent_factory = create_frontend_agent,
        )
        self.state.generated_templates = result
        print(f"[RUNNER] ✓ Templates: {len(result.get('artifacts', []))} generados.")

    # ── 3. Merge + validación determinista ───────────────────────────

    @listen(and_(generate_python_artifacts, generate_templates))
    def validate_against_contract(self):
        print("[RUNNER] ▶ Ejecutando validación determinista...")

        all_artifacts = []
        if self.state.generated_python:
            all_artifacts.extend(self.state.generated_python.get("artifacts", []))
        if self.state.generated_templates:
            all_artifacts.extend(self.state.generated_templates.get("artifacts", []))

        self.state.merged_artifacts = {
            "sprint_id" : self.state.sprint_id,
            "artifacts" : all_artifacts,
        }

        validator = ContractValidator(
            sprint_contract  = self.state.sprint_contract,
            routes_contract  = self.state.routes_contract,
            entities_contract= self.state.entities_contract,
        )
        report: ValidationReport = validator.validate(self.state.merged_artifacts)
        self.state.validation_report = report.to_dict()

        # Guardar reporte (artefacto 13) — antes de mostrar al humano
        sprint_dir = EXECUTION_DIR / self.state.sprint_id
        _save(sprint_dir / "13_validation_report.json", self.state.validation_report)

        display_artifacts(self.state.merged_artifacts)
        display_validation(self.state.validation_report)

    # ── 4. Gate humano ────────────────────────────────────────────────

    @listen(validate_against_contract)
    def human_approval_gate(self):
        self._run_human_gate()

    def _run_human_gate(self):
        """
        Separado del listener para poder llamarlo recursivamente en re-generación.
        """
        approval = human_gate(
            sprint_id         = self.state.sprint_id,
            validation_passed = self.state.validation_report.get("passed", False),
        )
        self.state.human_decision = approval["decision"]

        if approval["decision"] == "approved":
            self._write_to_disk(approval)

        elif approval["decision"] == "regenerate":
            self.state.regeneration_count += 1
            if self.state.regeneration_count > self.state.MAX_REGENERATIONS:
                print(
                    f"\n[RUNNER] ⛔ Límite de re-generaciones alcanzado "
                    f"({self.state.MAX_REGENERATIONS}). Sprint abortado."
                )
                self.state.human_decision = "aborted"
                self._save_aborted(approval)
                return

            print(f"\n[RUNNER] Re-generando (intento {self.state.regeneration_count}/{self.state.MAX_REGENERATIONS})...")
            self.generate_python_artifacts()
            self.generate_templates()
            self.validate_against_contract()
            self._run_human_gate()

        else:  # aborted
            print(f"\n[RUNNER] Sprint '{self.state.sprint_id}' abortado por decisión humana.")
            self._save_aborted(approval)

    # ── 5. Escritura a disco (solo si aprobado) ───────────────────────

    def _write_to_disk(self, approval: dict):
        """
        Usa ExecutionRunner.apply_patch_set() para escribir archivos.
        Esto reutiliza la lógica de diff + validación ya existente en runner_exec.
        """
        sprint_dir = EXECUTION_DIR / self.state.sprint_id

        # Guardar aprobación (artefacto 14)
        _save(sprint_dir / "14_sprint_approval.json", approval)

        # Convertir artifacts al formato patch_set que espera runner_exec
        patch_set = _artifacts_to_patch_set(
            self.state.merged_artifacts,
            self.state.sprint_contract,
        )

        runner = ExecutionRunner(OUTPUTS_JSON_DIR, PROJECT_ROOT)

        # Snapshot antes
        before = runner.collect_repo_snapshot()

        # Aplicar (runner_exec ya valida rutas, permisos, etc.)
        runner.repo_root.mkdir(parents=True, exist_ok=True)
        changed = runner.apply_patch_set(patch_set)

        # Snapshot después + diff
        after = runner.collect_repo_snapshot()
        diff  = runner.diff_snapshots(before, after)

        # Cargar el manifest del sprint para el reporte
        manifest = _load(sprint_dir / "11_sprint_contract.json")
        manifest["doc_id"] = f"11_sprint_manifest_{self.state.sprint_id}"

        # Validar diff contra manifest
        diff_validation = runner.validate_repo_diff_against_manifest(manifest, diff)

        # Reporte de entrega (artefacto 14_delivery_report)
        delivery = runner.build_delivery_report(
            sprint_or_bootstrap_id = self.state.sprint_id,
            manifest    = manifest,
            patch_set   = patch_set,
            diff        = diff,
            validation  = diff_validation,
        )
        _save(sprint_dir / f"14_delivery_report_{self.state.sprint_id}.json", delivery)

        # Actualizar log global
        _update_log(self.state.sprint_id, approval, changed)

        print(f"\n[RUNNER] ✅ Sprint '{self.state.sprint_id}' completado.")
        print(f"  Archivos escritos: {len(changed)}")
        for f in changed:
            print(f"    ✓ {f}")

    def _save_aborted(self, approval: dict):
        sprint_dir = EXECUTION_DIR / self.state.sprint_id
        _save(sprint_dir / "14_sprint_approval.json", approval)
        _update_log(self.state.sprint_id, approval, [])


# ══════════════════════════════════════════════════════════════════════
# Helpers de conversión y log
# ══════════════════════════════════════════════════════════════════════

def _artifacts_to_patch_set(generated: dict, sprint_contract: dict) -> dict:
    """
    Convierte el output del modelo (formato artifacts[])
    al formato patch_set que espera runner_exec.apply_patch_set().
    """
    operations = []
    for art in generated.get("artifacts", []):
        operations.append({
            "op"     : "create",        # runner_exec soporta create/update
            "path"   : art["path"],
            "content": art["content"],
        })
    return {
        "sprint_id" : generated.get("sprint_id", sprint_contract.get("sprint_id")),
        "freeze_id" : sprint_contract.get("freeze_id"),
        "operations": operations,
    }


def _update_log(sprint_id: str, approval: dict, written: list) -> None:
    log_path = EXECUTION_DIR / "execution_log.json"
    log = []
    if log_path.exists():
        try:
            log = json.loads(log_path.read_text(encoding="utf-8"))
        except Exception:
            log = []
    log.append({
        "sprint_id"    : sprint_id,
        "timestamp"    : approval.get("timestamp"),
        "decision"     : approval["decision"],
        "written_files": written,
    })
    _save(log_path, log)


# ══════════════════════════════════════════════════════════════════════
# Entrypoint
# ══════════════════════════════════════════════════════════════════════

def run_sprint(sprint_id: str):
    flow = SprintExecutionFlow()
    flow.state.sprint_id = sprint_id
    flow.kickoff()
    print(f"\n[RUNNER] Flow finalizado. Decisión: {flow.state.human_decision}")

# DESPUÉS
def kickoff():
    """
    Entrypoint para crewai run.
    Uso en Windows:  $env:SPRINT_ID="sprint_01"; crewai run
    Uso en Linux:    SPRINT_ID=sprint_01 crewai run
    """
    sprint_id = os.environ.get("SPRINT_ID", "").strip()
    if not sprint_id:
        print(
            "[ERROR] Variable de entorno SPRINT_ID no definida.\n"
            "  Windows : $env:SPRINT_ID='sprint_01'; crewai run\n"
            "  Linux   : SPRINT_ID=sprint_01 crewai run"
        )
        sys.exit(1)
    print(f"[RUNNER] SPRINT_ID={sprint_id}")
    run_sprint(sprint_id)

if __name__ == "__main__":
    kickoff()