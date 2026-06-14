from __future__ import annotations
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DESIGN_FILE  = PROJECT_ROOT / "outputs" / "json" / "10_diseno_tecnico.json"


def assert_freeze_valid(expected_freeze_id: str) -> str:
    """
    Verifica que 10_diseno_tecnico.json existe y que el freeze_id
    que contiene coincide con el que se pasó como referencia.
    """
    if not DESIGN_FILE.exists():
        raise RuntimeError(
            f"[FREEZE GUARD] No existe: {DESIGN_FILE}\n"
            "¿Ejecutaste la fase Dev antes de la fase de Ejecución?"
        )

    data = json.loads(DESIGN_FILE.read_text(encoding="utf-8"))
    actual = str(data.get("freeze_id", "")).strip()

    if not actual:
        raise RuntimeError(
            "[FREEZE GUARD] El archivo 10_diseno_tecnico.json no contiene 'freeze_id'.\n"
            "El diseño técnico no fue correctamente congelado en la fase Dev."
        )

    if not expected_freeze_id:
        # Sin referencia externa: solo confirmamos que existe
        print(f"[FREEZE GUARD] ✓ freeze_id presente en diseño técnico: {actual}")
        return actual

    if actual != expected_freeze_id:
        raise RuntimeError(
            f"[FREEZE GUARD] ¡freeze_id no coincide!\n"
            f"  En 10_diseno_tecnico.json : {actual}\n"
            f"  Referencia esperada       : {expected_freeze_id}\n"
            f"  El diseño técnico fue modificado después del freeze.\n"
            f"  Ejecución abortada."
        )

    print(f"[FREEZE GUARD] ✓ freeze_id verificado: {actual}")
    return actual