---
run_id: run_2026-05-11_13-31
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-11T14:23:01+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-11_13-31`

Total de historias: **22**

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
- Tras un login incorrecto, se muestra un mensaje de error sin revelar qué campo es incorrecto.
- La sesión se mantiene activa durante la navegación.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para asegurar que mi cuenta no queda accesible en dispositivos compartidos.

**Criterios de aceptación**

- El cliente puede pulsar un botón 'Cerrar sesión' desde cualquier página.
- Al cerrar sesión, la sesión se invalida inmediatamente.
- El cliente es redirigido a la página de inicio tras cerrar sesión.
- Las cookies de sesión se eliminan del navegador.

### HU-04 — Eliminación de cliente por administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero eliminar un cliente únicamente si no tiene reservas pendientes, para mantener la integridad de los datos de reservas.

**Criterios de aceptación**

- El administrador puede acceder a un listado de clientes desde el panel de administración.
- Si el cliente no tiene reservas pendientes, aparece un botón 'Eliminar'.
- Si el cliente tiene reservas pendientes, el botón 'Eliminar' está deshabilitado y se muestra un mensaje explicativo.
- Al eliminar un cliente sin reservas, se elimina su registro de la base de datos.

### HU-05 — Catálogo de barcos por categoría

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías, para encontrar fácilmente el tipo de barco que deseo alquilar.

**Criterios de aceptación**

- El catálogo muestra todos los barcos disponibles.
- Los barcos están agrupados por categoría.
- Cada barco muestra su nombre, categoría, precio y una imagen representativa.
- El cliente puede navegar entre categorías.

### HU-06 — Disponibilidad de barcos por rango de fechas

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero ver qué barcos están disponibles para un rango de fechas específico, para planificar mi reserva.

**Criterios de aceptación**

- El cliente puede seleccionar una fecha de inicio y una fecha de fin.
- Los barcos que no están disponibles en ese rango se marcan como 'No disponibles'.
- Los barcos disponibles se marcan como 'Disponible'.
- La búsqueda se aplica al catálogo sin recargar la página.

### HU-07 — Selección de cantidad y adición a cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero seleccionar la cantidad de unidades de un barco y añadirla a la cesta, para preparar mi reserva.

**Criterios de aceptación**

- En la ficha del barco, hay un campo para seleccionar la cantidad (mínimo 1).
- El cliente puede pulsar 'Añadir a cesta'.
- El barco y la cantidad se añaden a la cesta.
- Se muestra un mensaje de confirmación.

### HU-08 — Visibilidad permanente de la cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la cesta siempre visible desde cualquier página, para saber en todo momento qué barcos he seleccionado.

**Criterios de aceptación**

- La cesta aparece en un panel lateral o superior en todas las páginas.
- La cesta muestra el número de artículos y el importe total.
- El cliente puede acceder a la cesta desde cualquier página sin perder el contexto.

### HU-09 — Modificación de cantidad en cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ampliar o reducir la cantidad de unidades de cada barco en la cesta, para ajustar mi reserva antes de pagar.

**Criterios de aceptación**

- En la cesta, cada barco muestra botones para aumentar o disminuir la cantidad.
- Al cambiar la cantidad, el importe total se actualiza automáticamente.
- Si la cantidad llega a 0, el barco se elimina de la cesta.
- Los cambios se guardan sin necesidad de confirmar.

### HU-10 — Vaciado de cesta al entrar como administrador

- **Prioridad**: Media
- **Estimación**: S

**Descripción**

Como administrador, quiero que la cesta se vacíe cuando cambio de rol de cliente a administrador, para evitar confusiones entre contextos.

**Criterios de aceptación**

- Si un cliente autenticado accede al panel de administrador, la cesta se vacía.
- Se muestra un mensaje informativo sobre el vaciado de cesta.
- Al volver al contexto de cliente, la cesta permanece vacía.

### HU-11 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como visitante, quiero reservar un barco sin necesidad de registrarme previamente, para agilizar el proceso de compra.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta sin estar autenticado.
- El proceso de reserva se completa en no más de tres pasos.
- En el primer paso, se solicitan datos de contacto (correo, nombre, teléfono).
- En el segundo paso, se selecciona el método de pago.
- En el tercer paso, se confirma la reserva y se procesa el pago.

### HU-12 — Inicio de sesión durante reserva con recuperación de cesta

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero iniciar sesión durante el proceso de reserva y recuperar mi cesta anterior, para continuar con mis compras previas.

**Criterios de aceptación**

- Durante el proceso de reserva, hay una opción para iniciar sesión.
- Al iniciar sesión, la cesta anterior del cliente se recupera.
- El cliente puede continuar con la reserva usando la cesta recuperada.
- Si hay conflictos entre la cesta anterior y la actual, se muestra un mensaje de confirmación.

### HU-13 — Métodos de pago: PayPal Sandbox y contra-reembolso

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago (PayPal Sandbox y contra-reembolso), para pagar de la forma que me resulte más cómoda.

**Criterios de aceptación**

- En el paso de pago, se muestran dos opciones: PayPal Sandbox y contra-reembolso.
- Si elige PayPal, se redirige a la pasarela de PayPal Sandbox.
- Si elige contra-reembolso, se confirma la reserva sin procesar pago en línea.
- Tras completar el pago, se muestra un mensaje de confirmación.

### HU-14 — Correo de confirmación con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi pedido.

**Criterios de aceptación**

- Al finalizar la reserva, se envía un correo al cliente.
- El correo contiene: datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva.
- El correo se envía incluso si el cliente no está registrado.

### HU-15 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero que cada reserva tenga un estado bien definido, para gestionar el ciclo de vida de las reservas.

**Criterios de aceptación**

- Una reserva puede estar en uno de estos estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO.
- El estado se asigna automáticamente al crear la reserva (PENDIENTE DE PAGO).
- El estado se actualiza automáticamente al procesar el pago (PAGADO).
- El administrador puede cambiar manualmente el estado a EN USO o DEVUELTO.

### HU-16 — Cancelación de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar mi reserva si está en estado PENDIENTE DE PAGO, para no perder dinero si cambio de planes.

**Criterios de aceptación**

- El cliente puede ver un botón 'Cancelar' solo si la reserva está en estado PENDIENTE DE PAGO.
- Al pulsar 'Cancelar', se solicita confirmación.
- Si confirma, la reserva se elimina del sistema.
- Se muestra un mensaje de confirmación de cancelación.

### HU-17 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento, para saber en qué fase está mi pedido sin necesidad de iniciar sesión.

**Criterios de aceptación**

- Hay una página pública de 'Seguimiento de pedidos'.
- El cliente introduce el código de seguimiento.
- Se muestra el estado actual de la reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO).
- Se muestran los datos del barco, rango de fechas e importe.

### HU-18 — Panel de administración: gestión de barcos

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar el catálogo de barcos desde un panel propio, para añadir, editar o eliminar barcos.

**Criterios de aceptación**

- El administrador puede acceder a un listado de barcos.
- Puede crear un nuevo barco con nombre, categoría, precio, capacidad y disponibilidad.
- Puede editar los datos de un barco existente.
- Puede eliminar un barco si no tiene reservas activas.
- Los cambios se guardan en la base de datos inmediatamente.

### HU-19 — Panel de administración: gestión de clientes

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los clientes registrados desde un panel propio, para ver sus datos y eliminarlos si es necesario.

**Criterios de aceptación**

- El administrador puede acceder a un listado de clientes.
- Se muestra el correo, nombre y fecha de registro de cada cliente.
- Puede ver el historial de reservas de cada cliente.
- Puede eliminar un cliente si no tiene reservas pendientes (ver HU-04).
- Los cambios se guardan en la base de datos inmediatamente.

### HU-20 — Panel de administración: gestión de reservas

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar todas las reservas desde un panel propio, para cambiar estados y resolver incidencias.

**Criterios de aceptación**

- El administrador puede acceder a un listado de todas las reservas.
- Se muestra el código de seguimiento, cliente, barco, fechas, importe y estado.
- Puede cambiar el estado de una reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO).
- Puede ver los detalles completos de cada reserva.
- Los cambios se guardan en la base de datos inmediatamente.

### HU-21 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero que la aplicación use la zona horaria Europe/Madrid y el locale en español, para que las fechas y textos sean correctos para los usuarios españoles.

**Criterios de aceptación**

- La zona horaria del proyecto Django está configurada como Europe/Madrid.
- El locale está configurado en español.
- Las fechas se muestran en formato español (dd/mm/yyyy).
- Los textos de la interfaz están en español.

### HU-22 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación esté empaquetada en un contenedor Docker, para facilitar su despliegue y ejecución en cualquier entorno.

**Criterios de aceptación**

- Existe un Dockerfile que define la imagen de la aplicación.
- El Dockerfile incluye todas las dependencias necesarias (Django 3.2, SQLite, etc.).
- Existe un README con instrucciones claras de construcción y arranque del contenedor.
- El contenedor se puede construir y ejecutar sin errores.
