---
run_id: run_2026-05-11_13-11
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-11T13:24:03+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-11_13-11`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base técnica de la aplicación con autenticación, catálogo de barcos y ficha detallada. El cliente puede registrarse, iniciar sesión, explorar barcos y ver detalles sin realizar reservas.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-07`
- `HU-26`
- `HU-27`

**Entregable verificable**: La aplicación arranca con datos precargados, el cliente puede registrarse e iniciar sesión, navegar el catálogo con filtros combinables, ver fichas detalladas de barcos, y la zona horaria y locale están configurados correctamente.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva, cesta y pago. El cliente puede añadir barcos a la cesta, modificarla, completar una reserva en tres pasos y elegir entre dos métodos de pago.

**Historias asignadas**

- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`
- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`

**Entregable verificable**: El cliente puede añadir barcos a la cesta, modificar cantidades, completar una reserva sin registro previo en tres pasos, elegir entre PayPal Sandbox y contra-reembolso, recibir correo de confirmación con código de seguimiento, y la tasa de combustible se calcula correctamente.

## Sprint 3

**Objetivo**: Cerrar el ciclo de vida de reservas, implementar seguimiento y gestión administrativa completa. El cliente puede cancelar reservas, consultar estados, y el administrador gestiona barcos, clientes y reservas.

**Historias asignadas**

- `HU-18`
- `HU-19`
- `HU-20`
- `HU-21`
- `HU-22`
- `HU-23`
- `HU-24`
- `HU-25`

**Entregable verificable**: El cliente puede cancelar reservas en estado PENDIENTE DE PAGO, consultar reservas por código de seguimiento o desde su cuenta, el administrador puede gestionar barcos (alta, edición, baja), clientes (consulta, eliminación con restricciones) y reservas (consulta, cambio de estado), y se envían recordatorios de pago pendiente.
