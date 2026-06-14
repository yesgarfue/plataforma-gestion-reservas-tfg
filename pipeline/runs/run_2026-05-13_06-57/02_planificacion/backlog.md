---
run_id: run_2026-05-13_06-57
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-13T07:09:29+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-13_06-57`

Total de historias: **24**

## Historias

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Las contraseñas se almacenan de forma segura utilizando el mecanismo estándar de Django.

### HU-02 — Inicio de sesión de cliente

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- La protección CSRF está activada en el formulario.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para terminar mi sesión de forma segura.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón 'Cerrar sesión'.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se elimina del servidor.

### HU-04 — Reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero poder reservar un barco sin registrarme previamente, para agilizar el proceso de alquiler.

**Criterios de aceptación**

- El proceso de reserva permite continuar sin estar registrado.
- El cliente puede proporcionar sus datos de contacto durante el proceso de reserva.
- Si el cliente inicia sesión durante el proceso, la cesta se recupera y se continúa con el proceso.

### HU-05 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver el catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal presenta los barcos agrupados por categoría.
- Cada categoría es claramente identificable.
- Se muestran al menos 5 barcos predefinidos en el catálogo.

### HU-06 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente, quiero buscar barcos por nombre o título en la página de inicio, para encontrar rápidamente el barco que me interesa.

**Criterios de aceptación**

- Existe un campo de búsqueda en la página principal.
- La búsqueda filtra los barcos por nombre o título.
- Los resultados se actualizan en tiempo real o tras enviar el formulario.

### HU-07 — Filtros combinables de catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero filtrar el catálogo por puertos, fabricantes, precio, categoría, capacidad y rango de fechas, para encontrar el barco que se ajuste a mis necesidades.

**Criterios de aceptación**

- Los filtros de puertos y fabricante se presentan como desplegables con valores válidos.
- El cliente puede combinar múltiples filtros simultáneamente.
- Los barcos no disponibles en el rango de fechas seleccionado aparecen marcados con una etiqueta 'No disponible'.
- Los filtros se aplican correctamente al catálogo.

### HU-08 — Ficha de barco con selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha detallada de un barco e indicar la cantidad que deseo alquilar, para añadirlo a la cesta.

**Criterios de aceptación**

- La ficha del barco muestra todos los detalles relevantes (nombre, descripción, precio, categoría, capacidad, puerto, fabricante).
- El cliente puede seleccionar la cantidad de unidades a alquilar.
- El cliente puede añadir el barco a la cesta desde la ficha.

### HU-09 — Cesta visible e interactiva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible e interactiva desde cualquier página de la aplicación, para gestionar mis selecciones fácilmente.

**Criterios de aceptación**

- La cesta es visible en todas las páginas de la aplicación.
- El cliente puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El cliente puede vaciar la cesta completamente.
- La cesta del administrador se vacía automáticamente al entrar como admin y no permite añadir productos.

### HU-10 — Proceso de reserva en tres pasos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar el proceso de reserva en tres pasos sin exigir registro previo, para alquilar un barco de forma rápida.

**Criterios de aceptación**

- El proceso de reserva consta de tres pasos claramente definidos.
- El cliente puede completar la reserva sin estar registrado.
- Los datos de la reserva se validan correctamente en cada paso.
- El cliente puede navegar entre pasos o cancelar el proceso.

### HU-11 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago (PayPal Sandbox y contra-reembolso) para completar mi reserva.

**Criterios de aceptación**

- Se presentan dos opciones de pago: PayPal Sandbox y contra-reembolso.
- El cliente puede seleccionar uno de los métodos.
- El flujo de pago se adapta según el método seleccionado.
- El pago se procesa correctamente en ambos casos.

### HU-12 — Cálculo de tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en el cálculo del alquiler, excepto para los barcos en la categoría 'velero'.

**Criterios de aceptación**

- La tasa de combustible se calcula como 50 € por día.
- Los barcos en la categoría 'velero' no incluyen tasa de combustible.
- El total del alquiler incluye la tasa de combustible calculada correctamente.
- El cliente ve el desglose de costos en el resumen de la reserva.

### HU-13 — Confirmación de reserva por correo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva, incluyendo el código de seguimiento, para tener constancia de mi alquiler.

**Criterios de aceptación**

- Se envía un correo electrónico tras completar la reserva.
- El correo incluye los datos del barco, el rango de fechas y la información total del alquiler.
- El correo incluye el código de seguimiento único.
- El correo se envía a la dirección de correo proporcionada por el cliente.

### HU-14 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO) para controlar el ciclo de vida de cada alquiler.

**Criterios de aceptación**

- Las reservas tienen cuatro estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El estado se actualiza correctamente según el flujo de la reserva.
- El administrador puede cambiar el estado de una reserva desde el panel.

### HU-15 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar mi reserva si está en estado PENDIENTE DE PAGO, para desistir del alquiler si es necesario.

**Criterios de aceptación**

- El cliente puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO.
- Tras cancelar, la reserva se elimina del sistema.
- Se envía un correo de confirmación de cancelación al cliente.
- Las reservas en otros estados no pueden ser canceladas.

### HU-16 — Recordatorio de reserva por correo

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente un día antes de la fecha de inicio de la reserva, para que no olvide su alquiler.

**Criterios de aceptación**

- Se envía un correo de recordatorio un día antes de la fecha de inicio.
- El recordatorio se envía solo si la reserva está en estado PENDIENTE DE PAGO.
- El correo incluye los detalles de la reserva y el código de seguimiento.
- El sistema registra el envío del recordatorio.

### HU-17 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por correo, para verificar el estado de mi alquiler sin necesidad de registrarme.

**Criterios de aceptación**

- Existe una página de consulta de reserva por código de seguimiento.
- El cliente introduce el código de seguimiento.
- Se muestra el estado actual de la reserva.
- Se muestran los detalles de la reserva (barco, fechas, total).

### HU-18 — Consulta de reservas del cliente registrado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta personal, para seguimiento de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- Se muestran todas las reservas del cliente con sus estados.
- Se muestran los detalles de cada reserva (barco, fechas, estado, total).
- El cliente puede filtrar por estado si lo desea.

### HU-19 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de cualquier reserva en la aplicación, para gestionar el ciclo de vida de los alquileres.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- Se muestran los detalles de cada reserva (cliente, barco, fechas, estado, total).
- El administrador puede cambiar el estado de una reserva.
- El administrador puede filtrar las reservas por estado, cliente o barco.

### HU-20 — Gestión administrativa de barcos

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar el catálogo de barcos (crear, editar, eliminar), para mantener la información actualizada.

**Criterios de aceptación**

- El administrador puede crear nuevos barcos con todos los atributos (nombre, descripción, precio, categoría, capacidad, puerto, fabricante).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- El sistema valida que los datos sean correctos antes de guardar.

### HU-21 — Gestión administrativa de clientes

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los clientes registrados, incluyendo la eliminación de usuarios sin reservas pendientes.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes registrados.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Se muestra un mensaje de error si se intenta eliminar un cliente con reservas pendientes.
- El administrador puede ver los detalles de cada cliente.

### HU-22 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero operar bajo la zona horaria 'Europe/Madrid' y presentar la interfaz íntegramente en español, para garantizar consistencia regional.

**Criterios de aceptación**

- La zona horaria del sistema está configurada como 'Europe/Madrid'.
- Todos los textos de la interfaz están en español.
- Las fechas y horas se muestran en formato español.
- Los mensajes de error y validación están en español.

### HU-23 — Empaquetado Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como equipo de desarrollo, quiero que la aplicación se empaquete y ejecute como contenedor Docker, para facilitar el despliegue y la consistencia del entorno.

**Criterios de aceptación**

- Existe un Dockerfile que define la imagen de la aplicación.
- La aplicación se ejecuta correctamente dentro del contenedor Docker.
- El contenedor incluye todas las dependencias necesarias (Python, Django, SQLite).
- El contenedor se puede construir y ejecutar sin errores.

### HU-24 — Datos seed iniciales

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero arrancar con datos predefinidos (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, 1 usuario administrador y cliente), para que la aplicación sea funcional desde el inicio.

**Criterios de aceptación**

- La aplicación carga automáticamente 5 barcos al arrancar.
- Se crean 2 puertos predefinidos.
- Se crean 2 fabricantes predefinidos.
- Se crean 2 categorías predefinidas.
- Se crea 1 usuario administrador con credenciales de prueba.
- Se crea 1 usuario cliente con credenciales de prueba.
- Los datos seed se cargan de forma fiable en cada arranque.
