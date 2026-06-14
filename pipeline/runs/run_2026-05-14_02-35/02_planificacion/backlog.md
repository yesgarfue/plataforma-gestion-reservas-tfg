---
run_id: run_2026-05-14_02-35
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T02:43:53+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-14_02-35`

Total de historias: **23**

## Historias

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Las contraseñas se almacenan usando el mecanismo estándar de Django, no en texto plano.
- Tras registrarse, el cliente queda autenticado en la sesión.
- El formulario incluye validación CSRF.

### HU-02 — Inicio de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- El formulario incluye validación CSRF.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para salir de mi cuenta de forma segura.

**Criterios de aceptación**

- El cliente puede pulsar un botón de cierre de sesión desde cualquier página.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se elimina del servidor.

### HU-04 — Catálogo de barcos con filtros combinables

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías y aplicar filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas, para encontrar el barco que necesito.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con campos de nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El cliente puede buscar barcos por nombre o título desde la página de inicio.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El cliente puede aplicar filtros de puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma simultánea e independiente.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con una etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.

### HU-05 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha de un barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede acceder a la ficha del barco desde el catálogo.
- La ficha visualiza los datos del barco y su imagen.
- Desde la ficha de barco, el cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco seleccionado a la cesta.
- Se valida que la cantidad seleccionada no exceda la disponibilidad.

### HU-06 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la cesta siempre visible, modificar las cantidades de barcos y revisar el estado de la cesta desde el catálogo.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-07 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin haberse registrado previamente, proporcionando datos del cliente y datos de pago.

**Criterios de aceptación**

- El cliente puede completar una reserva sin haberse registrado previamente.
- El proceso de reserva se realiza en no más de tres pasos.
- Durante el proceso de reserva se solicitan los datos del cliente y los datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.
- Desde la cesta el usuario puede finalizar la compra iniciando el proceso de reserva.

### HU-08 — Pago mediante PayPal Sandbox

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero pagar mi reserva mediante PayPal Sandbox, para completar la transacción de forma segura.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- La integración de PayPal utiliza el entorno Sandbox, no producción.
- El cliente es redirigido a PayPal para completar el pago.
- Tras completar el pago en PayPal, el cliente regresa a la aplicación.
- El estado de la reserva se actualiza a PAGADO tras un pago exitoso.

### HU-09 — Pago mediante contra-reembolso

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero pagar mi reserva mediante contra-reembolso, para completar la reserva sin pagar en línea.

**Criterios de aceptación**

- El cliente puede seleccionar contra-reembolso como método de pago.
- Al seleccionar contra-reembolso, la reserva se crea en estado PENDIENTE DE PAGO.
- El cliente recibe un correo de confirmación con los datos de la reserva.

### HU-10 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-11 — Cálculo de tarifa con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el importe total de la reserva considerando el precio diario del barco, la cantidad de días y una tasa de combustible diferenciada por categoría.

**Criterios de aceptación**

- Los alquileres se miden por día.
- Se aplica una tasa de combustible de 50 euros por día para todos los barcos.
- Para barcos de categoría velero, la tasa de combustible es 0 euros.
- El importe total se calcula como: (precio_diario * cantidad_dias * cantidad_barcos) + (tasa_combustible * cantidad_dias * cantidad_barcos).
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-12 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente no registrado, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, para conocer el estado de mi alquiler.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- Ingresando el código de seguimiento, se muestra el estado actual de la reserva.
- Se muestran los datos del barco, rango de fechas e importe total.
- No se requiere estar registrado para consultar la reserva.

### HU-13 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El usuario registrado puede acceder a un listado de sus reservas.
- Se muestra el estado de cada reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO).
- Se muestran los datos del barco, rango de fechas e importe total de cada reserva.
- El cliente puede acceder a esta funcionalidad desde su cuenta.

### HU-14 — Cancelación de reserva en estado PENDIENTE DE PAGO

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar mi reserva si está en estado PENDIENTE DE PAGO, para anular mi alquiler sin dejar registro.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema sin quedar registrada con un estado posterior.
- El cliente recibe una confirmación de la cancelación.
- Las reservas en otros estados no pueden ser canceladas por el cliente.

### HU-15 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de una reserva en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario.
- El correo contiene los datos de la reserva y un enlace para completar el pago.
- El recordatorio se envía automáticamente sin intervención manual.

### HU-16 — Gestión de barcos en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar barcos desde el panel de administración, realizando operaciones de alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a un panel de administración propio de la aplicación.
- El administrador puede crear nuevos barcos con todos los campos requeridos (nombre, imagen, categoría, fabricante, puerto, capacidad, precio por día).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del sistema.
- Al eliminar un barco, se valida que no tenga reservas activas.

### HU-17 — Gestión de clientes en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando restricciones de seguridad.

**Criterios de aceptación**

- El administrador puede acceder a un listado de clientes.
- El administrador puede visualizar los datos de cada cliente.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Al intentar eliminar un cliente con reservas pendientes, se muestra un mensaje de error explicativo.
- Se mantiene un registro de auditoría de eliminaciones.

### HU-18 — Gestión de reservas en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- El administrador puede visualizar los datos completos de cada reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Las transiciones de estado válidas son: PENDIENTE DE PAGO → PAGADO, PAGADO → EN USO, EN USO → DEVUELTO.
- Se muestra un historial de cambios de estado para cada reserva.

### HU-19 — Ficha de barco para administrador

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador, quiero acceder a una ficha de barco propia con acciones de gestión de alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a una ficha de barco desde el panel de administración.
- La ficha muestra todos los datos del barco.
- El administrador puede crear un nuevo barco desde la ficha.
- El administrador puede editar los datos del barco.
- El administrador puede eliminar el barco.

### HU-20 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria a Europe/Madrid y el locale a español para que la aplicación funcione en el contexto correcto.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado como español.
- Todas las fechas y horas se muestran en la zona horaria Europe/Madrid.
- Los formatos de fecha y número siguen la convención española.

### HU-21 — Interfaz de usuario en español

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como usuario, quiero que la interfaz de usuario esté íntegramente en español, para una mejor comprensión y usabilidad.

**Criterios de aceptación**

- Todos los textos de la interfaz están en español.
- Los mensajes de error están en español.
- Los botones, etiquetas y campos están en español.
- Los correos electrónicos están en español.

### HU-22 — Datos precargados en arranque

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como desarrollador, quiero que la aplicación arranque con datos de ejemplo precargados para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- Hay 2 puertos precargados.
- Hay 2 fabricantes precargados.
- Hay 2 categorías precargadas, incluyendo velero.
- Hay 1 usuario administrador de prueba precargado.
- Hay 1 usuario cliente de prueba precargado.
- Los datos se cargan automáticamente en cada arranque del contenedor.

### HU-23 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación se entregue como contenedor Docker con instrucciones claras de construcción y arranque.

**Criterios de aceptación**

- La aplicación incluye un Dockerfile.
- El Dockerfile contiene instrucciones para construir la imagen.
- Se incluye un README con instrucciones de construcción del contenedor.
- Se incluye un README con instrucciones de arranque del contenedor.
- El contenedor arranca correctamente con los datos precargados.
