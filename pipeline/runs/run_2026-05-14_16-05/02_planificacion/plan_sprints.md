---
run_id: run_2026-05-14_16-05
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T16:10:05+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-14_16-05`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer el modelo de datos básico, autenticación de usuarios y catálogo navegable con filtros. El cliente puede registrarse, iniciar sesión, navegar el catálogo de barcos y ver la ficha de un barco específico.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`

**Entregable verificable**: El cliente puede registrarse con correo y contraseña, iniciar sesión, cerrar sesión, navegar un catálogo de barcos con filtros combinables (puerto, fabricante, precio, categoría, capacidad, fechas), buscar barcos por nombre y acceder a la ficha de un barco con sus datos e imagen.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva, cesta y pago con ambos métodos de pago. El cliente puede añadir barcos a la cesta, completar una reserva en tres pasos sin registro previo, pagar mediante PayPal o contra-reembolso, y recibir confirmación con código de seguimiento.

**Historias asignadas**

- `HU-07`
- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`

**Entregable verificable**: El cliente puede gestionar la cesta (añadir, modificar cantidad, vaciar), completar una reserva en tres pasos sin registro previo, seleccionar método de pago (PayPal Sandbox o contra-reembolso), recibir correo de confirmación con código de seguimiento, y el sistema calcula correctamente el precio con tasa de combustible (50 euros/día excepto veleros).

## Sprint 3

**Objetivo**: Cerrar el ciclo de seguimiento de reservas, cancelaciones, gestión administrativa completa y pulido final. El cliente puede consultar reservas por código de seguimiento o desde su cuenta, cancelar reservas pendientes, y el administrador gestiona barcos, clientes y reservas desde el panel de administración.

**Historias asignadas**

- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`
- `HU-20`
- `HU-21`

**Entregable verificable**: El cliente puede consultar el estado de una reserva por código de seguimiento sin estar registrado, ver sus reservas en su cuenta, cancelar reservas en estado PENDIENTE DE PAGO, y el administrador puede gestionar barcos (alta, edición, baja), clientes (consultar, eliminar respetando restricciones), reservas (consultar, cambiar estado) desde el panel de administración. El sistema envía recordatorios de pago pendiente 24 horas antes del inicio de la reserva.
