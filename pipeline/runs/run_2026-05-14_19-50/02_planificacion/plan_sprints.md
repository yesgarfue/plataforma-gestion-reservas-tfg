---
run_id: run_2026-05-14_19-50
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T20:09:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-14_19-50`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer el modelo de datos básico, autenticación de usuarios y catálogo navegable de barcos. El cliente puede registrarse, iniciar sesión y explorar el catálogo con búsqueda y filtros.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-19`
- `HU-20`
- `HU-21`

**Entregable verificable**: Un visitante puede registrarse, iniciar sesión, navegar el catálogo de barcos con búsqueda y filtros combinables, acceder a la ficha de un barco, y cerrar sesión. La aplicación arranca con datos precargados, zona horaria Europe/Madrid, locale español e interfaz completamente en español.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva, cesta y pago. El cliente puede añadir barcos a la cesta, completar una reserva en tres pasos sin registro previo, elegir método de pago y recibir confirmación con código de seguimiento.

**Historias asignadas**

- `HU-06`
- `HU-07`
- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`

**Entregable verificable**: Un cliente puede añadir barcos a la cesta desde la ficha, modificar cantidades, iniciar el proceso de reserva en tres pasos, elegir entre PayPal Sandbox y contra-reembolso, recibir un correo de confirmación con código de seguimiento, y ver el estado inicial PENDIENTE DE PAGO de su reserva. La tasa de combustible se calcula correctamente según la categoría del barco.

## Sprint 3

**Objetivo**: Cerrar funcionalidades de seguimiento, cancelación, gestión administrativa y pulido. El cliente puede consultar reservas, cancelarlas si están pendientes, y el administrador gestiona barcos, clientes y reservas.

**Historias asignadas**

- `HU-12`
- `HU-13`
- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`

**Entregable verificable**: Un cliente puede cancelar reservas en estado PENDIENTE DE PAGO, consultar el estado de sus reservas por código de seguimiento sin autenticación, y ver sus reservas en su cuenta. El administrador accede al panel de administración, gestiona barcos (alta, edición, baja), consulta y elimina clientes respetando restricciones, consulta y cambia estados de reservas. El sistema envía recordatorios de reservas pendientes un día antes del inicio.
