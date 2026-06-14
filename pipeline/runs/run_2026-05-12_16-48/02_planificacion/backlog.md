---
run_id: run_2026-05-12_16-48
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T17:01:38+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-12_16-48`

Total de historias: **24**

## Historias

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme mediante correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Las contraseñas se almacenan de forma segura, no en texto plano.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Se valida que el correo no esté ya registrado.

### HU-02 — Inicio de sesión

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- El cliente puede iniciar sesión durante el proceso de reserva, reconstruyendo la cesta.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para salir de mi cuenta de forma segura.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón de cierre de sesión.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se termina en el servidor.

### HU-04 — Reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero realizar una reserva sin necesidad de registrarme previamente, para agilizar el proceso de compra.

**Criterios de aceptación**

- El cliente puede completar una reserva sin tener una cuenta registrada.
- Se solicitan los datos del cliente durante el proceso de reserva.
- El cliente recibe un código de seguimiento para consultar el estado de su reserva.

### HU-05 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos.
- Los barcos están organizados por categorías.
- Cada barco muestra nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos agotados o no disponibles aparecen claramente marcados.

### HU-06 — Búsqueda y filtros combinables

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar barcos por nombre y aplicar filtros combinables, para encontrar la embarcación que se ajuste a mis necesidades.

**Criterios de aceptación**

- Se puede buscar por nombre o título de barco.
- Los filtros combinables incluyen puertos, fabricantes, precio, categoría, capacidad y rango de fechas.
- Los filtros por puerto y fabricante se presentan como desplegables con valores válidos.
- Los filtros se aplican de forma combinada.
- Los resultados se actualizan al aplicar o cambiar filtros.

### HU-07 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la ficha detallada de un barco y seleccionar la cantidad de unidades, para añadirlo a mi cesta.

**Criterios de aceptación**

- La ficha del barco muestra todos los datos del barco e imagen.
- El cliente puede seleccionar la cantidad de unidades del barco.
- El cliente puede añadir el barco a la cesta desde la ficha.
- Se valida que la cantidad sea mayor a cero.

### HU-08 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver, modificar y vaciar mi cesta desde cualquier página, para gestionar mis compras antes de finalizar.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Cuando el administrador entra en modo administrador, la cesta se vacía y no puede añadir artículos.

### HU-09 — Proceso de reserva en tres pasos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin exigir registro previo, para finalizar mi compra de forma rápida.

**Criterios de aceptación**

- El proceso de reserva consta de no más de tres pasos.
- Se solicitan los datos del cliente durante el proceso.
- Se solicitan los datos de pago durante el proceso.
- El cliente puede completar la reserva sin estar registrado.
- Se calcula el precio total incluyendo la tasa de combustible cuando aplique.

### HU-10 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago para completar mi reserva, para usar la opción que me resulte más conveniente.

**Criterios de aceptación**

- Se ofrecen dos métodos de pago: PayPal Sandbox y contra-reembolso.
- El cliente puede seleccionar el método de pago durante el proceso de reserva.
- El pago se procesa según el método seleccionado.
- Se valida que los datos de pago sean correctos antes de procesar.

### HU-11 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi pedido.

**Criterios de aceptación**

- Tras completar la reserva, se envía un correo electrónico al cliente.
- El correo contiene los datos del barco reservado, el rango de fechas y el código de seguimiento.
- El cliente recibe el código de seguimiento para consultar el estado de su reserva.
- El correo se envía de forma fiable en el entorno configurado.

### HU-12 — Cálculo de precio con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el precio total de la reserva aplicando la tasa de combustible según la categoría del barco, para cobrar el importe correcto.

**Criterios de aceptación**

- Los alquileres se miden por día.
- Se aplica una tasa de combustible de 50 €/día para barcos que no sean de categoría 'velero'.
- Para barcos de categoría 'velero', no se aplica tasa de combustible.
- El precio total se calcula correctamente en el proceso de reserva.

### HU-13 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas para reflejar su ciclo de vida, desde la creación hasta la devolución.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- El estado de la reserva se actualiza correctamente en el sistema.

### HU-14 — Recordatorio de pago pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, para asegurar que complete el pago a tiempo.

**Criterios de aceptación**

- Se identifica automáticamente las reservas que faltan un día para iniciarse y están en estado PENDIENTE DE PAGO.
- Se envía un correo recordatorio al cliente con los datos de la reserva.
- El correo se envía una sola vez por reserva.

### HU-15 — Consulta de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero consultar el estado de mi reserva usando el código de seguimiento recibido, para saber en qué punto está mi pedido sin necesidad de estar registrado.

**Criterios de aceptación**

- El cliente puede ingresar un código de seguimiento en un formulario de búsqueda.
- Se muestra el estado actual de la reserva asociada al código.
- Se muestran los datos del barco, el rango de fechas y el estado de la reserva.
- Si el código no existe, se muestra un mensaje de error.

### HU-16 — Consulta de reservas del cliente registrado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el estado de todas mis reservas desde mi cuenta, para tener un historial de mis pedidos.

**Criterios de aceptación**

- El cliente autenticado puede acceder a un listado de sus reservas.
- Se muestran los datos de cada reserva: barco, fechas, estado y código de seguimiento.
- El cliente puede ver el estado actual de cada reserva.

### HU-17 — Panel de administración

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero acceder a un panel de administración propio diferente del admin de Django, para gestionar barcos, clientes y reservas.

**Criterios de aceptación**

- El panel de administración es accesible solo para usuarios administrador.
- El panel es diferente del admin de Django por defecto.
- El panel permite navegar entre gestión de barcos, clientes y reservas.
- El acceso al panel requiere autenticación.

### HU-18 — Gestión de barcos en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero gestionar los barcos en el panel de administración, para mantener el catálogo actualizado.

**Criterios de aceptación**

- El administrador puede dar de alta nuevos barcos con todos los campos requeridos.
- El administrador puede editar los datos de un barco existente.
- El administrador puede dar de baja un barco del sistema.
- Se valida que todos los campos obligatorios estén completos.
- La imagen del barco es obligatoria.

### HU-19 — Gestión de clientes en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y eliminar clientes en el panel de administración, para mantener la base de datos de usuarios.

**Criterios de aceptación**

- El administrador puede ver un listado de todos los clientes registrados.
- El administrador puede eliminar un cliente únicamente si ese cliente no tiene reservas pendientes.
- Se muestra un mensaje de error si se intenta eliminar un cliente con reservas pendientes.
- Se confirma la eliminación antes de proceder.

### HU-20 — Gestión de reservas en administración

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero consultar y cambiar el estado de las reservas en el panel de administración, para gestionar el ciclo de vida de los pedidos.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas.
- El administrador puede cambiar el estado de una reserva mediante botones por transición.
- Se muestran los datos completos de cada reserva: cliente, barco, fechas, estado y código de seguimiento.
- Solo se permiten transiciones de estado válidas.

### HU-21 — Configuración de locale y zona horaria

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero operar con la zona horaria Europe/Madrid y localización española, para que todas las fechas y textos sean correctos para el usuario.

**Criterios de aceptación**

- La aplicación está configurada con zona horaria Europe/Madrid.
- La interfaz de usuario está íntegramente en español.
- Las fechas se muestran en formato español.
- Los textos del sistema están en español.

### HU-22 — Seguridad de contraseñas y CSRF

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero aplicar medidas de seguridad básicas para proteger las contraseñas y prevenir ataques CSRF.

**Criterios de aceptación**

- Las contraseñas no se almacenan en texto plano.
- Se aplica CSRF activo en todos los formularios.
- Las contraseñas se validan según estándares de seguridad de Django.

### HU-23 — Datos seed precargados

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero que la aplicación arranque con datos pre-cargados, para poder probar todas las funcionalidades de manera automática.

**Criterios de aceptación**

- La aplicación incluye un script de carga de datos iniciales.
- Los datos seed incluyen barcos de diferentes categorías, puertos y fabricantes.
- Los datos seed incluyen clientes de prueba.
- Los datos seed incluyen reservas en diferentes estados.
- Los datos se cargan automáticamente al iniciar la aplicación.

### HU-24 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como equipo de desarrollo, quiero que la aplicación se empaquete en un contenedor Docker, para facilitar el despliegue y la reproducibilidad del entorno.

**Criterios de aceptación**

- La aplicación incluye un Dockerfile funcional.
- El contenedor incluye todas las dependencias necesarias.
- Se proporciona un README con instrucciones de construcción y ejecución del contenedor.
- El contenedor se puede ejecutar sin configuración adicional.
