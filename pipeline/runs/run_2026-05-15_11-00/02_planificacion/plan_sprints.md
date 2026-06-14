---
run_id: run_2026-05-15_11-00
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-15T11:04:48+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-15_11-00`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer el modelo de datos básico, autenticación de usuarios y catálogo navegable con ficha de barco. Demostrar el PMV con capacidad de exploración de barcos.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-07`
- `HU-08`

**Entregable verificable**: El cliente puede registrarse, iniciar sesión, cerrar sesión, navegar el catálogo con búsqueda y filtros combinables, acceder a la ficha de un barco, seleccionar cantidad y añadir a la cesta. La cesta es visible desde cualquier página.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva, métodos de pago y confirmación con código de seguimiento. Incluir cálculo de tasa de combustible y gestión de estados de reserva.

**Historias asignadas**

- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`
- `HU-22`

**Entregable verificable**: El cliente puede completar una reserva en tres pasos sin registro previo, seleccionar método de pago (PayPal Sandbox o contra-reembolso), recibir confirmación por correo con código de seguimiento, y consultar el estado de su reserva por código. La tasa de combustible se calcula correctamente.

## Sprint 3

**Objetivo**: Cerrar funcionalidades de seguimiento, cancelación, gestión administrativa completa y pulido. Proporcionar herramientas de administración para barcos, clientes y reservas.

**Historias asignadas**

- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`
- `HU-20`
- `HU-21`
- `HU-23`

**Entregable verificable**: El cliente puede cancelar reservas pendientes, consultar reservas por código de seguimiento, ver sus reservas en su cuenta. El administrador puede gestionar barcos (alta, edición, baja), clientes (consulta, eliminación con restricciones), reservas (cambio de estado), acceder al panel de administración y ver fichas de barco con historial de reservas.
