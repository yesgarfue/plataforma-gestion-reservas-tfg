---
run_id: run_2026-05-15_11-00
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-15T11:09:45+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-15_11-00`

Total de historias: **6**

## Historias del sprint

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
