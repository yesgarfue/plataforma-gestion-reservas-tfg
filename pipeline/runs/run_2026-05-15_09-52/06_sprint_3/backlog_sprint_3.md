---
run_id: run_2026-05-15_09-52
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-15T10:00:43+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-15_09-52`

Total de historias: **7**

## Historias del sprint

### HU-13 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para eliminarla del sistema si cambio de opinión.

**Criterios de aceptación**

- El cliente puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- No se puede cancelar una reserva en otros estados.

### HU-14 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para evitar que se pierda la reserva.

**Criterios de aceptación**

- El sistema identifica reservas que vencen en un día y están en estado PENDIENTE DE PAGO.
- Se envía un correo de recordatorio al cliente con los datos de la reserva.
- El correo incluye instrucciones para completar el pago.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado, para hacer seguimiento de mi alquiler.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- Introduciendo el código, el sistema muestra el estado actual de la reserva.
- No se requiere estar registrado para consultar por código de seguimiento.
- Se muestra el estado, datos del barco, rango de fechas e importe total.

### HU-16 — Consulta de reservas del cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta, para hacer seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente registrado puede acceder a un listado de sus reservas.
- El listado muestra el estado, datos del barco, rango de fechas e importe de cada reserva.
- El cliente puede filtrar o buscar sus reservas.

### HU-17 — Panel de administración de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero gestionar barcos desde un panel de administración propio, realizando alta, edición y baja de barcos, para mantener el catálogo actualizado.

**Criterios de aceptación**

- Existe un panel de administración propio de la aplicación.
- El administrador puede crear un nuevo barco con todos sus datos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- El panel muestra un listado de todos los barcos con opciones de acción.

### HU-18 — Panel de administración de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes, para gestionar la base de clientes.

**Criterios de aceptación**

- El administrador puede consultar un listado de todos los clientes.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si un cliente tiene reservas pendientes, el botón de eliminar está deshabilitado o muestra un mensaje de error.
- El panel muestra información relevante de cada cliente.

### HU-19 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración, para gestionar el ciclo de vida de las reservas.

**Criterios de aceptación**

- El administrador puede consultar un listado de todas las reservas.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- El panel muestra el estado actual, datos del barco, cliente, rango de fechas e importe de cada reserva.
- Solo se muestran transiciones válidas según el estado actual.
