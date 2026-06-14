from __future__ import annotations
from datetime import datetime


def display_artifacts(generated: dict) -> None:
    artifacts = generated.get("artifacts", [])
    print(f"\n{'═'*62}")
    print(f"  ARTEFACTOS GENERADOS ({len(artifacts)} archivos)")
    print(f"{'═'*62}")
    for art in artifacts:
        print(f"\n📄 [{art['type'].upper()}]  {art['name']}")
        print(f"   → {art['path']}")
        print(f"{'─'*50}")
        lines = art["content"].split("\n")
        preview = "\n".join(lines[:50])
        if len(lines) > 50:
            preview += f"\n  ... ({len(lines)-50} líneas más)"
        print(preview)
    print(f"\n{'═'*62}\n")


def display_validation(report: dict) -> None:
    print(f"\n{'═'*62}")
    print(f"  VALIDACIÓN DE CONTRATO — Sprint {report['sprint_id']}")
    print(f"{'═'*62}")

    if report["passed"]:
        print("  ✅ Sin violaciones de contrato detectadas.")
    else:
        print(f"  ❌ {len(report['violations'])} VIOLACIÓN(ES) DETECTADA(S):")
        for v in report["violations"]:
            print(f"     • {v}")

    if report.get("warnings"):
        print(f"\n  ⚠️  Advertencias ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"     • {w}")

    print(f"{'═'*62}\n")


def human_gate(sprint_id: str, validation_passed: bool) -> dict:
    """
    Gate bloqueante. Devuelve la decisión humana como dict.
    """
    print(f"{'═'*62}")
    print(f"  GATE HUMANO — Sprint {sprint_id}")
    print(f"{'═'*62}")

    if not validation_passed:
        print("  ⛔ Hay violaciones de contrato. No puedes aprobar.")
        print("  Opciones: [r] Re-generar   [a] Abortar")
        valid_choices = {"r", "a"}
    else:
        print("  Opciones: [y] Aprobar   [r] Re-generar   [a] Abortar")
        valid_choices = {"y", "r", "a"}

    while True:
        choice = input("\n  Tu decisión: ").strip().lower()
        if choice in valid_choices:
            break
        print(f"  Opción no válida. Elige entre: {', '.join(sorted(valid_choices))}")

    decision_map = {"y": "approved", "r": "regenerate", "a": "aborted"}
    return {
        "decision"        : decision_map[choice],
        "sprint_id"       : sprint_id,
        "timestamp"       : datetime.now().isoformat(timespec="seconds"),
        "validation_passed": validation_passed,
    }