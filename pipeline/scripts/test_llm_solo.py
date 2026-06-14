# scripts/test_llm_solo.py
"""
Test aislado: ¿la clase LLM puede generar respuestas largas
fuera del Flow?
"""

import time
from pipeline.utils.llm_factory import get_llm

print("Construyendo LLM...")
llm = get_llm("default")
print(f"LLM: {type(llm).__name__}")
print(f"  model={llm.model}")
print(f"  base_url={getattr(llm, 'base_url', '<sin atributo>')}")

print("\nLlamando al LLM con un prompt LARGO (10-25 minutos esperados)...")
t0 = time.monotonic()
respuesta = llm.call(
    "Genera un objeto JSON con la estructura siguiente: una clave "
    "'requisitos_funcionales' con un array de 22 objetos, cada uno con "
    "campos id (RF-01 a RF-22), descripcion (mínimo 25 palabras describiendo "
    "una funcionalidad de un sistema Django de alquiler de barcos online "
    "con catálogo, búsqueda, cesta, reservas y pagos) y prioridad (Alta, "
    "Media o Baja). Y otra clave 'requisitos_no_funcionales' con un array "
    "de 6 objetos similares pero con campo categoria. Devuelve SOLO el JSON, "
    "sin markdown, sin prefacio."
)
elapsed = time.monotonic() - t0
print(f"\nTardó {elapsed:.1f}s ({elapsed/60:.1f} minutos)")
print(f"Respuesta ({len(respuesta)} caracteres):")
print(respuesta[:800])
print("..." if len(respuesta) > 800 else "")