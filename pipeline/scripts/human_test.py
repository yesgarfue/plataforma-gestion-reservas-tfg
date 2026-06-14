# scripts/human_test.py
from pathlib import Path
from pipeline.gates.human_gate import human_gate

# Raíz del proyecto: scripts/ está un nivel por debajo.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RUN_DIR = PROJECT_ROOT / "runs" / "run_2026-05-08_12-03" / "01_requisitos"

result = human_gate(
    fase="01_requisitos",
    fase_dir=RUN_DIR,
    artefacto_md=RUN_DIR / "registro_requisitos.md",
    numero_gate=1,
    regeneraciones_consumidas=2,
)
print(result.model_dump_json(indent=2))