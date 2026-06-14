---
run_id: run_2026-05-19_02-15
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-19T02:56:07+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-19_02-15`

Total de historias: **7**

## Historias del sprint

### HU-07 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la cesta siempre visible, modificar cantidades, revisar el estado y vaciarla si es necesario, para gestionar mis compras.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-08 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin haberse registrado previamente, para alquilar un barco de forma rápida.

**Criterios de aceptación**

- El cliente puede completar una reserva sin haberse registrado previamente.
- El proceso de reserva se realiza en no más de tres pasos.
- Durante el proceso se solicitan los datos del cliente y los datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.

### HU-09 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero pagar mediante PayPal Sandbox o contra-reembolso, para elegir el método de pago que prefiero.

**Criterios de aceptación**

- El cliente puede pagar mediante PayPal Sandbox.
- El cliente puede pagar mediante contra-reembolso.
- La integración de PayPal utiliza el entorno Sandbox, no producción.
- Se validan todos los formularios de pago.
- El formulario de pago incluye validación CSRF.

### HU-10 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de la reserva y un código de seguimiento, para confirmar mi alquiler y poder consultarlo después.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo incluye los datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva.
- El correo se envía en español.

### HU-11 — Cálculo de precio con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el precio total de la reserva considerando el precio diario del barco, la cantidad de días y una tasa de combustible, para cobrar el importe correcto.

**Criterios de aceptación**

- Los alquileres se miden por día.
- Se aplica una tasa de combustible de 50 euros por día.
- Para barcos de categoría velero, la tasa de combustible es 0 euros.
- El precio total se calcula correctamente en el proceso de reserva.
- El precio total se muestra al cliente antes de confirmar el pago.

### HU-12 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas para controlar su ciclo de vida.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO o PAGADO según el método de pago.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas mediante botones por transición aplicable.
- El sistema registra el historial de cambios de estado.

### HU-14 — Recordatorio de reserva pendiente

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero enviar un correo de recordatorio al cliente cuando falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO.

**Criterios de aceptación**

- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio.
- El correo incluye los datos de la reserva y un enlace para completar el pago.
- El correo se envía en español.
- El sistema registra que el recordatorio fue enviado.
