from __future__ import annotations
import argparse
from pathlib import Path
from caso02.execution.exec_core import (
    apply_model_output,
    assert_execution_preconditions,
    build_change_request,
    build_execution_prompt,
    build_implementation_report,
    build_paths,
    build_validation_report,
    check_changed_files_against_packet,
    derive_sprint_packet,
    diff_snapshots,
    ensure_repo_bootstrap,
    infer_project_package,
    load_contracts,
    load_model_output,
    run_light_local_checks,
    save_attempt_prompt,
    save_execution_outputs,
    snapshot_repo,
)

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="runner_exec",
        description="Runner mínimo de ejecución por sprint.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("bootstrap", help="Materializa repo_target desde el freeze aprobado.")

    packet = sub.add_parser("packet", help="Genera el sprint execution packet.")
    packet.add_argument("--sprint", required=True, help="ID del sprint. Ej: S1")

    sprint = sub.add_parser("sprint", help="Ejecuta un sprint o prepara dry-run.")
    sprint.add_argument("--sprint", required=True, help="ID del sprint. Ej: S1")
    sprint.add_argument("--attempt", type=int, default=1, help="Número de intento.")
    sprint.add_argument("--dry-run", action="store_true", help="Solo genera packet + prompt.")
    sprint.add_argument(
        "--from-json",
        type=str,
        default=None,
        help="Ruta al JSON de salida del modelo con file_writes.",
    )

    status = sub.add_parser("status", help="Muestra el último estado guardado.")
    status.add_argument("--sprint", required=True, help="ID del sprint. Ej: S1")

    return parser

def cmd_bootstrap() -> None:
    paths = build_paths(Path(__file__))
    contracts = load_contracts(paths)
    manifest = ensure_repo_bootstrap(paths, contracts)
    print(f"[OK] Bootstrap completado en: {paths.repo_target_dir}")
    print(f"[OK] project_package: {manifest.project_package}")
    print(f"[OK] apps: {', '.join(manifest.apps_to_create) if manifest.apps_to_create else '(ninguna)'}")

def cmd_packet(sprint_id: str) -> None:
    paths = build_paths(Path(__file__))
    contracts = load_contracts(paths)
    assert_execution_preconditions(contracts, sprint_id)
    packet = derive_sprint_packet(paths, contracts, sprint_id)
    saved = save_execution_outputs(paths, packet)
    print(f"[OK] Packet generado: {saved['packet']}")

def cmd_sprint(sprint_id: str, attempt_no: int, dry_run: bool, from_json: str | None) -> None:
    paths = build_paths(Path(__file__))
    contracts = load_contracts(paths)
    assert_execution_preconditions(contracts, sprint_id)

    ensure_repo_bootstrap(paths, contracts)
    project_package = infer_project_package(paths, contracts)

    packet = derive_sprint_packet(paths, contracts, sprint_id)
    prompt = build_execution_prompt(packet)
    prompt_path = save_attempt_prompt(paths, sprint_id, attempt_no, prompt)

    if dry_run or not from_json:
        saved = save_execution_outputs(paths, packet)
        print(f"[OK] Packet generado: {saved['packet']}")
        print(f"[OK] Prompt generado: {prompt_path}")
        print("[STOP] Dry-run terminado. Ahora pasa la salida del modelo con --from-json.")
        return

    model_output = load_model_output(Path(from_json))
    if model_output.freeze_id != packet.freeze_id:
        raise ValueError("freeze_id del output del modelo no coincide con el packet.")
    if model_output.sprint_id != packet.sprint_id:
        raise ValueError("sprint_id del output del modelo no coincide con el packet.")

    before = snapshot_repo(paths.repo_target_dir)
    touched_files = apply_model_output(paths.repo_target_dir, model_output)
    after = snapshot_repo(paths.repo_target_dir)

    changed_files = diff_snapshots(before, after)
    unexpected_files = check_changed_files_against_packet(changed_files, packet)
    local_checks = run_light_local_checks(paths, project_package=project_package)

    impl_report = build_implementation_report(packet, model_output, touched_files, attempt_no)
    validation_report = build_validation_report(
        packet,
        changed_files,
        unexpected_files,
        local_checks,
        needs_change_request=model_output.needs_change_request,
    )
    change_request = build_change_request(packet, model_output) if model_output.needs_change_request else None

    saved = save_execution_outputs(paths, packet, impl_report, validation_report, change_request)

    print(f"[OK] Prompt: {prompt_path}")
    print(f"[OK] Implementation report: {saved.get('implementation_report')}")
    print(f"[OK] Validation report: {saved.get('validation_report')}")
    if change_request is not None:
        print(f"[WARN] Change request: {saved.get('change_request')}")
    print(f"[STATUS] {validation_report.status} - {validation_report.summary}")

def cmd_status(sprint_id: str) -> None:
    paths = build_paths(Path(__file__))
    state_path = paths.status_dir / f"execution_state_{sprint_id}.json"
    if not state_path.exists():
        print(f"[INFO] No existe estado para {sprint_id}: {state_path}")
        return

    print(f"[OK] Estado: {state_path}")
    print(state_path.read_text(encoding="utf-8"))

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "bootstrap":
        cmd_bootstrap()
        return
    if args.command == "packet":
        cmd_packet(args.sprint)
        return
    if args.command == "sprint":
        cmd_sprint(args.sprint, args.attempt, args.dry_run, args.from_json)
        return
    if args.command == "status":
        cmd_status(args.sprint)
        return

    parser.error("Comando no soportado.")


if __name__ == "__main__":
    main()