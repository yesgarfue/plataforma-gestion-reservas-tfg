---
run_id: run_2026-05-17_18-49
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-17T19:09:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-17_18-49`

Total de historias: **22**

## Historias

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme mediante correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Las contraseñas se almacenan usando el mecanismo estándar de Django, no en texto plano.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Se validan todos los formularios y está activa la protección CSRF.

### HU-02 — Inicio de sesión de cliente

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo electrónico y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- Se valida el formulario y está activa la protección CSRF.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para terminar mi sesión de forma segura.

**Criterios de aceptación**

- El cliente puede acceder a una opción de cerrar sesión desde cualquier página.
- Al cerrar sesión, la sesión se termina y el cliente es redirigido a la página principal.
- Tras cerrar sesión, el cliente no puede acceder a funcionalidades autenticadas sin volver a iniciar sesión.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos se organizan por categorías.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- La interfaz está íntegramente en español.

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título desde la página de inicio, para encontrar rápidamente el barco que me interesa.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de búsqueda.
- La búsqueda filtra los barcos por nombre o título coincidentes.
- Los resultados se actualizan dinámicamente o tras enviar el formulario.

### HU-06 — Filtros combinables de catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero aplicar filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma simultánea e independiente, para refinar mi búsqueda.

**Criterios de aceptación**

- El cliente puede filtrar por puerto mediante un desplegable con valores válidos.
- El cliente puede filtrar por fabricante mediante un desplegable con valores válidos.
- El cliente puede filtrar por rango de precio.
- El cliente puede filtrar por categoría.
- El cliente puede filtrar por capacidad.
- El cliente puede filtrar por rango de fechas.
- Los filtros se aplican de forma combinada e independiente.
- Al filtrar por fechas, se muestran todos los barcos del catálogo, marcando con una etiqueta 'No disponible' los que no están disponibles en ese rango sin ocultarlos.

### HU-07 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha del barco desde el catálogo, visualizar sus datos e imagen, y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede hacer clic en un barco del catálogo para acceder a su ficha.
- La ficha muestra todos los datos del barco y su imagen.
- El cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta desde la ficha.
- Se valida que la cantidad seleccionada no exceda la disponibilidad.

### HU-08 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página, poder ampliar o reducir la cantidad de unidades de cada barco, revisar su estado y vaciarlo si es necesario.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta.
- Al entrar en modo administrador, la cesta se vacía automáticamente.

### HU-09 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva sin haberme registrado previamente, proporcionando mis datos durante el proceso en no más de tres pasos.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta sin estar registrado.
- El proceso de reserva se realiza en no más de tres pasos.
- Durante el proceso se solicitan los datos del cliente (nombre, correo, teléfono, etc.) y datos de pago.
- El cliente puede completar la reserva sin registro previo.
- Si el cliente inicia sesión durante el proceso de reserva, sus datos se heredan al volver de la página de login.

### HU-10 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero poder pagar mi reserva mediante PayPal Sandbox o contra-reembolso, para elegir el método que prefiero.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- La integración de PayPal utiliza el entorno Sandbox, no producción.
- El cliente es redirigido al flujo de pago correspondiente según el método seleccionado.

### HU-11 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico de confirmación con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico de confirmación.
- El correo contiene los datos del barco, el rango de fechas, el importe total y un código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-12 — Cálculo de tarifa con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el importe total de la reserva considerando el precio diario del barco, la cantidad de días y una tasa de combustible, para mostrar el precio correcto al cliente.

**Criterios de aceptación**

- Los alquileres se miden por día.
- Se aplica una tasa de combustible de 50 euros por día para todos los barcos.
- Para barcos de categoría velero, la tasa de combustible es 0 euros.
- El importe total se calcula correctamente: (precio_diario * cantidad_dias * cantidad_barcos) + (tasa_combustible * cantidad_dias * cantidad_barcos).
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-13 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas para reflejar su ciclo de vida, permitiendo transiciones válidas entre estados.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO, implicando su eliminación del sistema.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas mediante botones por transición aplicable.
- Las transiciones de estado respetan las reglas de negocio.

### HU-14 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con fecha de inicio en el próximo día.
- Se envía un correo de recordatorio al cliente con los datos de la reserva.
- El correo incluye un enlace o código para completar el pago o consultar el estado.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, incluso si no estoy registrado.

**Criterios de aceptación**

- El cliente puede acceder a una página de consulta de reserva por código de seguimiento.
- Introduciendo el código de seguimiento, se muestra el estado actual de la reserva.
- Se muestran los datos de la reserva: barco, fechas, importe, estado.
- No se requiere estar registrado para consultar la reserva.

### HU-16 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a una sección de mis reservas.
- Se muestran todas las reservas del cliente con su estado actual.
- Se muestran los datos de cada reserva: barco, fechas, importe, estado.
- El cliente puede acceder a la ficha de cada reserva para más detalles.

### HU-17 — Panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero acceder a un panel de administración propio de la aplicación para gestionar barcos, clientes y reservas.

**Criterios de aceptación**

- Existe un panel de administración accesible solo para administradores.
- El panel proporciona acceso a la gestión de barcos, clientes y reservas.
- El panel está íntegramente en español.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-18 — Gestión de barcos en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero realizar alta, edición y baja de barcos desde el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede crear un nuevo barco con todos sus datos (nombre, imagen, categoría, fabricante, puerto, capacidad, precio por día).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- Los cambios se reflejan inmediatamente en el catálogo visible para los clientes.
- Existe una ficha de barco propia del administrador con acciones de gestión: alta, edición y baja.

### HU-19 — Gestión de clientes en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes registrados.
- El administrador puede ver los datos de cada cliente.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si un cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- Se valida la restricción antes de permitir la eliminación.

### HU-20 — Gestión de reservas en panel de administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de reservas desde el panel de administración, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas.
- El administrador puede filtrar reservas por estado, cliente, barco o rango de fechas.
- El administrador puede ver los datos completos de cada reserva.
- El administrador puede cambiar el estado de una reserva mediante botones por transición aplicable.
- Los cambios de estado se registran y se reflejan inmediatamente.

### HU-21 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español para que todas las fechas y textos se muestren correctamente.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- Todas las fechas se muestran en la zona horaria Europe/Madrid.
- La interfaz de usuario está íntegramente en español.
- Los nombres de variables, clases, funciones y rutas están en inglés; comentarios y docstrings en español.

### HU-22 — Datos precargados de ejemplo

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
