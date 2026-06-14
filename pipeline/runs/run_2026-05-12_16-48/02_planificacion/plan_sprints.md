---
run_id: run_2026-05-12_16-48
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T17:01:38+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-12_16-48`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer el modelo de datos básico, autenticación de usuarios y catálogo navegable de barcos. El cliente puede registrarse, iniciar sesión, explorar el catálogo y ver fichas de barcos.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-05`
- `HU-06`
- `HU-07`
- `HU-21`
- `HU-22`
- `HU-23`
- `HU-24`

**Entregable verificable**: Un cliente puede registrarse con correo y contraseña, iniciar sesión, navegar el catálogo de barcos filtrado por categoría, puerto, fabricante y precio, ver la ficha detallada de un barco con imagen y datos completos, y cerrar sesión. La aplicación está en español, con zona horaria Europe/Madrid, y arranca con datos seed precargados en Docker.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva, cesta y pago. El cliente puede añadir barcos a la cesta, completar una reserva en tres pasos sin registro previo, elegir método de pago y recibir confirmación con código de seguimiento.

**Historias asignadas**

- `HU-04`
- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`

**Entregable verificable**: Un cliente puede seleccionar cantidad de barcos y añadirlos a la cesta, ver la cesta siempre visible, modificar cantidades, completar una reserva en tres pasos sin estar registrado, elegir entre PayPal Sandbox y contra-reembolso, recibir un correo con código de seguimiento, y el precio se calcula correctamente con tasa de combustible según la categoría del barco.

## Sprint 3

**Objetivo**: Cerrar el ciclo de seguimiento, gestión administrativa completa y pulido. El cliente puede consultar reservas por código o desde su cuenta, el administrador gestiona barcos, clientes y reservas, y se implementan recordatorios de pago.

**Historias asignadas**

- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`
- `HU-20`

**Entregable verificable**: Un cliente puede consultar el estado de su reserva usando el código de seguimiento sin estar registrado, o desde su cuenta si está autenticado. Un administrador accede a un panel propio para gestionar barcos (alta, edición, baja), clientes (consulta, eliminación con validación), y reservas (consulta, cambio de estado). Se envían recordatorios de pago automáticos cuando falta un día para el inicio de una reserva en estado PENDIENTE DE PAGO.
