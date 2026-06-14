---
run_id: run_2026-05-13_15-33
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-13T15:53:10+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-13_15-33`

Total de historias: **9**

## Historias del sprint

### HU-04 — Eliminación de cliente por administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero eliminar un cliente si no tiene reservas pendientes, para mantener la base de datos limpia.

**Criterios de aceptación**

- El administrador puede acceder a un listado de clientes desde el panel de administración.
- El administrador puede eliminar un cliente solo si no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- Tras la eliminación, el cliente desaparece del sistema.

### HU-14 — Estados de reserva y transiciones

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO) para controlar el ciclo de vida de cada reserva.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Una reserva comienza en estado PENDIENTE DE PAGO.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas.
- Las transiciones de estado se registran en el sistema.

### HU-15 — Cancelación de reserva en estado PENDIENTE DE PAGO

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO, para poder desistir antes de realizar el pago.

**Criterios de aceptación**

- El cliente puede cancelar una reserva solo si está en estado PENDIENTE DE PAGO.
- Si la reserva está en otro estado, no aparece la opción de cancelación.
- Al cancelar, la reserva se elimina del sistema.
- Se muestra un mensaje de confirmación antes de cancelar.

### HU-16 — Correo de recordatorio de pago pendiente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para evitar que olvide completar el pago.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con inicio en 24 horas.
- Se envía un correo de recordatorio al cliente.
- El correo incluye los datos de la reserva y un enlace para completar el pago.
- El recordatorio se envía una sola vez por reserva.

### HU-17 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento, para verificar el progreso sin necesidad de estar registrado.

**Criterios de aceptación**

- El cliente puede ingresar un código de seguimiento en un formulario de búsqueda.
- El sistema muestra el estado actual de la reserva.
- Se muestran los datos de la reserva (barco, fechas, importe).
- La búsqueda es accesible sin autenticación.

### HU-18 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta, para tener un historial de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- Se muestra el estado de cada reserva.
- Se muestran los datos de cada reserva (barco, fechas, importe).
- El cliente puede filtrar por estado de reserva.

### HU-19 — Consulta de reservas por administrador

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar el estado de cualquier reserva en el sistema, para supervisar todas las transacciones.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- Se muestra el estado de cada reserva.
- Se muestran los datos de cada reserva (cliente, barco, fechas, importe).
- El administrador puede filtrar por estado, cliente o barco.

### HU-20 — Panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero acceder a un panel de administración propio de la aplicación, para gestionar barcos, clientes y reservas.

**Criterios de aceptación**

- Existe un panel de administración accesible solo para administradores.
- El panel proporciona acceso a la gestión de barcos.
- El panel proporciona acceso a la gestión de clientes.
- El panel proporciona acceso a la gestión de reservas.
- El panel muestra estadísticas o resúmenes del sistema.

### HU-21 — Gestión de barcos (alta, edición, baja)

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero crear, editar y eliminar barcos en el sistema, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede crear un nuevo barco con todos sus campos (nombre, imagen, categoría, fabricante, puerto, capacidad, precio).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- Se valida que los datos del barco sean correctos antes de guardar.
- Se muestra un mensaje de confirmación tras cada operación.
