---
run_id: run_2026-05-18_16-37
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-18T19:56:50+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-18_16-37`

Total de historias: **7**

## Historias del sprint

### HU-14 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para deshacer mi alquiler si cambio de opinión.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- El cliente recibe una confirmación de la cancelación.

### HU-15 — Recordatorio de pago pendiente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para evitar que se pierda la reserva.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio.
- El correo contiene los datos de la reserva y un enlace para completar el pago.
- El recordatorio se envía automáticamente sin intervención manual.

### HU-16 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado, para hacer seguimiento de mi alquiler.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reservas por código de seguimiento.
- Introduciendo el código de seguimiento, el sistema muestra el estado actual de la reserva.
- La consulta es accesible sin necesidad de autenticación.
- Si el código no existe, se muestra un mensaje de error.

### HU-17 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para ver el historial y estado actual de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- El listado muestra el estado de cada reserva.
- El cliente puede ver los detalles de cada reserva.
- El listado solo muestra las reservas del cliente autenticado.

### HU-18 — Gestión administrativa de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los barcos del catálogo (alta, edición y baja), para mantener actualizado el inventario de embarcaciones.

**Criterios de aceptación**

- El administrador puede acceder a una ficha de barco propia con acciones de gestión.
- El administrador puede crear un nuevo barco (alta).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco (baja).
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-19 — Gestión administrativa de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes, con la restricción de no poder eliminar clientes que tengan reservas pendientes, para mantener la integridad de los datos.

**Criterios de aceptación**

- El administrador puede consultar el listado de clientes.
- El administrador puede ver los detalles de cada cliente.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, el botón de eliminar está deshabilitado y se muestra un mensaje explicativo.
- Al eliminar un cliente, se elimina su cuenta del sistema.

### HU-20 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar el estado de cualquier reserva y cambiar su estado mediante botones por transición aplicable, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede consultar el listado de todas las reservas.
- El administrador puede ver los detalles de cada reserva.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas.
- Los botones de transición solo muestran las transiciones aplicables según el estado actual.
- El cambio de estado se registra y es visible en el historial de la reserva.
