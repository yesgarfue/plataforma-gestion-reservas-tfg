---
gate: 3
fase: 03_arquitectura
decision: rechazado
timestamp_revision_inicio: 2026-05-18T17:15:12+02:00
timestamp_revision_fin: 2026-05-18T19:46:12+02:00
---

## Observaciones

El diseño cubre gran parte del stack y las apps principales, pero contiene incoherencias bloqueantes para avanzar a scaffold/desarrollo. La principal es que el panel administrativo propio se define bajo `/admin/` en lugar de `/admin-panel/`, lo que entra en conflicto con el admin nativo de Django y con las rutas mínimas esperadas por la validación final. Además, el modelo de Reserva solo contempla un barco por reserva, aunque la cesta permite múltiples elementos, y la cancelación aparece restringida a usuarios autenticados pese a que el sistema permite reservas sin registro.

## Acción

Regenerar arquitectura indicando explícitamente que el panel propio debe exponerse bajo `/admin-panel/`, mantener `/admin/` para Django admin si se usa, modelar reservas con líneas de reserva, y permitir cancelación compatible con reservas de visitantes.