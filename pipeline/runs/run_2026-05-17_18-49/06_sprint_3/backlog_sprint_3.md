---
run_id: run_2026-05-17_18-49
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-17T19:43:33+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-17_18-49`

Total de historias: **7**

## Historias del sprint

### HU-14 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con fecha de inicio en el próximo día.
- Se envía un correo de recordatorio al cliente con los datos de la reserva.
- El correo incluye un enlace o código para completar el pago o consultar el estado.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso si no estoy registrado.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- Introduciendo el código de seguimiento, se muestra el estado actual de la reserva.
- Se muestran los datos de la reserva: barco, fechas, importe, estado.
- No se requiere estar registrado para consultar la reserva.

### HU-16 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a una sección de mis reservas.
- Se muestran todas las reservas del cliente con su estado actual.
- Se muestran los datos de cada reserva: barco, fechas, importe, estado.
- El cliente puede acceder a la ficha de cada reserva para más detalles.

### HU-17 — Panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero acceder a un panel de administración propio de la aplicación para gestionar barcos, clientes y reservas.

**Criterios de aceptación**

- Existe un panel de administración accesible solo para administradores.
- El panel proporciona acceso a la gestión de barcos, clientes y reservas.
- El panel está íntegramente en español.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-18 — Gestión de barcos en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero realizar alta, edición y baja de barcos desde el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede crear un nuevo barco con todos sus datos (nombre, imagen, categoría, fabricante, puerto, capacidad, precio por día).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- Los cambios se reflejan inmediatamente en el catálogo visible para los clientes.
- Existe una ficha de barco propia del administrador con acciones de gestión: alta, edición y baja.

### HU-19 — Gestión de clientes en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes registrados.
- El administrador puede ver los datos de cada cliente.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si un cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- Se valida la restricción antes de permitir la eliminación.

### HU-20 — Gestión de reservas en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas.
- El administrador puede filtrar reservas por estado, cliente, barco o rango de fechas.
- El administrador puede ver los datos completos de cada reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Los cambios de estado se registran y se reflejan inmediatamente.
