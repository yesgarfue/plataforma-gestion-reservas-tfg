---
run_id: run_2026-05-12_15-34
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-12T15:59:09+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_15-34`

Total de historias: **6**

## Historias del sprint

### HU-14 — Cancelación de reserva en estado PENDIENTE DE PAGO

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar mi reserva si está en estado PENDIENTE DE PAGO, para desistir de mi compra si cambio de opinión.

**Criterios de aceptación**

- El cliente puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO.
- Tras cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado de reservas del cliente.
- Se muestra un mensaje de confirmación tras la cancelación.

### HU-15 — Recordatorio por email antes del inicio de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un recordatorio por email al cliente si falta un día para el inicio de su reserva, para que no olvide su alquiler.

**Criterios de aceptación**

- Se envía un email automático si falta exactamente un día para el inicio de la reserva.
- El email contiene los datos de la reserva y el código de seguimiento.
- El email se envía solo si la reserva está en estado CONFIRMADA o posterior.

### HU-16 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente no registrado, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, para saber el estado de mi alquiler sin necesidad de registrarme.

**Criterios de aceptación**

- El cliente puede introducir un código de seguimiento en un formulario de búsqueda.
- Se muestra el estado actual de la reserva (PENDIENTE DE PAGO, CONFIRMADA, CANCELADA, etc.).
- Se muestran los datos de la reserva (barco, fechas, importe).
- Si el código no existe, se muestra un mensaje de error.

### HU-17 — Historial de reservas del cliente registrado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el historial de todas mis reservas desde mi cuenta, para revisar mis alquileres anteriores y actuales.

**Criterios de aceptación**

- El cliente autenticado puede acceder a su historial de reservas.
- Se muestran todas las reservas del cliente (pasadas, actuales y canceladas).
- Cada reserva muestra el barco, fechas, importe y estado.
- El cliente puede ver el código de seguimiento de cada reserva.

### HU-18 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero gestionar las reservas, ver su estado y cambiar el estado de una reserva que esté en PENDIENTE DE PAGO, para administrar los alquileres.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas del sistema.
- El administrador puede ver los detalles de cada reserva (cliente, barco, fechas, estado, importe).
- El administrador puede cambiar el estado de una reserva únicamente si está en PENDIENTE DE PAGO.
- El administrador puede cambiar el estado a CONFIRMADA o CANCELADA.
- Se muestra un mensaje de confirmación tras cambiar el estado.

### HU-19 — Eliminación de cliente por administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero eliminar un cliente únicamente si no tiene reservas pendientes, para mantener la integridad de los datos.

**Criterios de aceptación**

- El administrador puede ver un listado de clientes.
- El administrador puede eliminar un cliente solo si no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- Tras eliminar un cliente, se muestra un mensaje de confirmación.
