---
run_id: run_2026-05-14_11-32
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-14T11:57:01+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_11-32`

Total de historias: **5**

## Historias del sprint

### HU-11 — Estados de reserva y cancelación

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero poder cancelar mi reserva si está en estado PENDIENTE DE PAGO, y consultar el estado de mis reservas en cualquier momento.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar una reserva en estado PENDIENTE DE PAGO, la reserva se elimina del sistema sin dejar registro posterior.
- El usuario registrado puede consultar el estado de sus reservas desde su cuenta.
- El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

### HU-12 — Recordatorio de reserva pendiente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario.
- El correo incluye los datos de la reserva y un enlace para consultar el estado.

### HU-13 — Panel de administración de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar barcos desde el panel de administración, realizando alta, edición y baja de barcos.

**Criterios de aceptación**

- El administrador dispone de una ficha de barco propia con acciones de gestión: alta, edición y baja.
- El administrador puede realizar alta, edición y baja de barcos desde el panel de administración.
- El sistema proporciona un panel de administración propio para gestión de barcos, clientes y reservas.

### HU-14 — Panel de administración de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede consultar clientes desde el panel de administración.
- El administrador puede eliminar clientes desde el panel de administración.
- El administrador no puede eliminar un usuario cliente si ese usuario tiene reservas pendientes.
- Se muestra un mensaje de error si se intenta eliminar un cliente con reservas pendientes.

### HU-15 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración mediante botones por transición aplicable.

**Criterios de aceptación**

- El administrador puede consultar el estado de cualquier reserva.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas mediante botones por transición aplicable.
- El administrador puede consultar y cambiar el estado de reservas desde el panel de administración.
- Solo se muestran transiciones válidas según el estado actual de la reserva.
