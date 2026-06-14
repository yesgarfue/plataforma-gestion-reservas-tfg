---
run_id: run_2026-05-14_16-53
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-14T17:11:46+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_16-53`

Total de historias: **8**

## Historias del sprint

### HU-12 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para dejar de alquilar el barco.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema sin dejar registro posterior.
- El cliente recibe una confirmación de cancelación.

### HU-13 — Recordatorio de reserva próxima

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de una reserva en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO que comienzan en un día.
- El sistema envía un correo de recordatorio al cliente.
- El correo contiene los datos de la reserva y el código de seguimiento.

### HU-14 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- El cliente puede ingresar el código de seguimiento sin estar registrado.
- El sistema muestra el estado actual de la reserva.
- El sistema muestra los datos del barco, rango de fechas e importe total.

### HU-15 — Consulta de reservas del cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta.

**Criterios de aceptación**

- El cliente registrado puede acceder a un listado de sus reservas.
- El listado muestra el estado de cada reserva.
- El cliente puede ver los detalles de cada reserva.

### HU-16 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero consultar el estado de cualquier reserva y cambiar su estado mediante botones por transición aplicable.

**Criterios de aceptación**

- El administrador puede acceder a un panel de reservas.
- El panel muestra todas las reservas del sistema.
- El administrador puede consultar el estado de cualquier reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Solo se muestran transiciones válidas según el estado actual.

### HU-17 — Gestión de barcos en panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero realizar alta, edición y baja de barcos desde el panel de administración.

**Criterios de aceptación**

- El administrador puede acceder a un panel de gestión de barcos.
- El administrador puede crear un nuevo barco con todos sus datos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del sistema.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-18 — Gestión de clientes en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede acceder a un panel de gestión de clientes.
- El administrador puede visualizar el listado de clientes.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- El administrador puede consultar las reservas de cada cliente.

### HU-19 — Ficha de barco para administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero acceder a una ficha de barco propia con acciones de gestión: alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a una ficha de barco desde el panel de administración.
- La ficha muestra todos los datos del barco.
- El administrador puede editar los datos del barco desde la ficha.
- El administrador puede eliminar el barco desde la ficha.
- El administrador puede crear un nuevo barco desde una ficha vacía.
