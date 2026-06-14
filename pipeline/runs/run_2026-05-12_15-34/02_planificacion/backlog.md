---
run_id: run_2026-05-12_15-34
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T15:55:36+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Backlog

**ID de ejecución**: `run_2026-05-12_15-34`

Total de historias: **22**

## Historias

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Las contraseñas se almacenan de forma segura, no en texto plano.
- Se activa protección CSRF en el formulario de registro.

### HU-02 — Inicio de sesión de cliente

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error sin revelar qué campo es incorrecto.
- Se activa protección CSRF en el formulario de login.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para terminar mi sesión de forma segura.

**Criterios de aceptación**

- El cliente puede pulsar un botón 'Cerrar sesión' desde cualquier página.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se invalida completamente en el servidor.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver el catálogo de barcos organizado por categorías en la página principal, para explorar los barcos disponibles.

**Criterios de aceptación**

- La página principal muestra todos los barcos del catálogo.
- Los barcos se organizan por categorías.
- Los barcos no disponibles en un rango de fechas muestran una etiqueta 'No disponible'.
- El catálogo carga con los datos seed: 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (una de ellas 'velero').

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título, para encontrar rápidamente el barco que me interesa.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de búsqueda.
- La búsqueda filtra el catálogo por nombre o título del barco.
- Si no hay resultados, se muestra un mensaje indicando que no se encontraron barcos.

### HU-06 — Filtros combinables del catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero aplicar filtros combinables (puertos, fabricantes, precio y cantidad) al catálogo, para refinar mi búsqueda de barcos.

**Criterios de aceptación**

- El cliente puede filtrar por puerto.
- El cliente puede filtrar por fabricante.
- El cliente puede filtrar por rango de precio.
- El cliente puede filtrar por cantidad disponible.
- Los filtros pueden aplicarse simultáneamente de forma independiente.
- El catálogo se actualiza en tiempo real al cambiar los filtros.

### HU-07 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la ficha detallada de un barco y seleccionar la cantidad de unidades que deseo reservar, para añadirlas a mi cesta.

**Criterios de aceptación**

- La ficha del barco muestra todos los detalles del barco (nombre, descripción, precio, categoría, fabricante, puerto).
- El cliente puede seleccionar la cantidad de unidades a reservar.
- El cliente puede añadir la cantidad seleccionada a su cesta.
- Se muestra un mensaje de confirmación tras añadir a la cesta.

### HU-08 — Cesta visible y modificable

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver mi cesta siempre visible desde cualquier página y poder modificar las cantidades o vaciarla, para gestionar mis reservas antes de pagar.

**Criterios de aceptación**

- La cesta está siempre visible en la interfaz desde cualquier página.
- El cliente puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El cliente puede revisar el estado de su cesta desde el catálogo.
- El cliente puede vaciar completamente la cesta.
- El total de la cesta se actualiza en tiempo real.

### HU-09 — Vaciado de cesta al entrar como administrador

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador, quiero que mi cesta se vacíe al cambiar a modo administrador, para evitar confusiones entre mis datos de cliente y administrador.

**Criterios de aceptación**

- Al entrar en modo administrador, la cesta se vacía automáticamente.
- El administrador no puede añadir barcos a la cesta.
- El administrador puede revisar el estado de su cesta (vacía) desde la interfaz.

### HU-10 — Proceso de reserva en tres pasos sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero realizar una reserva en tres pasos sin necesidad de registrarme previamente, para completar mi compra rápidamente.

**Criterios de aceptación**

- El proceso de reserva consta de tres pasos claramente definidos.
- En el paso 1 se solicitan los datos del cliente (nombre, correo, teléfono) o se heredan si hay sesión iniciada.
- En el paso 2 se solicitan los datos de pago (método y detalles).
- En el paso 3 se muestra un resumen de la reserva antes de confirmar.
- El cliente puede completar la reserva sin estar registrado.

### HU-11 — Métodos de pago: PayPal Sandbox y contra-reembolso

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como método de pago, para pagar mi reserva de la forma que prefiera.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- Si elige PayPal Sandbox, se redirige a la pasarela de PayPal Sandbox.
- Si elige contra-reembolso, la reserva se crea en estado PENDIENTE DE PAGO.
- Tras completar el pago, se muestra un mensaje de confirmación.

### HU-12 — Correo de confirmación con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi alquiler.

**Criterios de aceptación**

- Tras completar la reserva, se envía un correo al cliente.
- El correo contiene los datos del barco reservado.
- El correo contiene el rango de fechas de la reserva.
- El correo contiene el importe total de la reserva.
- El correo contiene el código de seguimiento único de la reserva.

### HU-13 — Tasa de combustible con excepción para veleros

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en todas las reservas, excepto para barcos de categoría 'velero' donde la tasa es 0 €, para calcular correctamente el importe total.

**Criterios de aceptación**

- Para barcos que no son veleros, se aplica una tasa de 50 € por día.
- Para barcos de categoría 'velero', la tasa de combustible es 0 €.
- La tasa se calcula correctamente en el importe total de la reserva.
- El cliente ve el desglose de la tasa en el resumen de la reserva.

### HU-14 — Cancelación de reserva en estado PENDIENTE DE PAGO

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero cancelar mi reserva si está en estado PENDIENTE DE PAGO, para desistir de mi compra si cambio de opinión.

**Criterios de aceptación**

- El cliente puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO.
- Tras cancelar, la reserva se elimina del sistema.
- La reserva desaparece del listado de reservas del cliente.
- Se muestra un mensaje de confirmación tras la cancelación.

### HU-15 — Recordatorio por email antes del inicio de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un recordatorio por email al cliente si falta un día para el inicio de su reserva, para que no olvide su alquiler.

**Criterios de aceptación**

- Se envía un email automático si falta exactamente un día para el inicio de la reserva.
- El email contiene los datos de la reserva y el código de seguimiento.
- El email se envía solo si la reserva está en estado CONFIRMADA o posterior.

### HU-16 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente no registrado, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por email, para saber el estado de mi alquiler sin necesidad de registrarme.

**Criterios de aceptación**

- El cliente puede introducir un código de seguimiento en un formulario de búsqueda.
- Se muestra el estado actual de la reserva (PENDIENTE DE PAGO, CONFIRMADA, CANCELADA, etc.).
- Se muestran los datos de la reserva (barco, fechas, importe).
- Si el código no existe, se muestra un mensaje de error.

### HU-17 — Historial de reservas del cliente registrado

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero consultar el historial de todas mis reservas desde mi cuenta, para revisar mis alquileres anteriores y actuales.

**Criterios de aceptación**

- El cliente autenticado puede acceder a su historial de reservas.
- Se muestran todas las reservas del cliente (pasadas, actuales y canceladas).
- Cada reserva muestra el barco, fechas, importe y estado.
- El cliente puede ver el código de seguimiento de cada reserva.

### HU-18 — Gestión administrativa de reservas

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como administrador, quiero gestionar las reservas, ver su estado y cambiar el estado de una reserva que esté en PENDIENTE DE PAGO, para administrar los alquileres.

**Criterios de aceptación**

- El administrador puede ver un listado de todas las reservas del sistema.
- El administrador puede ver los detalles de cada reserva (cliente, barco, fechas, estado, importe).
- El administrador puede cambiar el estado de una reserva únicamente si está en PENDIENTE DE PAGO.
- El administrador puede cambiar el estado a CONFIRMADA o CANCELADA.
- Se muestra un mensaje de confirmación tras cambiar el estado.

### HU-19 — Eliminación de cliente por administrador

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero eliminar un cliente únicamente si no tiene reservas pendientes, para mantener la integridad de los datos.

**Criterios de aceptación**

- El administrador puede ver un listado de clientes.
- El administrador puede eliminar un cliente solo si no tiene reservas pendientes.
- Si el cliente tiene reservas pendientes, se muestra un mensaje indicando que no puede ser eliminado.
- Tras eliminar un cliente, se muestra un mensaje de confirmación.

### HU-20 — Recuperación de cesta al iniciar sesión durante reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que mi cesta se recupere si inicio sesión durante el proceso de reserva, para continuar con mi compra sin perder los barcos seleccionados.

**Criterios de aceptación**

- Si el cliente inicia sesión durante el proceso de reserva, la cesta se mantiene.
- Tras iniciar sesión, el cliente vuelve a la página de login y puede continuar el proceso.
- Los barcos en la cesta se recuperan correctamente.
- El cliente puede continuar el proceso de reserva desde donde lo dejó.

### HU-21 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero operar bajo la zona horaria Europe/Madrid con locale español, para que todas las fechas y textos se muestren correctamente.

**Criterios de aceptación**

- La zona horaria del sistema está configurada como Europe/Madrid.
- El locale del sistema está configurado como español.
- Las fechas se muestran en formato español (DD/MM/YYYY).
- Los textos de la interfaz se muestran en español.

### HU-22 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación esté empaquetada en un contenedor Docker con instrucciones claras, para desplegar la aplicación de forma consistente.

**Criterios de aceptación**

- La aplicación incluye un Dockerfile con las instrucciones de construcción.
- El README contiene instrucciones claras para construir y arrancar el contenedor.
- El contenedor arranca correctamente con los datos seed precargados.
- La aplicación es accesible desde el contenedor en el puerto configurado.
