---
run_id: run_2026-05-15_11-00
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-15T11:04:48+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-15_11-00`

Total de historias: **23**

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

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para salir de mi cuenta de forma segura.

**Criterios de aceptación**

- El cliente puede pulsar un botón de cierre de sesión desde cualquier página.
- Tras cerrar sesión, el cliente es redirigido a la página principal sin autenticación.
- La sesión se elimina del servidor.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos se organizan por categorías.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título desde la página de inicio, para encontrar rápidamente el barco que me interesa.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de búsqueda.
- El catálogo se filtra mostrando solo los barcos cuyo nombre o título coincide con el término.
- Si no hay resultados, se muestra un mensaje indicando que no hay barcos disponibles.

### HU-06 — Filtros combinables de catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero aplicar filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma simultánea e independiente, para refinar mi búsqueda.

**Criterios de aceptación**

- El cliente puede seleccionar filtros de puerto, fabricante, categoría y capacidad desde desplegables con valores válidos.
- El cliente puede introducir un rango de precio mínimo y máximo.
- El cliente puede seleccionar un rango de fechas de disponibilidad.
- Los filtros se aplican de forma combinada y simultánea.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con una etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.

### HU-07 — Ficha de barco con selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha del barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta, para preparar mi reserva.

**Criterios de aceptación**

- El cliente puede pulsar sobre un barco en el catálogo para acceder a su ficha.
- La ficha muestra los datos completos del barco e imagen.
- El cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta con la cantidad seleccionada.
- Tras añadir a la cesta, se muestra un mensaje de confirmación.

### HU-08 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero visualizar, modificar y vaciar mi cesta desde cualquier página de la aplicación, para gestionar mis selecciones antes de reservar.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede eliminar un barco de la cesta.
- El usuario puede vaciar completamente la cesta.
- Al entrar en modo administrador, la cesta se vacía automáticamente.

### HU-09 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva sin haberme registrado previamente, para alquilar un barco de forma rápida.

**Criterios de aceptación**

- El proceso de reserva se realiza en no más de tres pasos.
- No se exige registro previo para completar la reserva.
- Durante el proceso se solicitan los datos del cliente (nombre, correo, teléfono) y los datos de pago.
- Si el cliente tiene sesión iniciada, los datos se heredan automáticamente.
- El cliente puede modificar los datos heredados si es necesario.

### HU-10 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero pagar mi reserva mediante PayPal Sandbox o contra-reembolso, para elegir el método que prefiero.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- Si elige PayPal, es redirigido al entorno Sandbox de PayPal.
- Si elige contra-reembolso, la reserva se crea en estado PENDIENTE DE PAGO.
- Tras completar el pago, se muestra un mensaje de confirmación.

### HU-11 — Confirmación de reserva con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi alquiler.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco, el rango de fechas, el importe total y un código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-12 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible a los alquileres, para cobrar el consumo estimado.

**Criterios de aceptación**

- Se aplica una tasa de combustible de 50 € por día a los alquileres.
- Para barcos de categoría velero, la tasa de combustible es 0 €.
- La tasa se calcula y suma al importe total de la reserva.
- El cliente ve el desglose de la tasa en el resumen de la reserva.

### HU-13 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas, para controlar el ciclo de vida de cada alquiler.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO o PAGADO según el método de pago.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas mediante botones por transición aplicable.
- El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email, incluso sin estar registrado.
- El usuario registrado puede consultar el estado de sus reservas desde su cuenta.

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

### HU-22 — Inicio de sesión durante el proceso de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero iniciar sesión durante el proceso de reserva y recuperar mi cesta al volver de la página de login, para continuar con mi reserva sin perder mis selecciones.

**Criterios de aceptación**

- Durante el proceso de reserva, el cliente puede pulsar un enlace para iniciar sesión.
- Es redirigido a la página de login.
- Tras iniciar sesión correctamente, es redirigido de vuelta al proceso de reserva.
- La cesta se recupera con los barcos que había seleccionado.
- Los datos del cliente se heredan automáticamente en el formulario de reserva.

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
