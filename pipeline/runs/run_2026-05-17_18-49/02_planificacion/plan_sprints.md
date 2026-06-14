---
run_id: run_2026-05-17_18-49
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-17T19:09:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-17_18-49`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base técnica de la aplicación con autenticación, catálogo navegable y ficha de barco. El cliente puede registrarse, iniciar sesión, explorar barcos y ver detalles de cada uno.

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

**Entregable verificable**: Un visitante puede registrarse, iniciar sesión, cerrar sesión, navegar el catálogo de barcos con búsqueda y filtros combinables, acceder a la ficha de un barco y ver todos sus datos. La aplicación está configurada con zona horaria Europe/Madrid, locale español e interfaz completamente en español. Los datos de ejemplo están precargados.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva y pago. El cliente puede añadir barcos a la cesta, completar una reserva en tres pasos sin registro previo, seleccionar método de pago y recibir confirmación con código de seguimiento.

**Historias asignadas**

- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`

**Entregable verificable**: Un cliente puede añadir barcos a la cesta desde la ficha, modificar cantidades, iniciar el proceso de reserva sin estar registrado, completarlo en tres pasos, seleccionar PayPal Sandbox o contra-reembolso, y recibir un correo de confirmación con código de seguimiento único. El importe total se calcula correctamente incluyendo la tasa de combustible (50 euros/día, 0 para veleros).

## Sprint 3

**Objetivo**: Completar la gestión administrativa, seguimiento de reservas y funcionalidades de cierre. El administrador puede gestionar barcos, clientes y reservas. Los clientes pueden consultar el estado de sus reservas por código o desde su cuenta.

**Historias asignadas**

- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`
- `HU-20`

**Entregable verificable**: Un cliente puede consultar el estado de su reserva usando el código de seguimiento sin estar registrado, o desde su cuenta si está autenticado. Un administrador puede acceder al panel de administración, crear/editar/eliminar barcos, consultar y eliminar clientes (respetando restricción de reservas pendientes), consultar y cambiar estados de reservas. El sistema envía recordatorios de pago pendiente cuando falta un día para el inicio de la reserva.
