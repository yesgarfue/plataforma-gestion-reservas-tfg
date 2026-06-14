---
run_id: run_2026-05-14_02-35
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-14T02:48:23+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_02-35`

Total de historias: **8**

## Historias del sprint

### HU-12 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente no registrado, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, para conocer el estado de mi alquiler.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- Ingresando el código de seguimiento, se muestra el estado actual de la reserva.
- Se muestran los datos del barco, rango de fechas e importe total.
- No se requiere estar registrado para consultar la reserva.

### HU-13 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El usuario registrado puede acceder a un listado de sus reservas.
- Se muestra el estado de cada reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO).
- Se muestran los datos del barco, rango de fechas e importe total de cada reserva.
- El cliente puede acceder a esta funcionalidad desde su cuenta.

### HU-14 — Cancelación de reserva en estado PENDIENTE DE PAGO

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar mi reserva si está en estado PENDIENTE DE PAGO, para anular mi alquiler sin dejar registro.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema sin quedar registrada con un estado posterior.
- El cliente recibe una confirmación de la cancelación.
- Las reservas en otros estados no pueden ser canceladas por el cliente.

### HU-15 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de una reserva en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario.
- El correo contiene los datos de la reserva y un enlace para completar el pago.
- El recordatorio se envía automáticamente sin intervención manual.

### HU-16 — Gestión de barcos en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar barcos desde el panel de administración, realizando operaciones de alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a un panel de administración propio de la aplicación.
- El administrador puede crear nuevos barcos con todos los campos requeridos (nombre, imagen, categoría, fabricante, puerto, capacidad, precio por día).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del sistema.
- Al eliminar un barco, se valida que no tenga reservas activas.

### HU-17 — Gestión de clientes en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando restricciones de seguridad.

**Criterios de aceptación**

- El administrador puede acceder a un listado de clientes.
- El administrador puede visualizar los datos de cada cliente.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Al intentar eliminar un cliente con reservas pendientes, se muestra un mensaje de error explicativo.
- Se mantiene un registro de auditoría de eliminaciones.

### HU-18 — Gestión de reservas en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- El administrador puede visualizar los datos completos de cada reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Las transiciones de estado válidas son: PENDIENTE DE PAGO → PAGADO, PAGADO → EN USO, EN USO → DEVUELTO.
- Se muestra un historial de cambios de estado para cada reserva.

### HU-19 — Ficha de barco para administrador

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador, quiero acceder a una ficha de barco propia con acciones de gestión de alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a una ficha de barco desde el panel de administración.
- La ficha muestra todos los datos del barco.
- El administrador puede crear un nuevo barco desde la ficha.
- El administrador puede editar los datos del barco.
- El administrador puede eliminar el barco.
