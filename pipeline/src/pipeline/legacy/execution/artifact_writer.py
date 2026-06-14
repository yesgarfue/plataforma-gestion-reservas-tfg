import json
from pathlib import Path
from datetime import datetime

EXECUTION_BASE = Path("artifacts/execution")
# Estos paths son READ-ONLY. El writer nunca toca nada fuera de execution/
READ_ONLY_PATHS = [
    Path("artifacts/09_stack_y_restricciones.json"),
    Path("artifacts/09a_routes_required.json"),
    Path("artifacts/09b_domain_entities_required.json"),
    Path("artifacts/10_diseno_tecnico.json"),
    Path("artifacts/10a_sprint_contract_map.json"),
]

def assert_not_readonly(path: Path):
    resolved = path.resolve()
    for ro in READ_ONLY_PATHS:
        if resolved == ro.resolve():
            raise PermissionError(
                f"[ARTIFACT WRITER] Intento de escritura en archivo read-only: {path}\n"
                f"La fase de ejecución no puede modificar contratos congelados."
            )

def write_sprint_artifacts(
    sprint_id: str,
    generated: dict,
    approval: dict,
    report_dict: dict,
    project_root: Path = Path(".")
):
    """
    Escribe los artefactos generados al proyecto Django y al directorio de ejecución.
    Solo se llama si el humano aprobó.
    """
    sprint_dir = EXECUTION_BASE / sprint_id
    sprint_dir.mkdir(parents=True, exist_ok=True)

    # 1. Guardar artefactos generados en execution/sprint_xx/
    generated_path = sprint_dir / "12_generated_artifacts.json"
    assert_not_readonly(generated_path)
    generated_path.write_text(
        json.dumps(generated, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # 2. Guardar reporte de validación
    report_path = sprint_dir / "13_validation_report.json"
    assert_not_readonly(report_path)
    report_path.write_text(
        json.dumps(report_dict, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # 3. Guardar aprobación humana
    approval_path = sprint_dir / "14_sprint_approval.json"
    assert_not_readonly(approval_path)
    approval_path.write_text(
        json.dumps(approval, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # 4. Escribir los archivos reales al proyecto Django
    written_files = []
    for artifact in generated.get("artifacts", []):
        target = project_root / artifact["path"]
        assert_not_readonly(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(artifact["content"], encoding="utf-8")
        written_files.append(str(artifact["path"]))
        print(f"  ✓ Escrito: {target}")

    # 5. Actualizar log global
    _update_execution_log(sprint_id, approval, written_files)

def _update_execution_log(sprint_id: str, approval: dict, written_files: list):
    log_path = EXECUTION_BASE / "execution_log.json"
    log = []
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))

    log.append({
        "sprint_id": sprint_id,
        "timestamp": datetime.utcnow().isoformat(),
        "decision": approval["decision"],
        "written_files": written_files,
    })

    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")