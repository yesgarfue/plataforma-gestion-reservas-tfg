---
run_id: run_2026-05-12_15-34
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-12T15:59:09+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_15-34`

Total de historias: **7**

## Historias del sprint

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
