---
run_id: run_2026-05-14_16-05
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-14T16:16:40+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_16-05`

Total de historias: **8**

## Historias del sprint

### HU-14 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso si no estoy registrado.

**Criterios de aceptación**

- Existe una página pública para consultar el estado de una reserva por código de seguimiento.
- El cliente introduce el código de seguimiento en un formulario.
- El sistema muestra el estado actual de la reserva: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Se muestran los datos de la reserva: barco, rango de fechas e importe total.

### HU-15 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a una sección de mis reservas.
- Se muestra una lista de todas las reservas del cliente con su estado actual.
- Se muestran los datos de cada reserva: barco, rango de fechas, importe total y código de seguimiento.

### HU-16 — Cancelación de reserva pendiente de pago

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para eliminarla del sistema.

**Criterios de aceptación**

- El cliente puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- Se muestra un mensaje de confirmación antes de cancelar.

### HU-17 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con fecha de inicio en 24 horas.
- Se envía un correo de recordatorio al cliente con los datos de la reserva.
- El correo incluye un enlace para completar el pago o cancelar la reserva.

### HU-18 — Gestión de barcos en panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero gestionar barcos desde el panel de administración, realizando operaciones de alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a un panel de administración propio de la aplicación.
- El administrador puede crear un nuevo barco con todos sus datos: nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del sistema.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-19 — Gestión de clientes en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todos los clientes.
- El administrador puede ver los datos de cada cliente.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si un cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- La eliminación de un cliente se confirma antes de ejecutarse.

### HU-20 — Gestión de reservas en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración mediante botones por transición aplicable.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- Se muestra el estado actual de cada reserva: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El administrador puede cambiar el estado de una reserva mediante botones que representan transiciones válidas.
- Los cambios de estado se reflejan inmediatamente en el sistema.
- Se muestra un historial de cambios de estado para cada reserva.

### HU-21 — Ficha de barco para administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero acceder a una ficha de barco propia con acciones de gestión: alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a una ficha de barco desde el panel de administración.
- La ficha muestra todos los datos del barco.
- El administrador puede editar los datos del barco desde la ficha.
- El administrador puede eliminar el barco desde la ficha.
- El administrador puede crear un nuevo barco desde una ficha de alta.
