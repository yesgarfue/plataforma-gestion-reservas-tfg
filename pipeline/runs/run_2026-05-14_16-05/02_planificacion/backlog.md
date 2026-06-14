---
run_id: run_2026-05-14_16-05
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T16:10:05+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-14_16-05`

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

### HU-04 — Catálogo de barcos con filtros combinables

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías y aplicar filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas, para encontrar el barco que necesito.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El cliente puede aplicar filtros de puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma simultánea e independiente.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con una etiqueta 'No disponible' los que no están disponibles en ese rango sin ocultarlos.

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título desde la página de inicio, para localizar rápidamente un barco específico.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de búsqueda.
- La búsqueda filtra los barcos del catálogo por nombre o título.
- Los resultados se actualizan en tiempo real o tras pulsar un botón de búsqueda.

### HU-06 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha del barco desde el catálogo, visualizar sus datos e imagen, y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede pulsar sobre un barco en el catálogo para acceder a su ficha.
- La ficha muestra todos los datos del barco: nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta desde la ficha.

### HU-07 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página, poder ampliar o reducir la cantidad de unidades de cada barco, revisar su estado y vaciarlo si es necesario.

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

Como cliente, quiero completar una reserva sin haberme registrado previamente, en no más de tres pasos, proporcionando mis datos y datos de pago.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta.
- El proceso de reserva se realiza en no más de tres pasos.
- No se exige registro previo para completar una reserva.
- Durante el proceso se solicitan los datos del cliente y los datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.

### HU-09 — Pago mediante PayPal Sandbox

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero pagar mi reserva mediante PayPal Sandbox, para utilizar mi cuenta de PayPal de prueba.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal como método de pago durante el proceso de reserva.
- El cliente es redirigido a PayPal Sandbox para completar el pago.
- Tras completar el pago en PayPal, el cliente es redirigido a la aplicación.
- La reserva se marca como PAGADO tras un pago exitoso en PayPal.

### HU-10 — Pago mediante contra-reembolso

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero pagar mi reserva mediante contra-reembolso, para pagar al recibir el barco.

**Criterios de aceptación**

- El cliente puede seleccionar contra-reembolso como método de pago durante el proceso de reserva.
- La reserva se marca como PENDIENTE DE PAGO tras seleccionar contra-reembolso.
- El cliente recibe un correo de confirmación con los datos de la reserva y el código de seguimiento.

### HU-11 — Confirmación de reserva con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico tras finalizar la reserva con los datos del barco, el rango de fechas, el importe total y un código de seguimiento.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco alquilado.
- El correo contiene el rango de fechas de la reserva.
- El correo contiene el importe total de la reserva.
- El correo contiene un código de seguimiento único para consultar el estado de la reserva.

### HU-12 — Cálculo de precio con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el precio total de la reserva considerando el precio diario del barco, el número de días y una tasa de combustible de 50 euros por día, excepto para barcos de categoría velero donde la tasa es 0 euros.

**Criterios de aceptación**

- El precio total se calcula como: (precio_diario + tasa_combustible) * número_de_días.
- La tasa de combustible es 50 euros por día para todas las categorías excepto velero.
- Para barcos de categoría velero, la tasa de combustible es 0 euros.
- El precio total se muestra al cliente antes de confirmar la reserva.

### HU-13 — Inicio de sesión durante el proceso de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero iniciar sesión durante el proceso de reserva y recuperar mi cesta al volver de la página de login, para continuar con mi compra sin perder los datos.

**Criterios de aceptación**

- El cliente puede acceder a un enlace de login durante el proceso de reserva.
- Tras iniciar sesión, el cliente es redirigido de vuelta al proceso de reserva.
- La cesta se mantiene intacta tras el login.
- Los datos del cliente se heredan automáticamente en el formulario de reserva.

### HU-14 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso si no estoy registrado.

**Criterios de aceptación**

- Existe una página pública para consultar el estado de una reserva por código de seguimiento.
- El cliente introduce el código de seguimiento en un formulario.
- El sistema muestra el estado actual de la reserva: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Se muestran los datos de la reserva: barco, rango de fechas e importe total.

### HU-15 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a una sección de mis reservas.
- Se muestra una lista de todas las reservas del cliente con su estado actual.
- Se muestran los datos de cada reserva: barco, rango de fechas, importe total y código de seguimiento.

### HU-16 — Cancelación de reserva pendiente de pago

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para eliminarla del sistema.

**Criterios de aceptación**

- El cliente puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- Se muestra un mensaje de confirmación antes de cancelar.

### HU-17 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con fecha de inicio en 24 horas.
- Se envía un correo de recordatorio al cliente con los datos de la reserva.
- El correo incluye un enlace para completar el pago o cancelar la reserva.

### HU-18 — Gestión de barcos en panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero gestionar barcos desde el panel de administración, realizando operaciones de alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a un panel de administración propio de la aplicación.
- El administrador puede crear un nuevo barco con todos sus datos: nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del sistema.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-19 — Gestión de clientes en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todos los clientes.
- El administrador puede ver los datos de cada cliente.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si un cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- La eliminación de un cliente se confirma antes de ejecutarse.

### HU-20 — Gestión de reservas en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración mediante botones por transición aplicable.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- Se muestra el estado actual de cada reserva: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El administrador puede cambiar el estado de una reserva mediante botones que representan transiciones válidas.
- Los cambios de estado se reflejan inmediatamente en el sistema.
- Se muestra un historial de cambios de estado para cada reserva.

### HU-21 — Ficha de barco para administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero acceder a una ficha de barco propia con acciones de gestión: alta, edición y baja.

**Criterios de aceptación**

- El administrador puede acceder a una ficha de barco desde el panel de administración.
- La ficha muestra todos los datos del barco.
- El administrador puede editar los datos del barco desde la ficha.
- El administrador puede eliminar el barco desde la ficha.
- El administrador puede crear un nuevo barco desde una ficha de alta.
