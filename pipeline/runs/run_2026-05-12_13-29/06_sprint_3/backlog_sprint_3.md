---
run_id: run_2026-05-12_13-29
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-12T13:56:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_13-29`

Total de historias: **6**

## Historias del sprint

### HU-13 — Cancelación de reserva en estado PENDIENTE DE PAGO

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para eliminarla del sistema si cambio de opinión.

**Criterios de aceptación**

- El cliente puede cancelar una reserva solo si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- Se muestra un mensaje de confirmación antes de eliminar.
- No se puede cancelar una reserva en otros estados.

### HU-15 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta en el sistema, para seguimiento de mis pedidos.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- El listado muestra el estado de cada reserva.
- El listado muestra los datos del barco, fechas e importe de cada reserva.
- El cliente puede ver el código de seguimiento de cada reserva.
- El cliente puede cancelar una reserva si está en estado PENDIENTE DE PAGO.

### HU-16 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero consultar y cambiar el estado de cualquier reserva desde el panel de administración, para gestionar el ciclo de vida de los pedidos.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas.
- El administrador puede filtrar reservas por estado.
- El administrador puede cambiar el estado de una reserva para transiciones aplicables.
- El sistema valida que la transición de estado sea válida.
- Se registra quién y cuándo cambió el estado de una reserva.

### HU-17 — Gestión administrativa de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero crear, editar y eliminar barcos en el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede crear un nuevo barco con todos los campos requeridos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- Se valida que todos los campos obligatorios estén completos.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-18 — Gestión administrativa de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, para mantener la base de datos de usuarios.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes.
- El administrador puede eliminar un cliente solo si no tiene reservas pendientes.
- Se valida que el cliente no tenga reservas antes de permitir la eliminación.
- Se muestra un mensaje de error si se intenta eliminar un cliente con reservas.
- Los datos del cliente se eliminan del sistema al confirmar.

### HU-21 — Recordatorio de reserva pendiente

- **Prioridad**: Baja
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo de recordatorio un día antes del inicio de mi reserva si aún está en estado PENDIENTE DE PAGO, para no olvidar completar el pago.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con inicio en el próximo día.
- Se envía un correo de recordatorio al cliente.
- El correo incluye los datos de la reserva y el código de seguimiento.
- El recordatorio se envía una sola vez por reserva.
- El sistema maneja correctamente las zonas horarias.
