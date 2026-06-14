---
run_id: run_2026-05-12_15-34
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T15:55:36+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-12_15-34`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base técnica de la aplicación con autenticación, catálogo de barcos y ficha detallada. El cliente puede registrarse, iniciar sesión, explorar barcos y ver detalles de cada uno.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-07`
- `HU-21`
- `HU-22`

**Entregable verificable**: La aplicación está empaquetada en Docker, arranca correctamente con datos seed, permite registro e inicio de sesión de clientes, muestra el catálogo de barcos organizado por categorías, permite búsqueda y filtrado combinable, y muestra la ficha detallada de cada barco con opción de seleccionar cantidad.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva, cesta y pago. El cliente puede añadir barcos a la cesta, realizar una reserva en tres pasos, elegir método de pago y recibir confirmación por email con código de seguimiento.

**Historias asignadas**

- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`
- `HU-20`

**Entregable verificable**: El cliente puede añadir barcos a la cesta visible desde cualquier página, modificar cantidades, realizar una reserva en tres pasos sin registro previo, elegir entre PayPal Sandbox y contra-reembolso, recibir correo de confirmación con código de seguimiento, y la tasa de combustible se calcula correctamente con excepción para veleros.

## Sprint 3

**Objetivo**: Cerrar funcionalidades de seguimiento, cancelación, gestión administrativa y pulido. El cliente puede consultar reservas, cancelarlas si están pendientes, y el administrador puede gestionar reservas y clientes.

**Historias asignadas**

- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`

**Entregable verificable**: El cliente puede cancelar reservas en estado PENDIENTE DE PAGO, consultar el estado de su reserva por código de seguimiento sin registrarse, ver su historial de reservas si está autenticado, recibir recordatorios por email un día antes del inicio de la reserva, y el administrador puede gestionar todas las reservas, cambiar estados y eliminar clientes sin reservas pendientes.
