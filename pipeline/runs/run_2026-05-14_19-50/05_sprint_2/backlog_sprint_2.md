---
run_id: run_2026-05-14_19-50
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-14T20:10:28+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_19-50`

Total de historias: **6**

## Historias del sprint

### HU-06 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero visualizar, modificar y vaciar mi cesta desde cualquier página de la aplicación, para gestionar mis barcos antes de finalizar la compra.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-07 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin haberse registrado previamente, proporcionando datos de cliente y pago.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta.
- El proceso de reserva se realiza en no más de tres pasos.
- No se exige registro previo para completar una reserva.
- Durante el proceso se solicitan los datos del cliente y datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.

### HU-08 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como métodos de pago durante el proceso de reserva.

**Criterios de aceptación**

- El sistema ofrece PayPal Sandbox como método de pago.
- El sistema ofrece contra-reembolso como método de pago.
- El cliente puede seleccionar uno de los dos métodos durante el proceso de reserva.
- La integración de PayPal utiliza el entorno Sandbox, no producción.

### HU-09 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico de confirmación con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-10 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en todas las reservas, excepto para barcos de categoría velero donde la tasa es 0 €.

**Criterios de aceptación**

- El sistema calcula la tasa de combustible como 50 € por día para barcos que no son velero.
- El sistema aplica tasa de combustible de 0 € para barcos de categoría velero.
- La tasa se incluye en el importe total de la reserva.
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-11 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero gestionar los estados de las reservas: PENDIENTE DE PAGO, PAGADO, EN USO y DEVUELTO.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El estado se actualiza según las transiciones aplicables.
