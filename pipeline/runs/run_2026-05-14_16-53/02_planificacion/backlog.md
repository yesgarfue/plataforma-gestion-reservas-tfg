---
run_id: run_2026-05-14_16-53
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T17:07:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-14_16-53`

Total de historias: **22**

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
- El sistema permite búsqueda de barcos por nombre o título.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- Los filtros de precio, categoría, capacidad y rango de fechas funcionan de forma independiente y combinable.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con etiqueta 'No disponible' los que no están disponibles en ese rango sin ocultarlos.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.

### HU-05 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha de un barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede acceder a la ficha de un barco desde el catálogo.
- La ficha visualiza todos los datos del barco e imagen.
- El cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta desde la ficha.

### HU-06 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero visualizar la cesta desde cualquier página, modificar las cantidades de barcos y revisar el estado de la cesta, para gestionar mis compras.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-07 — Reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como visitante, quiero completar una reserva sin haberme registrado previamente, para alquilar un barco sin crear una cuenta.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta sin estar registrado.
- El proceso de reserva se realiza en no más de tres pasos.
- Durante el proceso se solicitan los datos del cliente y los datos de pago.
- El cliente puede completar la reserva sin registro previo.

### HU-08 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como métodos de pago durante el proceso de reserva.

**Criterios de aceptación**

- El sistema ofrece PayPal Sandbox como método de pago.
- El sistema ofrece contra-reembolso como método de pago.
- El cliente puede seleccionar uno de los dos métodos durante el proceso de reserva.
- La integración de PayPal utiliza el entorno Sandbox, no producción.

### HU-09 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi alquiler.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva.

### HU-10 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en las reservas, excepto para barcos de categoría velero donde la tasa es 0 €.

**Criterios de aceptación**

- El sistema calcula la tasa de combustible como 50 € por día para barcos que no son velero.
- El sistema aplica tasa de combustible de 0 € para barcos de categoría velero.
- La tasa se incluye en el importe total de la reserva.
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-11 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas: PENDIENTE DE PAGO, PAGADO, EN USO y DEVUELTO.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El estado se actualiza según el flujo de la reserva.

### HU-12 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para dejar de alquilar el barco.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema sin dejar registro posterior.
- El cliente recibe una confirmación de cancelación.

### HU-13 — Recordatorio de reserva próxima

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de una reserva en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO que comienzan en un día.
- El sistema envía un correo de recordatorio al cliente.
- El correo contiene los datos de la reserva y el código de seguimiento.

### HU-14 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- El cliente puede ingresar el código de seguimiento sin estar registrado.
- El sistema muestra el estado actual de la reserva.
- El sistema muestra los datos del barco, rango de fechas e importe total.

### HU-15 — Consulta de reservas del cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta.

**Criterios de aceptación**

- El cliente registrado puede acceder a un listado de sus reservas.
- El listado muestra el estado de cada reserva.
- El cliente puede ver los detalles de cada reserva.

### HU-16 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero consultar el estado de cualquier reserva y cambiar su estado mediante botones por transición aplicable.

**Criterios de aceptación**

- El administrador puede acceder a un panel de reservas.
- El panel muestra todas las reservas del sistema.
- El administrador puede consultar el estado de cualquier reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Solo se muestran transiciones válidas según el estado actual.

### HU-17 — Gestión de barcos en panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero realizar alta, edición y baja de barcos desde el panel de administración.

**Criterios de aceptación**

- El administrador puede acceder a un panel de gestión de barcos.
- El administrador puede crear un nuevo barco con todos sus datos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del sistema.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-18 — Gestión de clientes en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede acceder a un panel de gestión de clientes.
- El administrador puede visualizar el listado de clientes.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- El administrador puede consultar las reservas de cada cliente.

### HU-19 — Ficha de barco para administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero acceder a una ficha de barco propia con acciones de gestión: alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a una ficha de barco desde el panel de administración.
- La ficha muestra todos los datos del barco.
- El administrador puede editar los datos del barco desde la ficha.
- El administrador puede eliminar el barco desde la ficha.
- El administrador puede crear un nuevo barco desde una ficha vacía.

### HU-20 — Login durante proceso de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero iniciar sesión durante el proceso de reserva y recuperar mi cesta al volver de la página de login.

**Criterios de aceptación**

- El cliente puede acceder a la página de login desde el proceso de reserva.
- Tras iniciar sesión, el cliente es redirigido al proceso de reserva.
- Los datos del cliente se heredan de la sesión iniciada.
- La cesta se mantiene y se recupera al volver del login.

### HU-21 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español para que la aplicación funcione correctamente.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- La interfaz de usuario está íntegramente en español.
- Las fechas y horas se muestran en formato español.

### HU-22 — Datos precargados de ejemplo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero que la aplicación arranque con datos precargados para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- La aplicación arranca con 2 puertos precargados.
- La aplicación arranca con 2 fabricantes precargados.
- La aplicación arranca con 2 categorías precargadas, incluyendo velero.
- La aplicación arranca con 1 usuario administrador de prueba.
- La aplicación arranca con 1 usuario cliente de prueba.
