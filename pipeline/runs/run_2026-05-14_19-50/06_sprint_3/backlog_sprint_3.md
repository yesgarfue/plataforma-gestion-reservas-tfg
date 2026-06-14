---
run_id: run_2026-05-14_19-50
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-14T20:10:28+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_19-50`

Total de historias: **7**

## Historias del sprint

### HU-12 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para eliminarla del sistema sin dejar registro posterior.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema sin dejar registro posterior.
- El cliente recibe una confirmación de cancelación.
- Las reservas en otros estados no pueden cancelarse.

### HU-13 — Recordatorio de reserva pendiente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con fecha de inicio en el próximo día.
- El sistema envía un correo de recordatorio al cliente.
- El correo contiene los datos de la reserva y un enlace para completar el pago.

### HU-14 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- El sistema busca la reserva por código de seguimiento.
- Se muestra el estado actual de la reserva.
- No se requiere autenticación para consultar por código de seguimiento.

### HU-15 — Consulta de reservas del cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- Se muestra el estado actual de cada reserva.
- Se muestran los datos del barco, rango de fechas e importe de cada reserva.
- El cliente puede acceder a los detalles de cada reserva.

### HU-16 — Panel de administración de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar barcos desde el panel de administración: dar de alta, editar y dar de baja.

**Criterios de aceptación**

- El administrador accede a un panel de administración propio.
- El administrador puede dar de alta nuevos barcos con todos los campos requeridos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede dar de baja un barco.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-17 — Panel de administración de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede consultar un listado de todos los clientes.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si un cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede eliminarse.
- Se muestra información de contacto y reservas de cada cliente.

### HU-18 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración mediante botones por transición aplicable.

**Criterios de aceptación**

- El administrador puede consultar un listado de todas las reservas.
- El administrador puede ver el estado actual de cada reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Se muestran los datos del barco, cliente, rango de fechas e importe de cada reserva.
- Los cambios de estado se registran en el sistema.
