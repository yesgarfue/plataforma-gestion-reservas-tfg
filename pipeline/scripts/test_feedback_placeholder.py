# scripts/test_feedback_placeholder.py
"""
Test aislado del placeholder {feedback_humano} en tasks.yaml.

Objetivo: verificar antes de tocar main.py que CrewAI/Jinja interpola
correctamente el placeholder {feedback_humano} tanto cuando se le pasa
string vacío (primera generación, sin feedback) como cuando se le pasa
contenido (regeneración tras gate humano rechazado).

Este test gasta DOS llamadas a Ollama. Se invoca directamente:

    python scripts/test_feedback_placeholder.py

Si Ollama no está corriendo, el test fallará en la primera llamada.

No usa el brief real: usa un mini-brief sintético de Hundidos para
acortar la generación. Lo que verificamos NO es la calidad del registro
(eso es lo que ya cubre verify_pipeline.py + los Runs medidos), sino
que la interpolación del placeholder no rompe el kickoff.
"""

from __future__ import annotations

import sys
import time
import traceback
from pathlib import Path

# Permite invocar el script desde la raíz del proyecto sin instalar el
# paquete: añade `src/` al sys.path para que `import pipeline...` funcione.
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))


# Mini-brief sintético: lo justo para que el Analista pueda producir
# >=15 RF + >=3 RNF respetando la regla de cobertura del prompt.
# No es el brief real (eso vive en brief/brief.md y solo lo usan los Runs
# oficiales). Aquí solo nos interesa que el kickoff no truene.
_MINI_BRIEF = """
Hundidos es una aplicación web para alquiler de barcos.

3.1 Usuarios y sesión: clientes y administradores con login.
3.2 Catálogo y búsqueda: listado de barcos por categoría y puerto.
3.3 Ficha de barco: detalle de cada barco.
3.4 Cesta: el cliente puede añadir barcos a una cesta.
3.5 Proceso de reserva y pago: con confirmación.
3.6 Estados de reserva y cancelación: PENDIENTE DE PAGO, CONFIRMADA.
3.7 Seguimiento: por código de seguimiento.
3.8 Gestión administrativa: el administrador gestiona barcos, puertos,
fabricantes y categorías.

4. Restricciones técnicas: framework Django, base de datos SQLite,
empaquetado en Docker, locale español, seguridad básica de Django,
datos seed precargados.
""".strip()


def _imprimir_separador(titulo: str) -> None:
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def _ejecutar_kickoff(feedback_humano: str, etiqueta: str) -> bool:
    """
    Ejecuta un kickoff de la requisitos_crew con el feedback indicado.
    Devuelve True si la ejecución termina sin excepción y produce un
    objeto con .pydantic. No valida la calidad del registro.
    """
    _imprimir_separador(f"Test: {etiqueta} (feedback_humano={feedback_humano!r})")

    from pipeline.crews.requisitos_crew.requisitos_crew import RequisitosCrew

    crew_obj = RequisitosCrew().crew()

    inputs = {
        "brief": _MINI_BRIEF,
        "run_id": f"run_test_{etiqueta}",
        "feedback_humano": feedback_humano,
    }

    t0 = time.monotonic()
    try:
        result = crew_obj.kickoff(inputs=inputs)
    except KeyError as e:
        # Síntoma típico de placeholder no encontrado en inputs.
        print(f"[FAIL] KeyError en kickoff: {e}")
        print("       Probable causa: tasks.yaml referencia un placeholder")
        print("       que no estamos pasando en inputs.")
        return False
    except Exception as e:
        print(f"[FAIL] {type(e).__name__}: {e}")
        traceback.print_exc()
        return False
    duracion = time.monotonic() - t0

    pyd = getattr(result, "pydantic", None)
    if pyd is None:
        print(f"[WARN] kickoff terminó en {duracion:.1f}s pero result.pydantic es None.")
        print(f"       Raw output (primeros 500 chars): {str(result)[:500]}")
        # Esto NO es un fallo del placeholder: el modelo puede haber
        # devuelto algo no parseable. Lo importante es que no haya
        # KeyError de Jinja.
        print("       (No es fallo del placeholder; el JSON del LLM no parseó.)")
        return True

    n_rf = len(pyd.requisitos_funcionales)
    n_rnf = len(pyd.requisitos_no_funcionales)
    print(f"[OK]   kickoff completado en {duracion:.1f}s. RF={n_rf}, RNF={n_rnf}")
    return True


def main() -> int:
    """
    Dos tests:
      1. feedback_humano="" — primera generación, debe funcionar.
      2. feedback_humano="<bloque de regeneración>" — regeneración.
    """
    print("Test del placeholder {feedback_humano} en tasks.yaml")
    print(f"Project root: {_PROJECT_ROOT}")

    # Test 1: string vacío.
    ok_vacio = _ejecutar_kickoff(
        feedback_humano="",
        etiqueta="placeholder_vacio",
    )

    # Test 2: con contenido (simula una regeneración real).
    feedback_simulado = (
        "------ INSTRUCCIONES DE REGENERACIÓN (operadora humana) ------\n"
        "Esta es la regeneración 1. La generación anterior fue rechazada\n"
        "porque omitía la subsección 3.5 del brief. Asegúrate de incluir\n"
        "al menos un requisito funcional sobre el proceso de reserva y pago.\n"
        "------ FIN INSTRUCCIONES DE REGENERACIÓN ------"
    )
    ok_con_contenido = _ejecutar_kickoff(
        feedback_humano=feedback_simulado,
        etiqueta="placeholder_con_contenido",
    )

    _imprimir_separador("Resumen")
    print(f"  Test 1 (vacío):         {'OK' if ok_vacio else 'FAIL'}")
    print(f"  Test 2 (con contenido): {'OK' if ok_con_contenido else 'FAIL'}")

    if ok_vacio and ok_con_contenido:
        print("\nResultado: placeholder operativo en ambos casos.")
        print("Podemos proceder al archivo 3 (modificar main.py).")
        return 0
    else:
        print("\nResultado: hay un problema con el placeholder.")
        print("NO procedas al archivo 3 hasta diagnosticar.")
        return 1


if __name__ == "__main__":
    sys.exit(main())