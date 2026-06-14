---
run_id: run_2026-05-12_13-29
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T13:52:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-12_13-29`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base de la aplicación con autenticación, catálogo de barcos y ficha de producto. El usuario puede registrarse, iniciar sesión, navegar el catálogo y ver detalles de barcos.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-07`
- `HU-22`
- `HU-23`
- `HU-24`
- `HU-25`

**Entregable verificable**: Un visitante puede registrarse, iniciar sesión, cerrar sesión, navegar el catálogo de barcos organizado por categorías, buscar y filtrar barcos, ver la ficha de un barco con todos sus datos, seleccionar cantidad y añadir a la cesta. La cesta es visible en todas las páginas. La aplicación está empaquetada en Docker, configurada con zona horaria Europe/Madrid y locale español, con datos seed precargados.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva y pago. El usuario puede modificar la cesta, completar una reserva en tres pasos, elegir método de pago, recibir confirmación con código de seguimiento y consultar el estado de su reserva.

**Historias asignadas**

- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-14`
- `HU-19`
- `HU-20`

**Entregable verificable**: Un cliente puede modificar la cesta (aumentar, reducir, eliminar barcos), completar una reserva en tres pasos sin registro previo, elegir entre PayPal Sandbox y contra-reembolso, recibir un correo de confirmación con código de seguimiento, y consultar el estado de su reserva usando el código sin estar registrado. La tasa de combustible se aplica correctamente (50 € por día, excepto para veleros).

## Sprint 3

**Objetivo**: Cerrar funcionalidades de seguimiento, gestión administrativa y pulido. El usuario registrado puede consultar sus reservas y cancelarlas si están pendientes. El administrador gestiona barcos, clientes y reservas. Se implementan recordatorios y validaciones finales.

**Historias asignadas**

- `HU-13`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-21`

**Entregable verificable**: Un cliente registrado puede consultar el listado de sus reservas y cancelar las que están en estado PENDIENTE DE PAGO. Un administrador puede gestionar barcos (crear, editar, eliminar), gestionar clientes (consultar, eliminar si no tienen reservas pendientes), y gestionar reservas (consultar todas, filtrar por estado, cambiar estado con validación). El sistema envía recordatorios un día antes de reservas pendientes. La aplicación está lista para producción con todas las medidas de seguridad implementadas.
