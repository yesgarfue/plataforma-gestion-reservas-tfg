---
run_id: run_2026-05-12_16-48
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-12T17:03:51+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_16-48`

Total de historias: **7**

## Historias del sprint

### HU-14 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para asegurar que complete el pago a tiempo.

**Criterios de aceptación**

- Se identifica automáticamente las reservas que faltan un día para iniciarse y están en estado PENDIENTE DE PAGO.
- Se envía un correo recordatorio al cliente con los datos de la reserva.
- El correo se envía una sola vez por reserva.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido, para saber en qué punto está mi pedido sin necesidad de estar registrado.

**Criterios de aceptación**

- El cliente puede ingresar un código de seguimiento en un formulario de búsqueda.
- Se muestra el estado actual de la reserva asociada al código.
- Se muestran los datos del barco, el rango de fechas y el estado de la reserva.
- Si el código no existe, se muestra un mensaje de error.

### HU-16 — Consulta de reservas del cliente registrado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta, para tener un historial de mis pedidos.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- Se muestran los datos de cada reserva: barco, fechas, estado y código de seguimiento.
- El cliente puede ver el estado actual de cada reserva.

### HU-17 — Panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero acceder a un panel de administración propio diferente del admin de Django, para gestionar barcos, clientes y reservas.

**Criterios de aceptación**

- El panel de administración es accesible solo para usuarios administrador.
- El panel es diferente del admin de Django por defecto.
- El panel permite navegar entre gestión de barcos, clientes y reservas.
- El acceso al panel requiere autenticación.

### HU-18 — Gestión de barcos en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los barcos en el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede dar de alta nuevos barcos con todos los campos requeridos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede dar de baja un barco del sistema.
- Se valida que todos los campos obligatorios estén completos.
- La imagen del barco es obligatoria.

### HU-19 — Gestión de clientes en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes en el panel de administración, para mantener la base de datos de usuarios.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes registrados.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Se muestra un mensaje de error si se intenta eliminar un cliente con reservas pendientes.
- Se confirma la eliminación antes de proceder.

### HU-20 — Gestión de reservas en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de las reservas en el panel de administración, para gestionar el ciclo de vida de los pedidos.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas.
- El administrador puede cambiar el estado de una reserva mediante botones por transición.
- Se muestran los datos completos de cada reserva: cliente, barco, fechas, estado y código de seguimiento.
- Solo se permiten transiciones de estado válidas.
