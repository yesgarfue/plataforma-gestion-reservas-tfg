---
run_id: run_2026-05-18_15-09
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-18T16:03:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-18_15-09`

Total de historias: **7**

## Historias del sprint

### HU-13 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está pendiente de pago, para anular mi alquiler.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- El cliente recibe una confirmación de cancelación.

### HU-14 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue pendiente de pago.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario.
- El correo incluye los datos de la reserva y un enlace para completar el pago.
- El correo está redactado en español.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

**Criterios de aceptación**

- El cliente puede consultar el estado de su reserva usando el código de seguimiento.
- No es necesario estar registrado para consultar por código de seguimiento.
- Se muestra el estado actual de la reserva, datos del barco y rango de fechas.
- Si el código no existe, se muestra un mensaje de error.

### HU-16 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta.

**Criterios de aceptación**

- El usuario registrado puede consultar el estado de sus reservas desde su cuenta.
- Se muestra una lista de todas las reservas del cliente con sus estados.
- Se puede acceder a los detalles de cada reserva.
- Se muestra el código de seguimiento de cada reserva.

### HU-17 — Gestión administrativa de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los barcos del catálogo mediante alta, edición y baja.

**Criterios de aceptación**

- El administrador dispone de una ficha de barco propia con acciones de gestión.
- El administrador puede crear un nuevo barco (alta).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco (baja).
- Al eliminar un barco, se valida que no tenga reservas activas.

### HU-18 — Gestión administrativa de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes con la restricción de que no tengan reservas pendientes.

**Criterios de aceptación**

- El panel de administración permite la consulta de clientes.
- El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- Se muestra una lista de clientes con sus datos principales.

### HU-19 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de las reservas desde el panel de administración.

**Criterios de aceptación**

- El panel de administración permite la consulta de todas las reservas.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Se muestra el estado actual y las transiciones disponibles para cada reserva.
- El administrador puede consultar los detalles completos de cualquier reserva.
