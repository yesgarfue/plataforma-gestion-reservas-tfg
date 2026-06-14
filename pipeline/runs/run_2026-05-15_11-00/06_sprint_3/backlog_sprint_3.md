---
run_id: run_2026-05-15_11-00
fase: 06_sprint_3
agente: Script
modelo: deterministico
timestamp: 2026-05-15T11:09:45+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 3 — Backlog del sprint

**ID de ejecución**: `run_2026-05-15_11-00`

Total de historias: **9**

## Historias del sprint

### HU-14 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar mi reserva si aún está pendiente de pago, para desistir del alquiler.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- El cliente recibe un correo de confirmación de la cancelación.
- La reserva desaparece del listado del cliente.

### HU-15 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue pendiente de pago, para evitar que olvide completar el pago.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con fecha de inicio en menos de 24 horas.
- Se envía un correo de recordatorio al cliente con los datos de la reserva y un enlace para completar el pago.
- El correo incluye el código de seguimiento.

### HU-16 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, para saber el estado de mi alquiler sin necesidad de estar registrado.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- Introduce el código de seguimiento y accede a los detalles de la reserva.
- Se muestra el estado actual, los datos del barco, el rango de fechas y el importe total.
- No se requiere autenticación para consultar.

### HU-17 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado accede a una sección 'Mis reservas' en su cuenta.
- Se muestra un listado de todas sus reservas con estado, barco, fechas e importe.
- El cliente puede pulsar sobre una reserva para ver los detalles completos.
- Se muestran tanto reservas activas como históricas.

### HU-18 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de cualquier reserva desde el panel de administración, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador accede a un panel de administración propio de la aplicación.
- El panel muestra un listado de todas las reservas con estado, cliente, barco, fechas e importe.
- El administrador puede pulsar sobre una reserva para ver los detalles completos.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Se registra quién y cuándo cambió el estado.

### HU-19 — Gestión de barcos por administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero realizar operaciones de alta, edición y baja de barcos desde el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador accede a una sección de gestión de barcos en el panel de administración.
- Puede crear un nuevo barco introduciendo nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Puede editar los datos de un barco existente.
- Puede eliminar un barco del catálogo.
- Al eliminar un barco, se valida que no tenga reservas activas.

### HU-20 — Gestión de clientes por administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, para mantener la base de datos de usuarios.

**Criterios de aceptación**

- El administrador accede a una sección de gestión de clientes en el panel de administración.
- Se muestra un listado de todos los clientes con correo, nombre y número de reservas.
- El administrador puede pulsar sobre un cliente para ver sus detalles y reservas.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Al intentar eliminar un cliente con reservas pendientes, se muestra un mensaje de error indicando la restricción.

### HU-21 — Ficha de barco para administrador

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero acceder a una ficha de barco propia con acciones de gestión, para administrar los detalles de cada barco.

**Criterios de aceptación**

- El administrador puede acceder a la ficha de un barco desde el panel de administración.
- La ficha muestra todos los datos del barco: nombre, imagen, categoría, fabricante, puerto, capacidad, precio por día.
- El administrador puede editar cualquier campo desde la ficha.
- El administrador puede eliminar el barco desde la ficha.
- El administrador puede ver el historial de reservas del barco.

### HU-23 — Acceso al modo administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero acceder al panel de administración de la aplicación, para gestionar barcos, clientes y reservas.

**Criterios de aceptación**

- El administrador puede acceder al panel de administración desde un enlace en la página principal o desde su cuenta.
- El panel muestra secciones para gestión de barcos, clientes y reservas.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.
- El administrador puede salir del modo administrador y volver a la vista de cliente.
