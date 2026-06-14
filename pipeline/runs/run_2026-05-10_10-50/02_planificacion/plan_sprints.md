---
run_id: run_2026-05-10_10-50
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-10T10:59:24+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-10_10-50`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base técnica y el catálogo navegable. El cliente puede registrarse, iniciar sesión, explorar barcos por categorías, buscar y filtrar, ver fichas detalladas y añadir barcos a la cesta.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-07`
- `HU-08`
- `HU-24`
- `HU-25`
- `HU-26`

**Entregable verificable**: Aplicación Django con autenticación funcional, catálogo de barcos con búsqueda y filtros combinables, ficha de barco con selección de cantidad, cesta visible y persistente, datos seed precargados, zona horaria y locale configurados, y seguridad implementada.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva y pago. El cliente puede reservar sin registro previo, iniciar sesión durante la reserva, completar el proceso en tres pasos, pagar mediante PayPal o contra-reembolso, y recibir confirmación con código de seguimiento.

**Historias asignadas**

- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`
- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`

**Entregable verificable**: Proceso de reserva en tres pasos sin registro previo, cálculo correcto de tasa de combustible, integración con PayPal Sandbox y contra-reembolso, envío de correos de confirmación con código de seguimiento, y gestión de estados de reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO).

## Sprint 3

**Objetivo**: Completar la gestión administrativa y el seguimiento de pedidos. El administrador puede gestionar barcos, clientes y reservas; el cliente puede consultar el estado de sus reservas por código de seguimiento o desde su cuenta.

**Historias asignadas**

- `HU-18`
- `HU-19`
- `HU-20`
- `HU-21`
- `HU-22`
- `HU-23`

**Entregable verificable**: Panel administrativo completo con gestión de barcos, clientes y reservas; página pública de seguimiento de pedidos por código de seguimiento; sección 'Mis reservas' para clientes autenticados; cancelación de reservas por administrador; y filtrado avanzado de reservas.
