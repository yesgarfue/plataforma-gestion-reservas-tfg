---
run_id: run_2026-05-13_06-57
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-13T07:11:55+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-13_06-57`

Total de historias: **7**

## Historias del sprint

### HU-15 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar mi reserva si está en estado PENDIENTE DE PAGO, para desistir del alquiler si es necesario.

**Criterios de aceptación**

- El cliente puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO.
- Tras cancelar, la reserva se elimina del sistema.
- Se envía un correo de confirmación de cancelación al cliente.
- Las reservas en otros estados no pueden ser canceladas.

### HU-16 — Recordatorio de reserva por correo

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente un día antes de la fecha de inicio de la reserva, para que no olvide su alquiler.

**Criterios de aceptación**

- Se envía un correo de recordatorio un día antes de la fecha de inicio.
- El recordatorio se envía solo si la reserva está en estado PENDIENTE DE PAGO.
- El correo incluye los detalles de la reserva y el código de seguimiento.
- El sistema registra el envío del recordatorio.

### HU-17 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por correo, para verificar el estado de mi alquiler sin necesidad de registrarme.

**Criterios de aceptación**

- Existe una página de consulta de reserva por código de seguimiento.
- El cliente introduce el código de seguimiento.
- Se muestra el estado actual de la reserva.
- Se muestran los detalles de la reserva (barco, fechas, total).

### HU-18 — Consulta de reservas del cliente registrado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta personal, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- Se muestran todas las reservas del cliente con sus estados.
- Se muestran los detalles de cada reserva (barco, fechas, estado, total).
- El cliente puede filtrar por estado si lo desea.

### HU-19 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de cualquier reserva en la aplicación, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- Se muestran los detalles de cada reserva (cliente, barco, fechas, estado, total).
- El administrador puede cambiar el estado de una reserva.
- El administrador puede filtrar las reservas por estado, cliente o barco.

### HU-20 — Gestión administrativa de barcos

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar el catálogo de barcos (crear, editar, eliminar), para mantener la información actualizada.

**Criterios de aceptación**

- El administrador puede crear nuevos barcos con todos los atributos (nombre, descripción, precio, categoría, capacidad, puerto, fabricante).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- El sistema valida que los datos sean correctos antes de guardar.

### HU-21 — Gestión administrativa de clientes

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los clientes registrados, incluyendo la eliminación de usuarios sin reservas pendientes.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes registrados.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Se muestra un mensaje de error si se intenta eliminar un cliente con reservas pendientes.
- El administrador puede ver los detalles de cada cliente.
