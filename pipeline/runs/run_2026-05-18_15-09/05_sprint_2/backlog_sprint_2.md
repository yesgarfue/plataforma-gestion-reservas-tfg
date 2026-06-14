---
run_id: run_2026-05-18_15-09
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-18T16:03:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-18_15-09`

Total de historias: **6**

## Historias del sprint

### HU-07 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la cesta siempre visible, modificar cantidades y revisar su estado desde el catálogo, para gestionar mis compras.

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
- Durante el proceso de reserva se solicitan los datos del cliente y los datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.

### HU-09 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como métodos de pago durante la reserva.

**Criterios de aceptación**

- El sistema ofrece PayPal Sandbox como método de pago.
- El sistema ofrece contra-reembolso como método de pago.
- El cliente puede seleccionar uno de los dos métodos durante el proceso de reserva.
- La integración de PayPal utiliza el entorno Sandbox, no producción.

### HU-10 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para confirmar y rastrear mi alquiler.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico con los datos del barco, rango de fechas, importe total y código de seguimiento.
- El correo incluye el código de seguimiento único para consultar el estado de la reserva.
- El correo está redactado en español.

### HU-11 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible diferenciada según la categoría del barco, para calcular correctamente el importe total de la reserva.

**Criterios de aceptación**

- El sistema aplica una tasa de combustible de 50 € por día para barcos que no sean veleros.
- El sistema aplica una tasa de combustible de 0 € por día para barcos de categoría velero.
- La tasa se incluye en el cálculo del importe total de la reserva.
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-12 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero gestionar los estados de las reservas para reflejar su ciclo de vida.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El estado se actualiza según las transiciones aplicables del ciclo de vida.
