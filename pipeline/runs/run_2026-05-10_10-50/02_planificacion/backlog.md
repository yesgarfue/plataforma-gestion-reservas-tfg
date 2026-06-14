---
run_id: run_2026-05-10_10-50
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-10T10:59:24+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-10_10-50`

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

Como cliente autenticado, quiero cerrar sesión explícitamente, para asegurar que mi cuenta no queda accesible en dispositivos compartidos.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón 'Cerrar sesión' desde cualquier página.
- Tras cerrar sesión, el cliente es redirigido a la página de inicio.
- La sesión se elimina del servidor y el cliente no puede acceder a funcionalidades autenticadas.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías, para explorar las opciones disponibles.

**Criterios de aceptación**

- El catálogo muestra todos los barcos disponibles.
- Los barcos están agrupados por categoría.
- Cada barco muestra su nombre, categoría, precio y una imagen o descripción básica.
- El catálogo es accesible sin necesidad de autenticación.

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título, para encontrar rápidamente el barco que me interesa.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de texto.
- La búsqueda filtra los barcos por nombre o título de forma case-insensitive.
- Los resultados se actualizan en tiempo real o tras pulsar un botón de búsqueda.
- Si no hay resultados, se muestra un mensaje informativo.

### HU-06 — Filtros combinables en catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero aplicar filtros simultáneamente por puerto, fabricante, precio, categoría y capacidad, para refinar mi búsqueda de barcos.

**Criterios de aceptación**

- El cliente puede seleccionar filtros de puerto, fabricante, precio, categoría y capacidad de forma independiente.
- Los filtros se aplican simultáneamente sin recargar la página.
- El cliente puede combinar múltiples filtros (p.ej. puerto + categoría + rango de precio).
- El cliente puede limpiar todos los filtros con un botón 'Limpiar filtros'.
- Los resultados se actualizan correctamente cuando se añade, modifica o elimina un filtro.

### HU-07 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la ficha detallada de un barco y seleccionar la cantidad de unidades, para añadirlo a la cesta.

**Criterios de aceptación**

- Al hacer clic en un barco, se muestra su ficha con detalles completos (nombre, descripción, precio, categoría, puerto, fabricante, capacidad).
- El cliente puede seleccionar una cantidad de unidades (mínimo 1).
- El cliente puede añadir el barco a la cesta con la cantidad seleccionada.
- Se muestra un mensaje de confirmación tras añadir a la cesta.

### HU-08 — Cesta visible y persistente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página, para saber qué barcos he seleccionado.

**Criterios de aceptación**

- La cesta aparece en un panel lateral o superior visible en todas las páginas.
- La cesta muestra el número de artículos y el importe total.
- El cliente puede hacer clic en la cesta para ver su contenido detallado.
- La cesta persiste durante la sesión del cliente.

### HU-09 — Modificación y vaciado de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero modificar las cantidades de los barcos en la cesta o vaciarla completamente, para ajustar mi compra antes de pagar.

**Criterios de aceptación**

- El cliente puede aumentar o disminuir la cantidad de cada barco en la cesta.
- El cliente puede eliminar un barco individual de la cesta.
- El cliente puede vaciar toda la cesta con un botón 'Vaciar cesta'.
- El administrador puede vaciar la cesta cuando entra al modo administrador.
- Los cambios en la cesta se reflejan inmediatamente en el importe total.

### HU-10 — Reserva sin registro previo

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como visitante, quiero reservar un barco sin necesidad de registrarme previamente, para completar la compra rápidamente.

**Criterios de aceptación**

- El cliente puede proceder al pago sin estar autenticado.
- El cliente proporciona sus datos (nombre, correo, teléfono) durante el proceso de reserva.
- El proceso de reserva no exige un registro previo en la plataforma.

### HU-11 — Inicio de sesión durante reserva con recuperación de cesta

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente, quiero poder iniciar sesión durante el proceso de reserva y recuperar mi cesta anterior, para continuar con mi compra sin perder los barcos seleccionados.

**Criterios de aceptación**

- Durante el proceso de reserva, el cliente puede hacer clic en 'Iniciar sesión'.
- Tras iniciar sesión, la cesta anterior del cliente se recupera y se muestra.
- El cliente puede continuar con el proceso de reserva con los barcos recuperados.
- Si el cliente no tiene una cesta anterior, procede con la cesta actual.

### HU-12 — Proceso de reserva en tres pasos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar la reserva en no más de tres pasos sin exigir registro previo, para agilizar el proceso de compra.

**Criterios de aceptación**

- El proceso de reserva consta de exactamente tres pasos o menos.
- Paso 1: Confirmación de barcos y fechas de la cesta.
- Paso 2: Datos del cliente (nombre, correo, teléfono) y método de pago.
- Paso 3: Confirmación final y pago.
- El cliente puede navegar hacia atrás entre pasos para modificar datos.
- No se exige registro previo para completar la reserva.

### HU-13 — Cálculo de tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, debo aplicar la tasa de combustible correctamente según la categoría del barco, para calcular el importe total de la reserva.

**Criterios de aceptación**

- La tasa de combustible es de 50 € por día para todos los barcos.
- Para barcos de categoría 'velero', la tasa de combustible es 0 €.
- El importe total de la reserva incluye el precio base del barco, el número de días y la tasa de combustible aplicable.
- El cliente ve el desglose del importe (precio base + tasa de combustible) antes de confirmar.

### HU-14 — Confirmación de reserva y envío de código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi pedido.

**Criterios de aceptación**

- Tras finalizar la reserva, el cliente recibe un correo electrónico de confirmación.
- El correo incluye: nombre del barco, rango de fechas de la reserva, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin autenticación.
- El correo se envía desde una dirección de correo configurada en el sistema.

### HU-15 — Pago mediante PayPal Sandbox

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero pagar mi reserva mediante PayPal Sandbox, para completar la transacción de forma segura.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal como método de pago.
- El cliente es redirigido a PayPal Sandbox para completar el pago.
- Tras un pago exitoso, la reserva se marca como PAGADO.
- Tras un pago fallido, se muestra un mensaje de error y la reserva permanece en PENDIENTE DE PAGO.
- La integración con PayPal Sandbox está completamente funcional.

### HU-16 — Pago mediante contra-reembolso

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero poder pagar mediante contra-reembolso, para completar la reserva sin usar una pasarela de pago en línea.

**Criterios de aceptación**

- El cliente puede seleccionar contra-reembolso como método de pago.
- La reserva se crea en estado PENDIENTE DE PAGO.
- El administrador puede cambiar el estado a PAGADO cuando se reciba el pago.
- El cliente recibe un correo de confirmación con instrucciones de pago.

### HU-17 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, debo gestionar los estados de reserva correctamente, para reflejar el ciclo de vida de cada reserva.

**Criterios de aceptación**

- Los estados de reserva son: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO.
- No existe el estado CANCELADO; las reservas canceladas se eliminan del sistema.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El administrador puede cambiar el estado de una reserva entre los estados válidos.
- El sistema registra la fecha y hora de cada cambio de estado.

### HU-18 — Cancelación de reserva por administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero poder cancelar una reserva en estado PENDIENTE DE PAGO, para eliminarla del sistema cuando sea necesario.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas.
- El administrador puede seleccionar una reserva en estado PENDIENTE DE PAGO y cancelarla.
- Al cancelar, la reserva se elimina completamente del sistema.
- Las reservas en otros estados (PAGADO, EN USO, DEVUELTO) no pueden ser canceladas.
- Se muestra un mensaje de confirmación antes de eliminar la reserva.

### HU-19 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento, incluso sin estar registrado, para hacer seguimiento de mi pedido.

**Criterios de aceptación**

- Existe una página pública de 'Seguimiento de pedidos'.
- El cliente introduce el código de seguimiento en un campo de texto.
- El sistema muestra el estado actual de la reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO).
- Se muestra también el barco reservado, las fechas y el importe total.
- Si el código no existe, se muestra un mensaje de error.

### HU-20 — Consulta de reservas del cliente autenticado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de mis reservas desde mi cuenta, para hacer seguimiento de mis pedidos.

**Criterios de aceptación**

- El cliente autenticado accede a una sección 'Mis reservas' en su cuenta.
- Se muestra un listado de todas las reservas del cliente con sus estados.
- Cada reserva muestra: barco, fechas, importe, estado y código de seguimiento.
- El cliente puede hacer clic en una reserva para ver sus detalles completos.

### HU-21 — Gestión administrativa de barcos

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar el catálogo de barcos (crear, editar, eliminar), para mantener la información actualizada.

**Criterios de aceptación**

- El administrador accede a un panel de gestión de barcos.
- El administrador puede crear un nuevo barco con todos sus atributos (nombre, descripción, precio, categoría, puerto, fabricante, capacidad).
- El administrador puede editar los datos de un barco existente.
- El administrador puede eliminar un barco del catálogo.
- Los cambios se reflejan inmediatamente en el catálogo visible para los clientes.

### HU-22 — Gestión administrativa de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los clientes registrados, para mantener el control sobre las cuentas de usuario.

**Criterios de aceptación**

- El administrador accede a un listado de todos los clientes registrados.
- El administrador puede ver los detalles de cada cliente (correo, nombre, reservas asociadas).
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Si se intenta eliminar un cliente con reservas pendientes, se muestra un mensaje de error.
- Se muestra un mensaje de confirmación antes de eliminar un cliente.

### HU-23 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero gestionar todas las reservas del sistema, para cambiar sus estados y hacer seguimiento.

**Criterios de aceptación**

- El administrador accede a un listado de todas las reservas.
- El administrador puede filtrar reservas por estado, cliente, barco o rango de fechas.
- El administrador puede cambiar el estado de una reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO).
- El administrador puede cancelar una reserva en estado PENDIENTE DE PAGO (eliminándola del sistema).
- Se muestra un historial de cambios de estado para cada reserva.

### HU-24 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, debo operar bajo la zona horaria Europe/Madrid y el locale español, para garantizar consistencia en fechas y formatos.

**Criterios de aceptación**

- El sistema está configurado con la zona horaria Europe/Madrid en Django.
- Las fechas y horas se muestran en formato español (dd/mm/yyyy HH:mm).
- Los mensajes del sistema están en español.
- Los cálculos de fechas y horas respetan la zona horaria configurada.

### HU-25 — Datos seed precargados

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, debo arrancar con datos precargados para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación carga automáticamente 5 barcos al arrancar.
- La aplicación carga automáticamente 2 puertos al arrancar.
- La aplicación carga automáticamente 2 fabricantes al arrancar.
- La aplicación carga automáticamente 2 categorías (una de ellas 'velero') al arrancar.
- La aplicación carga automáticamente 1 usuario administrador de prueba al arrancar.
- Los datos seed se cargan de forma fiable en cada arranque sin duplicados.

### HU-26 — Seguridad de contraseñas y CSRF

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, debo implementar medidas de seguridad para proteger las contraseñas y prevenir ataques CSRF.

**Criterios de aceptación**

- Las contraseñas se almacenan de forma segura usando hash, no en texto plano.
- Django CSRF está activo en todos los formularios.
- Los tokens CSRF se validan en cada solicitud POST.
- Las contraseñas cumplen con los requisitos de seguridad de Django.
