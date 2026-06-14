---
run_id: run_2026-05-11_13-11
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-11T13:24:03+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-11_13-11`

Total de historias: **27**

## Historias

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Las contraseñas se almacenan de forma segura (hasheadas).
- No se permite registrar dos clientes con el mismo correo electrónico.

### HU-02 — Inicio de sesión de cliente

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- La sesión se mantiene activa durante la navegación.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para asegurar que mi cuenta no queda abierta en dispositivos compartidos.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón 'Cerrar sesión'.
- Tras cerrar sesión, el cliente es redirigido a la página de inicio.
- La sesión se elimina del servidor.
- El cliente no puede acceder a funcionalidades autenticadas tras cerrar sesión.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías, para explorar las opciones disponibles de forma ordenada.

**Criterios de aceptación**

- El catálogo muestra todos los barcos disponibles.
- Los barcos están agrupados por categoría.
- Cada barco muestra nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El catálogo es accesible sin autenticación.

### HU-05 — Búsqueda y filtros combinables en catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar barcos por nombre y aplicar filtros combinables (puertos, fabricantes, precio, categoría, capacidad, rango de fechas), para encontrar rápidamente el barco que necesito.

**Criterios de aceptación**

- El cliente puede buscar por nombre o título del barco.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El cliente puede filtrar por precio (rango).
- El cliente puede filtrar por categoría.
- El cliente puede filtrar por capacidad.
- El cliente puede filtrar por rango de fechas de disponibilidad.
- Los filtros se pueden combinar entre sí.
- Los resultados se actualizan al aplicar o cambiar filtros.

### HU-06 — Visualización de disponibilidad de barcos

- **Prioridad**: Baja
- **Estimación**: S

**Descripción**

Como cliente, quiero ver claramente cuáles barcos están agotados o no disponibles, para evitar intentar reservar barcos que no puedo alquilar.

**Criterios de aceptación**

- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- El cliente no puede añadir a la cesta un barco no disponible.
- Se indica el motivo de la no disponibilidad (agotado, fuera de servicio, etc.).

### HU-07 — Ficha detallada del barco

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la ficha detallada de un barco con todos sus datos e imagen, para tomar una decisión informada antes de reservar.

**Criterios de aceptación**

- La ficha muestra nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- La ficha es accesible desde el catálogo.
- La ficha muestra información clara y legible.

### HU-08 — Selección de cantidad y adición a cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero seleccionar la cantidad de unidades de un barco y añadirlo a la cesta, para preparar mi reserva.

**Criterios de aceptación**

- El cliente puede seleccionar una cantidad numérica en la ficha del barco.
- El cliente puede hacer clic en 'Añadir a la cesta'.
- El barco se añade a la cesta con la cantidad seleccionada.
- Se muestra un mensaje de confirmación.
- La cantidad no puede ser negativa ni cero.

### HU-09 — Visualización permanente de la cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la cesta siempre visible desde cualquier página de la aplicación, para saber en todo momento qué he añadido.

**Criterios de aceptación**

- La cesta es visible en todas las páginas de la aplicación.
- La cesta muestra el número de artículos o el importe total.
- El cliente puede acceder a la cesta desde cualquier página.
- La cesta persiste durante la sesión del cliente.

### HU-10 — Modificación de la cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ampliar o reducir la cantidad de unidades de cada barco en la cesta, para ajustar mi reserva antes de finalizar la compra.

**Criterios de aceptación**

- El cliente puede aumentar la cantidad de un barco en la cesta.
- El cliente puede disminuir la cantidad de un barco en la cesta.
- El cliente puede eliminar completamente un barco de la cesta.
- Los cambios se reflejan inmediatamente en el total.
- Si la cantidad llega a cero, el barco se elimina de la cesta.

### HU-11 — Vaciado de cesta al entrar como administrador

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador, quiero que la cesta se vacíe automáticamente al entrar en modo administrador, para evitar confusiones entre compras de cliente y gestión administrativa.

**Criterios de aceptación**

- Al cambiar a modo administrador, la cesta se vacía completamente.
- El administrador no puede añadir barcos a la cesta mientras está en modo administrador.
- Si el administrador vuelve a modo cliente, la cesta anterior se recupera o se inicia vacía.

### HU-12 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como visitante, quiero completar una reserva en no más de tres pasos sin necesidad de registrarme previamente, para agilizar el proceso de compra.

**Criterios de aceptación**

- El proceso de reserva consta de no más de tres pasos.
- El cliente puede completar la reserva sin estar registrado.
- Se solicitan los datos necesarios (nombre, correo, teléfono, etc.) durante el proceso.
- Al finalizar, se ofrece la opción de registrarse o continuar como visitante.

### HU-13 — Inicio de sesión durante la reserva con recuperación de cesta

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero poder iniciar sesión durante el proceso de reserva y recuperar mi cesta anterior, para continuar con mi compra sin perder los datos.

**Criterios de aceptación**

- El cliente puede iniciar sesión en cualquier paso del proceso de reserva.
- Tras iniciar sesión, la cesta anterior del cliente se recupera.
- Los datos de la cesta se combinan correctamente con los nuevos artículos si los hay.
- El cliente puede continuar con el proceso de reserva tras iniciar sesión.

### HU-14 — Pago mediante PayPal Sandbox y contra-reembolso

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero poder elegir entre dos métodos de pago (PayPal Sandbox y contra-reembolso) para completar mi reserva de forma segura.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- Si elige PayPal, se redirige a la pasarela de PayPal Sandbox.
- Si elige contra-reembolso, se confirma la reserva sin pago inmediato.
- La reserva se crea con el estado correspondiente según el método elegido.

### HU-15 — Cálculo de tasa de combustible

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, debo aplicar una tasa de combustible de 50 € por día a todas las reservas, excepto para veleros, para reflejar correctamente el coste total.

**Criterios de aceptación**

- Se aplica una tasa de 50 € por día para barcos que no son veleros.
- Los veleros no tienen tasa de combustible.
- La tasa se calcula correctamente en función del número de días de la reserva.
- El importe total incluye la tasa de combustible (excepto para veleros).

### HU-16 — Correo de confirmación con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico tras finalizar la compra con los datos del barco, rango de fechas, importe total y código de seguimiento, para tener constancia de mi reserva.

**Criterios de aceptación**

- Se envía un correo electrónico al cliente tras completar la reserva.
- El correo incluye nombre y datos del barco reservado.
- El correo incluye el rango de fechas de la reserva.
- El correo incluye el importe total.
- El correo incluye un código de seguimiento único.
- El código de seguimiento es válido para consultar el estado de la reserva.

### HU-17 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, debo gestionar los estados de las reservas (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO) para reflejar el ciclo de vida de cada alquiler.

**Criterios de aceptación**

- Cada reserva tiene uno de los cuatro estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO o PAGADO según el método de pago.
- El estado se actualiza correctamente en la base de datos.
- El estado es visible para el cliente y el administrador.

### HU-18 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero poder cancelar mi reserva si aún está en estado PENDIENTE DE PAGO, para cambiar de opinión antes de confirmar el pago.

**Criterios de aceptación**

- El cliente puede cancelar una reserva en estado PENDIENTE DE PAGO.
- No se puede cancelar una reserva en otros estados.
- Al cancelar, la reserva se elimina del sistema.
- Se muestra un mensaje de confirmación antes de cancelar.
- Se envía un correo de confirmación de cancelación al cliente.

### HU-19 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, debo enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para evitar que olvide completar el pago.

**Criterios de aceptación**

- Se identifica automáticamente las reservas con estado PENDIENTE DE PAGO que comienzan mañana.
- Se envía un correo de recordatorio al cliente.
- El correo incluye los datos de la reserva y un enlace para completar el pago.
- El recordatorio se envía una sola vez por reserva.

### HU-20 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por correo, para saber en qué punto está mi alquiler sin necesidad de estar registrado.

**Criterios de aceptación**

- El cliente puede acceder a un formulario de búsqueda por código de seguimiento.
- Al introducir un código válido, se muestra el estado de la reserva.
- Se muestra el nombre del barco, fechas y estado actual.
- Si el código no existe, se muestra un mensaje de error.
- No se requiere autenticación para esta consulta.

### HU-21 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta, para tener un historial de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- El listado muestra todas las reservas del cliente (pasadas y futuras).
- Cada reserva muestra barco, fechas, estado e importe.
- El cliente puede hacer clic en una reserva para ver detalles.
- El cliente puede cancelar una reserva si está en estado PENDIENTE DE PAGO.

### HU-22 — Gestión de barcos en panel administrativo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los barcos (alta, edición, baja) desde el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede crear un nuevo barco con todos sus datos (nombre, imagen, categoría, fabricante, puerto, capacidad, precio).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del sistema.
- Los cambios se reflejan inmediatamente en el catálogo.
- Se validan los datos antes de guardar.

### HU-23 — Gestión de clientes en panel administrativo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar clientes con reservas pendientes.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes.
- El administrador puede ver los detalles de un cliente (correo, nombre, reservas).
- El administrador puede eliminar un cliente si no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje de error al intentar eliminar.
- Se solicita confirmación antes de eliminar un cliente.

### HU-24 — Gestión de reservas en panel administrativo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de las reservas desde el panel de administración, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas.
- El administrador puede filtrar reservas por estado, cliente o barco.
- El administrador puede ver los detalles completos de una reserva.
- El administrador puede cambiar el estado de una reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO).
- Los cambios de estado se guardan correctamente en la base de datos.

### HU-25 — Consulta de reservas por administrador

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador, quiero consultar el estado de cualquier reserva en el sistema, para supervisar todas las operaciones de alquiler.

**Criterios de aceptación**

- El administrador puede acceder a un listado completo de todas las reservas.
- El listado muestra cliente, barco, fechas, estado e importe.
- El administrador puede buscar una reserva por código de seguimiento.
- El administrador puede filtrar por estado, cliente o barco.
- Se muestra información detallada al hacer clic en una reserva.

### HU-26 — Carga de datos de ejemplo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, debo arrancar con datos precargados (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, 1 usuario administrador, 1 usuario cliente) para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación carga automáticamente 5 barcos al iniciar.
- Se crean 2 puertos en la base de datos.
- Se crean 2 fabricantes en la base de datos.
- Se crean 2 categorías en la base de datos.
- Se crea 1 usuario administrador con credenciales predefinidas.
- Se crea 1 usuario cliente con credenciales predefinidas.
- Los datos se cargan de forma fiable en cada arranque del contenedor.

### HU-27 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, debo configurar la zona horaria a Europe/Madrid y el locale a español para que todas las fechas, horas y textos se muestren correctamente.

**Criterios de aceptación**

- La zona horaria del proyecto Django es Europe/Madrid.
- El locale del proyecto es español.
- Las fechas se muestran en formato español (dd/mm/yyyy).
- Las horas se muestran en zona horaria de Madrid.
- Los textos de la interfaz están en español.
