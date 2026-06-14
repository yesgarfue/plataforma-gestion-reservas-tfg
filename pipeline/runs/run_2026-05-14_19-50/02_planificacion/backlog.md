---
run_id: run_2026-05-14_19-50
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T20:09:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-14_19-50`

Total de historias: **21**

## Historias

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Las contraseñas se almacenan usando el mecanismo estándar de Django, no en texto plano.

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

- El cliente puede pulsar un botón de cierre de sesión desde cualquier página.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se elimina del servidor.

### HU-04 — Catálogo de barcos con búsqueda y filtros

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero visualizar un catálogo de barcos organizado por categorías y buscar o filtrar por nombre, puerto, fabricante, precio, capacidad y rango de fechas, para encontrar el barco que necesito.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El sistema permite búsqueda por nombre o título desde la página de inicio.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El sistema permite filtrar por puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma combinable e independiente.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.

### HU-05 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha de un barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede acceder a la ficha del barco desde el catálogo.
- La ficha visualiza los datos del barco e imagen.
- El cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta desde la ficha.

### HU-06 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero visualizar, modificar y vaciar mi cesta desde cualquier página de la aplicación, para gestionar mis barcos antes de finalizar la compra.

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

Como cliente, quiero completar una reserva en no más de tres pasos sin haberse registrado previamente, proporcionando datos de cliente y pago.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta.
- El proceso de reserva se realiza en no más de tres pasos.
- No se exige registro previo para completar una reserva.
- Durante el proceso se solicitan los datos del cliente y datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.

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

Como cliente, quiero recibir un correo electrónico de confirmación con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-10 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en todas las reservas, excepto para barcos de categoría velero donde la tasa es 0 €.

**Criterios de aceptación**

- El sistema calcula la tasa de combustible como 50 € por día para barcos que no son velero.
- El sistema aplica tasa de combustible de 0 € para barcos de categoría velero.
- La tasa se incluye en el importe total de la reserva.
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-11 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero gestionar los estados de las reservas: PENDIENTE DE PAGO, PAGADO, EN USO y DEVUELTO.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El estado se actualiza según las transiciones aplicables.

### HU-12 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para eliminarla del sistema sin dejar registro posterior.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema sin dejar registro posterior.
- El cliente recibe una confirmación de cancelación.
- Las reservas en otros estados no pueden cancelarse.

### HU-13 — Recordatorio de reserva pendiente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con fecha de inicio en el próximo día.
- El sistema envía un correo de recordatorio al cliente.
- El correo contiene los datos de la reserva y un enlace para completar el pago.

### HU-14 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- El sistema busca la reserva por código de seguimiento.
- Se muestra el estado actual de la reserva.
- No se requiere autenticación para consultar por código de seguimiento.

### HU-15 — Consulta de reservas del cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- Se muestra el estado actual de cada reserva.
- Se muestran los datos del barco, rango de fechas e importe de cada reserva.
- El cliente puede acceder a los detalles de cada reserva.

### HU-16 — Panel de administración de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar barcos desde el panel de administración: dar de alta, editar y dar de baja.

**Criterios de aceptación**

- El administrador accede a un panel de administración propio.
- El administrador puede dar de alta nuevos barcos con todos los campos requeridos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede dar de baja un barco.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-17 — Panel de administración de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede consultar un listado de todos los clientes.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si un cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede eliminarse.
- Se muestra información de contacto y reservas de cada cliente.

### HU-18 — Panel de administración de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración mediante botones por transición aplicable.

**Criterios de aceptación**

- El administrador puede consultar un listado de todas las reservas.
- El administrador puede ver el estado actual de cada reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Se muestran los datos del barco, cliente, rango de fechas e importe de cada reserva.
- Los cambios de estado se registran en el sistema.

### HU-19 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria a Europe/Madrid y el locale a español para que todas las fechas, horas y textos se muestren correctamente.

**Criterios de aceptación**

- La zona horaria del sistema está configurada a Europe/Madrid.
- El locale está configurado a español.
- Todas las fechas y horas se muestran en zona horaria Europe/Madrid.
- La interfaz de usuario está íntegramente en español.

### HU-20 — Datos precargados de ejemplo

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero que la aplicación arranque con datos precargados para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- Hay 2 puertos precargados.
- Hay 2 fabricantes precargados.
- Hay 2 categorías precargadas, incluyendo velero.
- Hay 1 usuario administrador de prueba precargado.
- Hay 1 usuario cliente de prueba precargado.
- Los datos se cargan de forma fiable en cada arranque.

### HU-21 — Seguridad y validación de formularios

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero garantizar la seguridad mediante almacenamiento seguro de contraseñas, protección CSRF y validación de todos los formularios.

**Criterios de aceptación**

- Las contraseñas se almacenan usando el mecanismo estándar de Django, no en texto plano.
- CSRF está activo en todos los formularios.
- Se validan todos los formularios antes de procesar datos.
- Los datos sensibles no se exponen en URLs o logs.
