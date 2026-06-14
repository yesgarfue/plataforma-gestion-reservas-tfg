---
run_id: run_2026-05-12_13-29
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T13:52:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-12_13-29`

Total de historias: **25**

## Historias

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Las contraseñas se almacenan de forma segura, no en texto plano.
- Tras registrarse, el cliente queda autenticado en la sesión.
- El sistema valida que el correo no esté ya registrado.

### HU-02 — Inicio de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error sin revelar qué campo es incorrecto.
- La sesión se mantiene activa durante la navegación.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para asegurar que mi cuenta no permanece abierta en dispositivos compartidos.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón 'Cerrar sesión' desde cualquier página.
- Al cerrar sesión, la cesta se mantiene pero el cliente queda desautenticado.
- Tras cerrar sesión, el cliente es redirigido a la página principal.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos.
- Los barcos están organizados por categorías.
- Cada barco muestra nombre, imagen obligatoria, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos agotados o no disponibles están claramente marcados.

### HU-05 — Búsqueda y filtros combinables de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar barcos por nombre y aplicar filtros combinables, para encontrar rápidamente el barco que necesito.

**Criterios de aceptación**

- La búsqueda está disponible en la página de inicio.
- La búsqueda acepta búsquedas por nombre o título del barco.
- Se pueden aplicar filtros combinables (puerto, fabricante, categoría, capacidad, precio, fechas).
- Los resultados se actualizan al aplicar o cambiar filtros.
- La búsqueda devuelve resultados relevantes o un mensaje si no hay coincidencias.

### HU-06 — Selección de cantidad y adición a cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero seleccionar la cantidad de unidades de un barco desde su ficha y añadirlo a la cesta, para preparar mi reserva.

**Criterios de aceptación**

- La ficha del barco permite seleccionar una cantidad de unidades.
- El cliente puede añadir el barco a la cesta desde la ficha.
- La cesta se actualiza inmediatamente tras añadir el barco.
- Se valida que la cantidad sea mayor a cero.

### HU-07 — Visibilidad permanente de la cesta

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página de la aplicación, para saber en todo momento qué he añadido.

**Criterios de aceptación**

- La cesta es visible en todas las páginas de la aplicación.
- La cesta muestra el número de unidades totales.
- La cesta muestra el importe total.
- El cliente puede acceder a la cesta desde cualquier página.

### HU-08 — Modificación de la cesta

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente, quiero aumentar o reducir la cantidad de unidades de cada barco en la cesta, para ajustar mi reserva antes de pagar.

**Criterios de aceptación**

- El cliente puede aumentar la cantidad de un barco en la cesta.
- El cliente puede reducir la cantidad de un barco en la cesta.
- El cliente puede eliminar completamente un barco de la cesta.
- El importe total se recalcula automáticamente tras cada cambio.
- La cesta se vacía si el cliente entra en modo administrador.

### HU-09 — Proceso de reserva en tres pasos sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como visitante, quiero completar una compra en un proceso de tres pasos sin necesidad de registrarme previamente, para realizar una reserva rápidamente.

**Criterios de aceptación**

- El proceso de reserva consta de tres pasos claramente definidos.
- El cliente puede completar la reserva sin estar registrado.
- Los datos del cliente se solicitan durante el proceso de reserva.
- La cesta se mantiene durante todo el proceso.
- Al finalizar, se genera un código de seguimiento.

### HU-10 — Métodos de pago: PayPal Sandbox y contra-reembolso

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago (PayPal Sandbox y contra-reembolso), para pagar de la forma que prefiero.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- La integración con PayPal Sandbox funciona correctamente en el entorno de pruebas.
- El flujo de contra-reembolso registra la reserva en estado PENDIENTE DE PAGO.
- Se valida que se haya seleccionado un método de pago antes de confirmar.

### HU-11 — Tasa de combustible y excepción para veleros

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que se aplique correctamente la tasa de combustible en mi reserva, con excepción para veleros, para entender el importe final.

**Criterios de aceptación**

- Se aplica una tasa de combustible de 50 € por día a todos los barcos.
- Los veleros no tienen tasa de combustible.
- La tasa se calcula correctamente en función del rango de fechas de la reserva.
- El importe total incluye la tasa de combustible (excepto para veleros).
- El cliente ve desglosado el importe base y la tasa en el resumen de la reserva.

### HU-12 — Correo de confirmación con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi pedido.

**Criterios de aceptación**

- Se envía un correo electrónico tras confirmar la reserva.
- El correo incluye los datos del barco reservado.
- El correo incluye el rango de fechas de la reserva.
- El correo incluye el importe total.
- El correo incluye un código de seguimiento único.
- El código de seguimiento permite consultar el estado sin estar registrado.

### HU-13 — Cancelación de reserva en estado PENDIENTE DE PAGO

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva que está en estado PENDIENTE DE PAGO, para eliminarla del sistema si cambio de opinión.

**Criterios de aceptación**

- El cliente puede cancelar una reserva solo si está en estado PENDIENTE DE PAGO.
- Al cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado del cliente.
- Se muestra un mensaje de confirmación antes de eliminar.
- No se puede cancelar una reserva en otros estados.

### HU-14 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente no registrado, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por correo, para saber el progreso de mi pedido.

**Criterios de aceptación**

- Existe una página de consulta de estado accesible sin autenticación.
- El cliente introduce el código de seguimiento.
- El sistema devuelve el estado actual de la reserva.
- Se muestra el estado, los datos del barco, las fechas y el importe.
- Si el código no existe, se muestra un mensaje de error.

### HU-15 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta en el sistema, para seguimiento de mis pedidos.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- El listado muestra el estado de cada reserva.
- El listado muestra los datos del barco, fechas e importe de cada reserva.
- El cliente puede ver el código de seguimiento de cada reserva.
- El cliente puede cancelar una reserva si está en estado PENDIENTE DE PAGO.

### HU-16 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero consultar y cambiar el estado de cualquier reserva desde el panel de administración, para gestionar el ciclo de vida de los pedidos.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas.
- El administrador puede filtrar reservas por estado.
- El administrador puede cambiar el estado de una reserva para transiciones aplicables.
- El sistema valida que la transición de estado sea válida.
- Se registra quién y cuándo cambió el estado de una reserva.

### HU-17 — Gestión administrativa de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero crear, editar y eliminar barcos en el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede crear un nuevo barco con todos los campos requeridos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- Se valida que todos los campos obligatorios estén completos.
- Los cambios se reflejan inmediatamente en el catálogo.

### HU-18 — Gestión administrativa de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes desde el panel de administración, para mantener la base de datos de usuarios.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes.
- El administrador puede eliminar un cliente solo si no tiene reservas pendientes.
- Se valida que el cliente no tenga reservas antes de permitir la eliminación.
- Se muestra un mensaje de error si se intenta eliminar un cliente con reservas.
- Los datos del cliente se eliminan del sistema al confirmar.

### HU-19 — Inicio de sesión durante el proceso de reserva

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero iniciar sesión durante el proceso de reserva manteniendo la cesta, para no perder mis selecciones.

**Criterios de aceptación**

- El cliente puede acceder a un formulario de login durante el proceso de reserva.
- La cesta se mantiene tras iniciar sesión.
- El cliente queda autenticado y puede continuar con la reserva.
- Los datos de la cesta se asocian a la cuenta del cliente.

### HU-20 — Reserva sin registro previo

- **Prioridad**: Baja
- **Estimación**: S

**Descripción**

Como visitante, quiero realizar una reserva sin estar registrado previamente, para acceder rápidamente al servicio.

**Criterios de aceptación**

- El visitante puede completar una reserva sin tener una cuenta.
- Se solicitan los datos de contacto durante el proceso de reserva.
- Se genera un código de seguimiento para consultar el estado.
- El visitante recibe un correo de confirmación con el código.
- El visitante puede consultar el estado usando el código sin registrarse.

### HU-21 — Recordatorio de reserva pendiente

- **Prioridad**: Baja
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo de recordatorio un día antes del inicio de mi reserva si aún está en estado PENDIENTE DE PAGO, para no olvidar completar el pago.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con inicio en el próximo día.
- Se envía un correo de recordatorio al cliente.
- El correo incluye los datos de la reserva y el código de seguimiento.
- El recordatorio se envía una sola vez por reserva.
- El sistema maneja correctamente las zonas horarias.

### HU-22 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador del sistema, quiero que la aplicación funcione bajo la zona horaria Europe/Madrid y locale español, para que las fechas y textos sean correctos para los usuarios.

**Criterios de aceptación**

- La zona horaria del sistema está configurada como Europe/Madrid.
- El locale está configurado como español.
- Las fechas se muestran en formato español.
- Los textos de la interfaz están en español.
- Los correos electrónicos se envían con la zona horaria correcta.

### HU-23 — Datos seed precargados

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero que la aplicación arranque con datos precargados, para poder demostrar la funcionalidad sin necesidad de crear datos manualmente.

**Criterios de aceptación**

- La aplicación carga 5 barcos al iniciar.
- La aplicación carga 2 puertos al iniciar.
- La aplicación carga 2 fabricantes al iniciar.
- La aplicación carga 2 categorías al iniciar.
- La aplicación carga 1 usuario administrador al iniciar.
- La aplicación carga 1 cliente de prueba al iniciar.
- Los datos se cargan de forma fiable en cada arranque.

### HU-24 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación sea entregada como contenedor Docker, para facilitar el despliegue y la ejecución en diferentes entornos.

**Criterios de aceptación**

- Existe un Dockerfile que construye la imagen de la aplicación.
- El Dockerfile incluye todas las dependencias necesarias.
- Existe un README con instrucciones de construcción del contenedor.
- Existe un README con instrucciones de arranque del contenedor.
- El contenedor arranca correctamente y la aplicación es accesible.

### HU-25 — Seguridad: contraseñas, CSRF y validación

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador de seguridad, quiero que la aplicación implemente medidas de seguridad mínima, para proteger los datos de los usuarios.

**Criterios de aceptación**

- Las contraseñas no se almacenan en texto plano.
- La protección CSRF está activa en todos los formularios.
- Se validan todos los formularios en el servidor.
- Se validan los datos de entrada para prevenir inyecciones.
- Los errores no revelan información sensible al usuario.
