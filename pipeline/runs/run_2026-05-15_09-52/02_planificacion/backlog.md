---
run_id: run_2026-05-15_09-52
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-15T09:58:14+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-15_09-52`

Total de historias: **21**

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

Como cliente, quiero visualizar un catálogo de barcos organizado por categorías y filtrar por puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma combinable, para encontrar el barco que necesito.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El cliente puede filtrar por precio, categoría, capacidad y rango de fechas de forma independiente.
- Los filtros son combinables entre sí.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- El filtro de fechas muestra todos los barcos del catálogo marcando con etiqueta 'No disponible' aquellos no disponibles en ese rango, sin ocultarlos.

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título, para localizar rápidamente un barco específico.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de búsqueda.
- El sistema filtra los barcos del catálogo por nombre o título que coincidan con el término.
- La búsqueda es sensible a mayúsculas y minúsculas o realiza búsqueda insensible según implementación.

### HU-06 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha de un barco desde el catálogo, visualizar sus datos e imagen, y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede pulsar sobre un barco en el catálogo para acceder a su ficha.
- La ficha muestra todos los datos del barco e imagen.
- El cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta desde la ficha.

### HU-07 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero visualizar mi cesta desde cualquier página, modificar las cantidades de barcos y vaciarla, para gestionar mis reservas antes de finalizar la compra.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-08 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin haberse registrado previamente, proporcionando mis datos y datos de pago, para alquilar un barco sin trámites previos.

**Criterios de aceptación**

- El proceso de reserva se realiza en no más de tres pasos.
- No se exige registro previo para completar una reserva.
- Durante el proceso se solicitan los datos del cliente y datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.

### HU-09 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como métodos de pago, para completar mi reserva con la opción que prefiera.

**Criterios de aceptación**

- El sistema ofrece PayPal Sandbox como método de pago.
- El sistema ofrece contra-reembolso como método de pago.
- El cliente puede seleccionar uno de los dos métodos durante el proceso de reserva.
- La integración de PayPal utiliza el entorno Sandbox, no producción.

### HU-10 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva.

### HU-11 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en las reservas, excepto para barcos de categoría velero donde la tasa es 0 €, para calcular correctamente el importe total.

**Criterios de aceptación**

- El sistema aplica una tasa de combustible de 50 € por día a todas las reservas.
- Para barcos de categoría velero, la tasa de combustible es 0 €.
- El importe total de la reserva incluye la tasa de combustible calculada correctamente.

### HU-12 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero que cada reserva tenga uno de los estados PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO, para gestionar el ciclo de vida de las reservas.

**Criterios de aceptación**

- Cada reserva se crea en estado PENDIENTE DE PAGO.
- El sistema permite transiciones entre estados según las reglas de negocio.
- El estado de una reserva es visible para el cliente y el administrador.

### HU-13 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para eliminarla del sistema si cambio de opinión.

**Criterios de aceptación**

- El cliente puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- No se puede cancelar una reserva en otros estados.

### HU-14 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para evitar que se pierda la reserva.

**Criterios de aceptación**

- El sistema identifica reservas que vencen en un día y están en estado PENDIENTE DE PAGO.
- Se envía un correo de recordatorio al cliente con los datos de la reserva.
- El correo incluye instrucciones para completar el pago.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado, para hacer seguimiento de mi alquiler.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- Introduciendo el código, el sistema muestra el estado actual de la reserva.
- No se requiere estar registrado para consultar por código de seguimiento.
- Se muestra el estado, datos del barco, rango de fechas e importe total.

### HU-16 — Consulta de reservas del cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta, para hacer seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente registrado puede acceder a un listado de sus reservas.
- El listado muestra el estado, datos del barco, rango de fechas e importe de cada reserva.
- El cliente puede filtrar o buscar sus reservas.

### HU-17 — Panel de administración de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero gestionar barcos desde un panel de administración propio, realizando alta, edición y baja de barcos, para mantener el catálogo actualizado.

**Criterios de aceptación**

- Existe un panel de administración propio de la aplicación.
- El administrador puede crear un nuevo barco con todos sus datos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- El panel muestra un listado de todos los barcos con opciones de acción.

### HU-18 — Panel de administración de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes, para gestionar la base de clientes.

**Criterios de aceptación**

- El administrador puede consultar un listado de todos los clientes.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si un cliente tiene reservas pendientes, el botón de eliminar está deshabilitado o muestra un mensaje de error.
- El panel muestra información relevante de cada cliente.

### HU-19 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración, para gestionar el ciclo de vida de las reservas.

**Criterios de aceptación**

- El administrador puede consultar un listado de todas las reservas.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- El panel muestra el estado actual, datos del barco, cliente, rango de fechas e importe de cada reserva.
- Solo se muestran transiciones válidas según el estado actual.

### HU-20 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español, para que la aplicación funcione con la zona horaria y el idioma correcto.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- Las fechas y horas se muestran en la zona horaria correcta.
- La interfaz de usuario está íntegramente en español.

### HU-21 — Datos precargados de ejemplo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero que la aplicación arranque con datos precargados de ejemplo, para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- Hay 2 puertos precargados.
- Hay 2 fabricantes precargados.
- Hay 2 categorías precargadas, incluyendo velero.
- Hay 1 usuario administrador de prueba precargado.
- Hay 1 usuario cliente de prueba precargado.
- Los datos se cargan de forma fiable en cada arranque.
