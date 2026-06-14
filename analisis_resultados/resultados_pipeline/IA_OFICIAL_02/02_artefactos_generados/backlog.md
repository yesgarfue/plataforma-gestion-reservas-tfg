---
run_id: run_2026-05-18_16-37
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-18T16:52:09+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-18_16-37`

Total de historias: **25**

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
- El formulario valida que el correo no esté duplicado.

### HU-02 — Inicio de sesión

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

Como cliente autenticado, quiero cerrar sesión explícitamente, para terminar mi sesión de forma segura.

**Criterios de aceptación**

- El cliente puede acceder a una opción de cerrar sesión desde cualquier página.
- Al cerrar sesión, la sesión se invalida y el cliente es redirigido a la página principal.
- Tras cerrar sesión, el cliente no puede acceder a funcionalidades autenticadas sin volver a iniciar sesión.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las embarcaciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos se organizan por categorías.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- El catálogo es accesible sin necesidad de autenticación.

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título desde la página de inicio, para encontrar rápidamente la embarcación que me interesa.

**Criterios de aceptación**

- El sistema permite buscar barcos por nombre o título.
- La búsqueda filtra el catálogo en tiempo real o tras enviar el formulario.
- Si no hay resultados, se muestra un mensaje indicando que no se encontraron barcos.

### HU-06 — Filtros combinables de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero filtrar barcos por puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma combinable e independiente, para refinar mi búsqueda según mis necesidades.

**Criterios de aceptación**

- El sistema permite filtrar por puerto, fabricante, precio, categoría y capacidad de forma independiente.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con una etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.
- Los filtros se pueden combinar entre sí.
- Al aplicar filtros, el catálogo se actualiza mostrando solo los barcos que cumplen todos los criterios.

### HU-07 — Ficha de barco con selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha del barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta, para preparar mi reserva.

**Criterios de aceptación**

- El cliente puede acceder a la ficha del barco desde el catálogo.
- La ficha visualiza los datos del barco y su imagen.
- Desde la ficha, el cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta con la cantidad seleccionada.
- Si el barco no está disponible, el botón de añadir a la cesta está deshabilitado.

### HU-08 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la cesta siempre visible, modificar las cantidades de barcos y revisar el estado de la cesta desde el catálogo, para gestionar mis compras.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-09 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva sin haberme registrado previamente, para alquilar un barco sin obligación de crear una cuenta.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta sin estar registrado.
- El proceso de reserva se realiza en no más de tres pasos.
- Durante el proceso se solicitan los datos del cliente (nombre, correo, teléfono) y los datos de pago.
- Si el cliente está autenticado, los datos se heredan de su cuenta.
- El cliente puede completar la reserva sin registrarse.

### HU-10 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como métodos de pago, para completar mi reserva con la opción que prefiera.

**Criterios de aceptación**

- El sistema ofrece PayPal Sandbox como método de pago.
- El sistema ofrece contra-reembolso como método de pago.
- El cliente puede seleccionar uno de los dos métodos durante el proceso de reserva.
- La integración de PayPal utiliza el entorno Sandbox, no producción.

### HU-11 — Confirmación de reserva con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi alquiler.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-12 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en las reservas, excepto para barcos de categoría velero donde la tasa es 0 €, para calcular correctamente el importe total.

**Criterios de aceptación**

- El sistema aplica una tasa de combustible de 50 € por día a todas las reservas.
- Para barcos de categoría velero, la tasa de combustible es 0 €.
- El importe total de la reserva incluye la tasa de combustible calculada correctamente.
- El cliente ve el desglose del importe incluyendo la tasa de combustible antes de confirmar la reserva.

### HU-13 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO), para controlar el ciclo de vida de cada alquiler.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El estado se actualiza según las transiciones aplicables del flujo de negocio.
- El estado es visible para el cliente y el administrador.

### HU-14 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para deshacer mi alquiler si cambio de opinión.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- El cliente recibe una confirmación de la cancelación.

### HU-15 — Recordatorio de pago pendiente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para evitar que se pierda la reserva.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio.
- El correo contiene los datos de la reserva y un enlace para completar el pago.
- El recordatorio se envía automáticamente sin intervención manual.

### HU-16 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado, para hacer seguimiento de mi alquiler.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reservas por código de seguimiento.
- Introduciendo el código de seguimiento, el sistema muestra el estado actual de la reserva.
- La consulta es accesible sin necesidad de autenticación.
- Si el código no existe, se muestra un mensaje de error.

### HU-17 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para ver el historial y estado actual de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- El listado muestra el estado de cada reserva.
- El cliente puede ver los detalles de cada reserva.
- El listado solo muestra las reservas del cliente autenticado.

### HU-18 — Gestión administrativa de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los barcos del catálogo (alta, edición y baja), para mantener actualizado el inventario de embarcaciones.

**Criterios de aceptación**

- El administrador puede acceder a una ficha de barco propia con acciones de gestión.
- El administrador puede crear un nuevo barco (alta).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco (baja).
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-19 — Gestión administrativa de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes, con la restricción de no poder eliminar clientes que tengan reservas pendientes, para mantener la integridad de los datos.

**Criterios de aceptación**

- El administrador puede consultar el listado de clientes.
- El administrador puede ver los detalles de cada cliente.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, el botón de eliminar está deshabilitado y se muestra un mensaje explicativo.
- Al eliminar un cliente, se elimina su cuenta del sistema.

### HU-20 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar el estado de cualquier reserva y cambiar su estado mediante botones por transición aplicable, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede consultar el listado de todas las reservas.
- El administrador puede ver los detalles de cada reserva.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas.
- Los botones de transición solo muestran las transiciones aplicables según el estado actual.
- El cambio de estado se registra y es visible en el historial de la reserva.

### HU-21 — Inicio de sesión durante el proceso de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero iniciar sesión durante el proceso de reserva y recuperar mi cesta al volver de la página de login, para continuar mi compra sin perder los datos.

**Criterios de aceptación**

- El cliente puede acceder a un enlace de login desde el proceso de reserva.
- Al iniciar sesión, el cliente es redirigido de vuelta al proceso de reserva.
- La cesta se mantiene intacta tras el login.
- Los datos del cliente se heredan de su cuenta registrada.
- El cliente puede continuar el proceso de reserva sin perder información.

### HU-22 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español, para que la aplicación funcione con la configuración regional correcta.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- Las fechas y horas se muestran en la zona horaria correcta.
- La interfaz de usuario está íntegramente en español.

### HU-23 — Seguridad de formularios y contraseñas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero implementar medidas de seguridad en formularios y almacenamiento de contraseñas, para proteger los datos de los usuarios.

**Criterios de aceptación**

- Las contraseñas se almacenan usando el mecanismo estándar de Django, no en texto plano.
- CSRF está activo en todos los formularios.
- Se validan todos los formularios en el servidor.
- Los datos sensibles no se exponen en URLs o logs.

### HU-24 — Datos precargados de ejemplo

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
- Los datos se cargan automáticamente al iniciar la aplicación.

### HU-25 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación se entregue como contenedor Docker con instrucciones claras, para facilitar el despliegue y la ejecución.

**Criterios de aceptación**

- La aplicación incluye un Dockerfile.
- El Dockerfile contiene instrucciones para construir la imagen.
- Se proporciona un README con instrucciones de construcción y arranque.
- El contenedor arranca correctamente con los datos precargados.
- La aplicación es accesible tras arrancar el contenedor.
