---
run_id: run_2026-05-14_11-32
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T11:41:59+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-14_11-32`

Total de historias: **17**

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
- El filtro de fechas muestra todos los barcos del catálogo, marcando con etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- Los filtros funcionan de forma combinable e independiente.
- El sistema permite búsqueda de barcos por nombre o título desde la página de inicio.

### HU-05 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha de barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede acceder a la ficha de barco desde el catálogo.
- La ficha muestra los datos del barco e imagen.
- Desde la ficha, el cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta con la cantidad seleccionada.

### HU-06 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero visualizar, modificar y vaciar mi cesta desde cualquier página de la aplicación, para gestionar mis barcos antes de reservar.

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

- El proceso de reserva se realiza en no más de tres pasos.
- No se exige registro previo para completar una reserva.
- Durante el proceso se solicitan los datos del cliente y datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.
- Desde la cesta el usuario puede finalizar la compra iniciando el proceso de reserva.

### HU-08 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como métodos de pago durante la reserva.

**Criterios de aceptación**

- El sistema ofrece PayPal Sandbox como método de pago.
- El sistema ofrece contra-reembolso como método de pago.
- El cliente puede seleccionar uno de los dos métodos durante el proceso de reserva.
- La integración de PayPal utiliza el entorno Sandbox, no producción.

### HU-09 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo incluye datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-10 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en todas las reservas, excepto para barcos de categoría velero donde la tasa es 0 €.

**Criterios de aceptación**

- El sistema aplica una tasa de combustible de 50 € por día a todas las reservas.
- Para barcos de categoría velero, la tasa de combustible es 0 €.
- La tasa se incluye en el importe total de la reserva.
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-11 — Estados de reserva y cancelación

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero poder cancelar mi reserva si está en estado PENDIENTE DE PAGO, y consultar el estado de mis reservas en cualquier momento.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar una reserva en estado PENDIENTE DE PAGO, la reserva se elimina del sistema sin dejar registro posterior.
- El usuario registrado puede consultar el estado de sus reservas desde su cuenta.
- El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

### HU-12 — Recordatorio de reserva pendiente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario.
- El correo incluye los datos de la reserva y un enlace para consultar el estado.

### HU-13 — Panel de administración de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar barcos desde el panel de administración, realizando alta, edición y baja de barcos.

**Criterios de aceptación**

- El administrador dispone de una ficha de barco propia con acciones de gestión: alta, edición y baja.
- El administrador puede realizar alta, edición y baja de barcos desde el panel de administración.
- El sistema proporciona un panel de administración propio para gestión de barcos, clientes y reservas.

### HU-14 — Panel de administración de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede consultar clientes desde el panel de administración.
- El administrador puede eliminar clientes desde el panel de administración.
- El administrador no puede eliminar un usuario cliente si ese usuario tiene reservas pendientes.
- Se muestra un mensaje de error si se intenta eliminar un cliente con reservas pendientes.

### HU-15 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración mediante botones por transición aplicable.

**Criterios de aceptación**

- El administrador puede consultar el estado de cualquier reserva.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas mediante botones por transición aplicable.
- El administrador puede consultar y cambiar el estado de reservas desde el panel de administración.
- Solo se muestran transiciones válidas según el estado actual de la reserva.

### HU-16 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español para que la aplicación funcione correctamente en el contexto regional.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- La interfaz de usuario está íntegramente en español.
- Los nombres de variables, clases, funciones y rutas están en inglés; comentarios y docstrings en español.

### HU-17 — Datos precargados y Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero arrancar con datos precargados y estar empaquetado en Docker para facilitar el despliegue y las pruebas.

**Criterios de aceptación**

- La aplicación arranca con datos precargados: mínimo 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (incluyendo velero), 1 usuario administrador de prueba y 1 usuario cliente de prueba.
- La aplicación se entrega como contenedor Docker con Dockerfile incluido.
- Se incluyen instrucciones de construcción y arranque en README.
- La aplicación está desarrollada en Python usando Django 3.2.
- La aplicación utiliza SQLite como base de datos.
