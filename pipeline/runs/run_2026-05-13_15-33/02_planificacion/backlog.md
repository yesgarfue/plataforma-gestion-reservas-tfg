---
run_id: run_2026-05-13_15-33
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-13T15:47:23+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-13_15-33`

Total de historias: **26**

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
- Se valida que el correo no esté ya registrado.

### HU-02 — Inicio de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error genérico.
- La sesión se mantiene activa durante la navegación.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para asegurar que mi cuenta no queda accesible desde el dispositivo.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón 'Cerrar sesión'.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se invalida y el cliente no puede acceder a funcionalidades autenticadas sin volver a iniciar sesión.

### HU-04 — Eliminación de cliente por administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero eliminar un cliente si no tiene reservas pendientes, para mantener la base de datos limpia.

**Criterios de aceptación**

- El administrador puede acceder a un listado de clientes desde el panel de administración.
- El administrador puede eliminar un cliente solo si no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- Tras la eliminación, el cliente desaparece del sistema.

### HU-05 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver el catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos.
- Los barcos están organizados por categorías.
- Cada barco muestra: nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El catálogo es accesible sin necesidad de autenticación.

### HU-06 — Búsqueda y filtros combinables de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar y filtrar barcos por nombre, puertos, fabricantes, precio, categoría, capacidad y fechas, para encontrar la embarcación que se ajuste a mis necesidades.

**Criterios de aceptación**

- La búsqueda funciona por nombre o título del barco.
- Los filtros de puertos, fabricante y precio se presentan como desplegables.
- Los filtros de categoría y capacidad están disponibles.
- El filtro de fechas muestra todos los barcos del catálogo; los no disponibles en ese rango aparecen marcados con una etiqueta 'No disponible'.
- Los filtros son combinables entre sí.
- Los resultados se actualizan al aplicar o modificar filtros.

### HU-07 — Selección de cantidad y adición a cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero seleccionar la cantidad de unidades de un barco desde su ficha y añadirlo a la cesta, para preparar mi reserva.

**Criterios de aceptación**

- La ficha del barco muestra un campo para seleccionar cantidad.
- El cliente puede añadir el barco a la cesta con la cantidad seleccionada.
- Se muestra una confirmación de que el barco ha sido añadido a la cesta.
- La cantidad debe ser un número entero positivo.

### HU-08 — Cesta visible y modificable

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página y poder modificar las cantidades o vaciarla, para gestionar mis reservas antes de finalizar la compra.

**Criterios de aceptación**

- La cesta es visible desde cualquier página de la aplicación.
- El cliente puede ampliar y reducir la cantidad de unidades de cada barco en la cesta.
- El cliente puede revisar el estado de la cesta desde el catálogo.
- El cliente puede vaciar la cesta completamente.
- Se muestra el total de la cesta actualizado en tiempo real.

### HU-09 — Vaciado de cesta al entrar como administrador

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador, quiero que la cesta se vacíe al cambiar a modo administrador y no poder añadir barcos al carro, para evitar confusiones entre roles.

**Criterios de aceptación**

- Al cambiar a modo administrador, la cesta se vacía automáticamente.
- El administrador no puede añadir barcos a la cesta.
- Se muestra un mensaje indicando que el modo administrador no permite usar la cesta.

### HU-10 — Proceso de reserva en tres pasos sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin necesidad de estar registrado previamente, para agilizar el proceso de compra.

**Criterios de aceptación**

- El proceso de reserva consta de máximo tres pasos.
- El registro previo no es obligatorio para realizar una reserva.
- Se solicitan los datos del cliente (nombre, correo, teléfono) durante el proceso.
- Se solicitan los datos de pago durante el proceso.
- El cliente puede completar la reserva sin haber creado una cuenta.

### HU-11 — Métodos de pago: PayPal Sandbox y contra-reembolso

- **Prioridad**: Media
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago (PayPal Sandbox y contra-reembolso) para completar mi reserva.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- La integración con PayPal Sandbox permite procesar pagos en línea.
- El método contra-reembolso registra la reserva sin procesar pago inmediato.

### HU-12 — Correo de confirmación con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico tras finalizar la reserva con los datos del barco, rango de fechas, importe total y código de seguimiento, para tener constancia de mi reserva.

**Criterios de aceptación**

- Al finalizar la reserva, se envía un correo electrónico al cliente.
- El correo incluye los datos del barco reservado.
- El correo incluye el rango de fechas de la reserva.
- El correo incluye el importe total.
- El correo incluye un código de seguimiento único.
- El código de seguimiento permite consultar el estado de la reserva.

### HU-13 — Tasa de combustible por día

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día a cada reserva, excepto si el barco es de categoría 'velero', para reflejar los costos operativos.

**Criterios de aceptación**

- Se aplica una tasa de combustible de 50 € por día a la reserva.
- La tasa de combustible no se aplica si el barco es de categoría 'velero'.
- El importe total de la reserva incluye la tasa de combustible calculada correctamente.
- El cliente ve el desglose de costos (precio del barco + tasa de combustible) antes de confirmar.

### HU-14 — Estados de reserva y transiciones

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO) para controlar el ciclo de vida de cada reserva.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Una reserva comienza en estado PENDIENTE DE PAGO.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas.
- Las transiciones de estado se registran en el sistema.

### HU-15 — Cancelación de reserva en estado PENDIENTE DE PAGO

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO, para poder desistir antes de realizar el pago.

**Criterios de aceptación**

- El cliente puede cancelar una reserva solo si está en estado PENDIENTE DE PAGO.
- Si la reserva está en otro estado, no aparece la opción de cancelación.
- Al cancelar, la reserva se elimina del sistema.
- Se muestra un mensaje de confirmación antes de cancelar.

### HU-16 — Correo de recordatorio de pago pendiente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para evitar que olvide completar el pago.

**Criterios de aceptación**

- El sistema identifica reservas en estado PENDIENTE DE PAGO con inicio en 24 horas.
- Se envía un correo de recordatorio al cliente.
- El correo incluye los datos de la reserva y un enlace para completar el pago.
- El recordatorio se envía una sola vez por reserva.

### HU-17 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento, para verificar el progreso sin necesidad de estar registrado.

**Criterios de aceptación**

- El cliente puede ingresar un código de seguimiento en un formulario de búsqueda.
- El sistema muestra el estado actual de la reserva.
- Se muestran los datos de la reserva (barco, fechas, importe).
- La búsqueda es accesible sin autenticación.

### HU-18 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta, para tener un historial de mis alquileres.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- Se muestra el estado de cada reserva.
- Se muestran los datos de cada reserva (barco, fechas, importe).
- El cliente puede filtrar por estado de reserva.

### HU-19 — Consulta de reservas por administrador

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar el estado de cualquier reserva en el sistema, para supervisar todas las transacciones.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- Se muestra el estado de cada reserva.
- Se muestran los datos de cada reserva (cliente, barco, fechas, importe).
- El administrador puede filtrar por estado, cliente o barco.

### HU-20 — Panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero acceder a un panel de administración propio de la aplicación, para gestionar barcos, clientes y reservas.

**Criterios de aceptación**

- Existe un panel de administración accesible solo para administradores.
- El panel proporciona acceso a la gestión de barcos.
- El panel proporciona acceso a la gestión de clientes.
- El panel proporciona acceso a la gestión de reservas.
- El panel muestra estadísticas o resúmenes del sistema.

### HU-21 — Gestión de barcos (alta, edición, baja)

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero crear, editar y eliminar barcos en el sistema, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede crear un nuevo barco con todos sus campos (nombre, imagen, categoría, fabricante, puerto, capacidad, precio).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- Se valida que los datos del barco sean correctos antes de guardar.
- Se muestra un mensaje de confirmación tras cada operación.

### HU-22 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero operar con zona horaria Europe/Madrid y locale español, para que todas las fechas, horas y textos se muestren correctamente.

**Criterios de aceptación**

- La aplicación está configurada con zona horaria Europe/Madrid.
- La aplicación utiliza locale español.
- Las fechas y horas se muestran en formato español.
- Los textos de la interfaz están en español.

### HU-23 — Datos seed precargados

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como desarrollador, quiero que la aplicación arranque con datos precargados que permitan probar todas las funcionalidades sin trabajo previo, para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación incluye un conjunto de barcos de ejemplo en diferentes categorías.
- La aplicación incluye clientes de ejemplo.
- La aplicación incluye reservas de ejemplo en diferentes estados.
- Los datos seed se cargan automáticamente al iniciar la aplicación.
- Los datos seed permiten probar todos los filtros y funcionalidades.

### HU-24 — Seguridad: contraseñas, CSRF y validación

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero implementar medidas de seguridad mínima para proteger los datos de los usuarios.

**Criterios de aceptación**

- Las contraseñas no se almacenan en texto plano.
- La protección CSRF está activa en todos los formularios.
- Se validan todos los formularios en el servidor.
- Se validan los datos de entrada para prevenir inyecciones.
- Los errores de validación se muestran al usuario sin revelar información sensible.

### HU-25 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación esté empaquetada como contenedor Docker con instrucciones claras de construcción y arranque, para facilitar el despliegue.

**Criterios de aceptación**

- Existe un Dockerfile que define la construcción de la imagen.
- Existe un README con instrucciones de construcción del contenedor.
- Existe un README con instrucciones de arranque del contenedor.
- El contenedor incluye todas las dependencias necesarias.
- La aplicación funciona correctamente al ejecutarse desde el contenedor.

### HU-26 — Inicio de sesión durante el proceso de reserva

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente, quiero poder iniciar sesión durante el proceso de reserva, para acceder a mis datos guardados sin completar el registro.

**Criterios de aceptación**

- Durante el proceso de reserva, se ofrece la opción de iniciar sesión.
- El cliente puede ingresar sus credenciales sin abandonar el flujo de reserva.
- Tras iniciar sesión, los datos del cliente se cargan automáticamente.
- El cliente puede continuar con la reserva sin necesidad de completar el registro.
