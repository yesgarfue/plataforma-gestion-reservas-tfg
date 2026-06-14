---
gate: 1
fase: 01_requisitos
decision: rechazado
timestamp_revision_inicio: 2026-05-14T00:02:04+02:00
timestamp_revision_fin:
---

## Observaciones
La regeneración mejora la cobertura, pero el artefacto sigue sin ser aceptable.
Problemas bloqueantes:
- RF-23 atribuye al cliente el cambio de estado de la reserva, pero el brief solo permite al cliente consultar; el cambio de estado corresponde al administrador.
- No aparece un requisito funcional explícito que declare los cuatro estados de reserva: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO.
- La cancelación no recoge que cancelar una reserva pendiente implica eliminarla del sistema y que no existe estado CANCELADO.
- Varios requisitos no funcionales aparecen clasificados como funcionales: idioma, código, zona horaria, seguridad, CSRF, validación de formularios y datos seed.
- El registro no cubre completamente ficha de barco, filtros combinables con rango de fechas, ni desplegables de puerto y fabricante.

## Acción
Ninguna, run abortado por falta de intentos.
