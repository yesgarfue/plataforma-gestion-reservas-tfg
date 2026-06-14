---
run_id: run_2026-05-15_09-52
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-15T10:00:43+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-15_09-52`

Total de historias: **6**

## Historias del sprint

### HU-07 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero visualizar mi cesta desde cualquier página, modificar las cantidades de barcos y vaciarla, para gestionar mis reservas antes de finalizar la compra.

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

Como cliente, quiero completar una reserva en no más de tres pasos sin haberse registrado previamente, proporcionando mis datos y datos de pago, para alquilar un barco sin trámites previos.

**Criterios de aceptación**

- El proceso de reserva se realiza en no más de tres pasos.
- No se exige registro previo para completar una reserva.
- Durante el proceso se solicitan los datos del cliente y datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.
- El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login.

### HU-09 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre PayPal Sandbox y contra-reembolso como métodos de pago, para completar mi reserva con la opción que prefiera.

**Criterios de aceptación**

- El sistema ofrece PayPal Sandbox como método de pago.
- El sistema ofrece contra-reembolso como método de pago.
- El cliente puede seleccionar uno de los dos métodos durante el proceso de reserva.
- La integración de PayPal utiliza el entorno Sandbox, no producción.

### HU-10 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco, rango de fechas, importe total y código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva.

### HU-11 — Tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en las reservas, excepto para barcos de categoría velero donde la tasa es 0 €, para calcular correctamente el importe total.

**Criterios de aceptación**

- El sistema aplica una tasa de combustible de 50 € por día a todas las reservas.
- Para barcos de categoría velero, la tasa de combustible es 0 €.
- El importe total de la reserva incluye la tasa de combustible calculada correctamente.

### HU-12 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero que cada reserva tenga uno de los estados PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO, para gestionar el ciclo de vida de las reservas.

**Criterios de aceptación**

- Cada reserva se crea en estado PENDIENTE DE PAGO.
- El sistema permite transiciones entre estados según las reglas de negocio.
- El estado de una reserva es visible para el cliente y el administrador.
