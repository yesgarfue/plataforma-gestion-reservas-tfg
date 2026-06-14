---
gate: 3
fase: 03_arquitectura
decision: aceptado
timestamp_revision_inicio: 2026-05-18T17:15:12+02:00
timestamp_revision_fin: 2026-05-18T19:56:12+02:00
---

## Observaciones

El diseño regenerado corrige los bloqueos detectados: define el panel propio bajo `/admin-panel/`, evita conflicto con `/admin/`, modela reservas con `LineaReserva`, y permite cancelación pública compatible con reservas sin registro. La arquitectura cubre stack, apps, modelos y rutas necesarias para avanzar a scaffold/desarrollo.

Observaciones no bloqueantes:
- `ImageField(upload_to=barcos/)` debe implementarse como cadena válida.
- El modelo `User` propio requiere una implementación correcta con `AUTH_USER_MODEL` o debe sustituirse por el usuario estándar de Django.
- `core/settings.py` y `core/urls.py` pueden confundirse con el paquete de proyecto.
- La disponibilidad por fechas debe calcularse a partir de reservas y líneas, no solo con `Barco.disponible`.

## Acción

Ninguno.