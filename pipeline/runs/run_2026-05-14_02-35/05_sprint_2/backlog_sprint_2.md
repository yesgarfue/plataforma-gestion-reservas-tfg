---
run_id: run_2026-05-14_02-35
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-14T02:48:23+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_02-35`

Total de historias: **5**

## Historias del sprint

### HU-07 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin haberse registrado previamente, proporcionando datos del cliente y datos de pago.

**Criterios de aceptación**

- El cliente puede completar una reserva sin haberse registrado previamente.
- El proceso de reserva se realiza en no más de tres pasos.
- Durante el proceso de reserva se solicitan los datos del cliente y los datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.
- Desde la cesta el usuario puede finalizar la compra iniciando el proceso de reserva.

### HU-08 — Pago mediante PayPal Sandbox

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero pagar mi reserva mediante PayPal Sandbox, para completar la transacción de forma segura.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- La integración de PayPal utiliza el entorno Sandbox, no producción.
- El cliente es redirigido a PayPal para completar el pago.
- Tras completar el pago en PayPal, el cliente regresa a la aplicación.
- El estado de la reserva se actualiza a PAGADO tras un pago exitoso.

### HU-09 — Pago mediante contra-reembolso

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero pagar mi reserva mediante contra-reembolso, para completar la reserva sin pagar en línea.

**Criterios de aceptación**

- El cliente puede seleccionar contra-reembolso como método de pago.
- Al seleccionar contra-reembolso, la reserva se crea en estado PENDIENTE DE PAGO.
- El cliente recibe un correo de confirmación con los datos de la reserva.

### HU-10 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-11 — Cálculo de tarifa con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el importe total de la reserva considerando el precio diario del barco, la cantidad de días y una tasa de combustible diferenciada por categoría.

**Criterios de aceptación**

- Los alquileres se miden por día.
- Se aplica una tasa de combustible de 50 euros por día para todos los barcos.
- Para barcos de categoría velero, la tasa de combustible es 0 euros.
- El importe total se calcula como: (precio_diario * cantidad_dias * cantidad_barcos) + (tasa_combustible * cantidad_dias * cantidad_barcos).
- El importe total se muestra al cliente antes de confirmar la reserva.
