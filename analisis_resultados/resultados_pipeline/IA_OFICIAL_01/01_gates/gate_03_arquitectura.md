---
gate: 3
fase: 03_arquitectura
decision: aceptado
timestamp_revision_inicio: 2026-05-18T15:47:30+02:00
timestamp_revision_fin: 2026-05-18T16:03:30+02:00
---

## Observaciones

El diseño técnico cubre el stack, las apps Django, modelos y rutas necesarias para generar el producto. La arquitectura propuesta es coherente con los requisitos y la planificación aceptados, y permite avanzar a scaffold/desarrollo.

Observaciones no bloqueantes:
- `core/settings.py` y `core/urls.py` pueden confundirse con el paquete de proyecto Django; debe interpretarse como configuración central, no necesariamente como app instalada.
- La definición `ImageField(upload_to=barcos/)` debe implementarse con cadena válida, por ejemplo `upload_to='barcos/'`.
- La disponibilidad por fechas no debe depender solo de `Barco.disponible`; debe calcularse a partir de reservas, fechas y líneas de reserva.
- Logout aparece como ruta GET; sería preferible POST por seguridad.
- Docker/README/requirements no aparecen en archivos principales aunque forman parte del stack esperado.

Se acepta porque no hay contradicciones bloqueantes y el artefacto es suficientemente operativo para la generación de código.

## Acción

Ninguno.
