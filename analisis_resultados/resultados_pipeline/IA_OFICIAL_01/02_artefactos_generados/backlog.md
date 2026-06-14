---
run_id: run_2026-05-18_15-09
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-18T15:29:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-18_15-09`

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
- La interfaz está íntegramente en español.

### HU-05 — Búsqueda y filtrado de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar barcos por nombre y filtrar por puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma combinable, para encontrar el barco que necesito.

**Criterios de aceptación**

- El sistema permite buscar barcos por nombre o título desde la página de inicio.
- El sistema permite filtrar barcos por puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma combinable e independiente.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con una etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.
- Los barcos no disponibles en el rango de fechas seleccionado aparecen claramente marcados.

### HU-06 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha del barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede acceder a la ficha del barco desde el catálogo.
- La ficha visualiza los datos del barco e imagen.
- Desde la ficha de barco, el cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco seleccionado a la cesta.
- Si el barco está agotado, no se permite añadir a la cesta.

### HU-07 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la cesta siempre visible, modificar cantidades y revisar su estado desde el catálogo, para gestionar mis compras.

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

Como cliente, quiero completar una reserva en no más de tres pasos sin haberse registrado previamente, para alquilar un barco de forma rápida.

**Criterios de aceptación**

- El cliente puede completar una reserva sin haberse registrado previamente.
- El proceso de reserva se realiza en no más de tres pasos.
- Durante el proceso de reserva se solicitan los datos del cliente y los datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.

### HU-09 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como métodos de pago durante la reserva.

**Criterios de aceptación**

- El sistema ofrece PayPal Sandbox como método de pago.
- El sistema ofrece contra-reembolso como método de pago.
- El cliente puede seleccionar uno de los dos métodos durante el proceso de reserva.
- La integración de PayPal utiliza el entorno Sandbox, no producción.

### HU-10 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para confirmar y rastrear mi alquiler.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico con los datos del barco, rango de fechas, importe total y código de seguimiento.
- El correo incluye el código de seguimiento único para consultar el estado de la reserva.
- El correo está redactado en español.

### HU-11 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible diferenciada según la categoría del barco, para calcular correctamente el importe total de la reserva.

**Criterios de aceptación**

- El sistema aplica una tasa de combustible de 50 € por día para barcos que no sean veleros.
- El sistema aplica una tasa de combustible de 0 € por día para barcos de categoría velero.
- La tasa se incluye en el cálculo del importe total de la reserva.
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-12 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero gestionar los estados de las reservas para reflejar su ciclo de vida.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El estado se actualiza según las transiciones aplicables del ciclo de vida.

### HU-13 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está pendiente de pago, para anular mi alquiler.

**Criterios de aceptación**

- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- El cliente recibe una confirmación de cancelación.

### HU-14 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue pendiente de pago.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario.
- El correo incluye los datos de la reserva y un enlace para completar el pago.
- El correo está redactado en español.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.

**Criterios de aceptación**

- El cliente puede consultar el estado de su reserva usando el código de seguimiento.
- No es necesario estar registrado para consultar por código de seguimiento.
- Se muestra el estado actual de la reserva, datos del barco y rango de fechas.
- Si el código no existe, se muestra un mensaje de error.

### HU-16 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta.

**Criterios de aceptación**

- El usuario registrado puede consultar el estado de sus reservas desde su cuenta.
- Se muestra una lista de todas las reservas del cliente con sus estados.
- Se puede acceder a los detalles de cada reserva.
- Se muestra el código de seguimiento de cada reserva.

### HU-17 — Gestión administrativa de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los barcos del catálogo mediante alta, edición y baja.

**Criterios de aceptación**

- El administrador dispone de una ficha de barco propia con acciones de gestión.
- El administrador puede crear un nuevo barco (alta).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco (baja).
- Al eliminar un barco, se valida que no tenga reservas activas.

### HU-18 — Gestión administrativa de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes con la restricción de que no tengan reservas pendientes.

**Criterios de aceptación**

- El panel de administración permite la consulta de clientes.
- El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- Se muestra una lista de clientes con sus datos principales.

### HU-19 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de las reservas desde el panel de administración.

**Criterios de aceptación**

- El panel de administración permite la consulta de todas las reservas.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Se muestra el estado actual y las transiciones disponibles para cada reserva.
- El administrador puede consultar los detalles completos de cualquier reserva.

### HU-20 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español para asegurar que las fechas y textos se muestren correctamente.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- Las fechas se muestran en formato español.
- Los textos del sistema están en español.

### HU-21 — Datos precargados de ejemplo

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero arrancar con datos precargados para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- Hay mínimo 2 puertos precargados.
- Hay mínimo 2 fabricantes precargados.
- Hay mínimo 2 categorías precargadas, incluyendo velero.
- Hay 1 usuario administrador de prueba precargado.
- Hay 1 usuario cliente de prueba precargado.
