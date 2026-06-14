---
run_id: run_2026-05-13_15-33
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-13T15:47:23+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-13_15-33`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base de la aplicación con autenticación, catálogo de barcos y ficha de producto. El usuario puede registrarse, iniciar sesión y explorar el catálogo con búsqueda y filtros.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-05`
- `HU-06`
- `HU-22`
- `HU-23`
- `HU-24`
- `HU-25`

**Entregable verificable**: Un visitante puede registrarse, iniciar sesión, cerrar sesión, navegar el catálogo de barcos organizado por categorías, buscar barcos por nombre y aplicar filtros combinables (puertos, fabricantes, precio, categoría, capacidad, fechas). La aplicación está configurada con zona horaria Europe/Madrid, locale español, datos seed precargados y empaquetada en Docker.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva y pago. El cliente puede seleccionar barcos, gestionar la cesta, completar una reserva en tres pasos y recibir confirmación con código de seguimiento.

**Historias asignadas**

- `HU-07`
- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`
- `HU-26`

**Entregable verificable**: Un cliente puede seleccionar cantidad de barcos y añadirlos a la cesta, modificar cantidades, vaciar la cesta, completar una reserva en tres pasos sin registro previo, elegir entre PayPal Sandbox y contra-reembolso, ver el desglose de costos con tasa de combustible, y recibir un correo de confirmación con código de seguimiento.

## Sprint 3

**Objetivo**: Completar la gestión administrativa, seguimiento de reservas y funcionalidades de cierre. El administrador puede gestionar barcos, clientes y reservas; los clientes pueden consultar y cancelar reservas.

**Historias asignadas**

- `HU-04`
- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`
- `HU-20`
- `HU-21`

**Entregable verificable**: Un administrador puede acceder al panel de administración, crear/editar/eliminar barcos, eliminar clientes sin reservas pendientes y cambiar estados de reservas. Un cliente puede cancelar reservas en estado PENDIENTE DE PAGO, consultar el estado de sus reservas por código de seguimiento o desde su cuenta autenticada. El sistema envía correos de recordatorio de pago pendiente 24 horas antes del inicio de la reserva.
