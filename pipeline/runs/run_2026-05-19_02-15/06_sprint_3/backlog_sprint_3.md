---
run_id: run_2026-05-19_02-15
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-19T02:56:07+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-19_02-15`

Total de historias: **7**

## Historias del sprint

### HU-13 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva en estado PENDIENTE DE PAGO, para anular mi alquiler si cambio de opinión.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- El cliente recibe una confirmación de cancelación por correo.
- La cancelación es irreversible.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

**Criterios de aceptación**

- El cliente puede consultar el estado de su reserva usando el código de seguimiento.
- No es necesario estar registrado para consultar por código de seguimiento.
- Se muestra el estado actual, datos del barco, rango de fechas e importe total.
- Si el código no existe, se muestra un mensaje de error.

### HU-16 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El usuario registrado puede consultar el estado de sus reservas desde su cuenta.
- Se muestran todas las reservas del cliente con su estado actual.
- Se pueden filtrar por estado de reserva.
- Se muestra el código de seguimiento de cada reserva.

### HU-17 — Panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero acceder a un panel de administración propio de la aplicación para gestionar barcos, clientes y reservas.

**Criterios de aceptación**

- Existe un panel de administración propio de la aplicación.
- El panel permite gestión de barcos, clientes y reservas.
- Solo los usuarios administradores pueden acceder al panel.
- El panel está íntegramente en español.
- El acceso al panel requiere autenticación.

### HU-18 — Gestión de barcos en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero realizar operaciones de alta, edición y baja de barcos desde el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede crear nuevos barcos con todos los campos requeridos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- Se validan todos los formularios de gestión de barcos.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-19 — Gestión de clientes en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede consultar la lista de clientes.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si se intenta eliminar un cliente con reservas pendientes, se muestra un mensaje de error.
- Se muestra el historial de reservas de cada cliente.
- La eliminación de un cliente es irreversible.

### HU-20 — Gestión de reservas en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede consultar el estado de cualquier reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Se muestra el historial de cambios de estado de cada reserva.
- Se validan las transiciones de estado permitidas.
- Los cambios se registran con fecha y hora.
