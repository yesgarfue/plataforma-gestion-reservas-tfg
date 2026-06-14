---
run_id: run_2026-05-12_13-29
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-12T13:56:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_13-29`

Total de historias: **8**

## Historias del sprint

### HU-08 — Modificación de la cesta

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente, quiero aumentar o reducir la cantidad de unidades de cada barco en la cesta, para ajustar mi reserva antes de pagar.

**Criterios de aceptación**

- El cliente puede aumentar la cantidad de un barco en la cesta.
- El cliente puede reducir la cantidad de un barco en la cesta.
- El cliente puede eliminar completamente un barco de la cesta.
- El importe total se recalcula automáticamente tras cada cambio.
- La cesta se vacía si el cliente entra en modo administrador.

### HU-09 — Proceso de reserva en tres pasos sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como visitante, quiero completar una compra en un proceso de tres pasos sin necesidad de registrarme previamente, para realizar una reserva rápidamente.

**Criterios de aceptación**

- El proceso de reserva consta de tres pasos claramente definidos.
- El cliente puede completar la reserva sin estar registrado.
- Los datos del cliente se solicitan durante el proceso de reserva.
- La cesta se mantiene durante todo el proceso.
- Al finalizar, se genera un código de seguimiento.

### HU-10 — Métodos de pago: PayPal Sandbox y contra-reembolso

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago (PayPal Sandbox y contra-reembolso), para pagar de la forma que prefiero.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- La integración con PayPal Sandbox funciona correctamente en el entorno de pruebas.
- El flujo de contra-reembolso registra la reserva en estado PENDIENTE DE PAGO.
- Se valida que se haya seleccionado un método de pago antes de confirmar.

### HU-11 — Tasa de combustible y excepción para veleros

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que se aplique correctamente la tasa de combustible en mi reserva, con excepción para veleros, para entender el importe final.

**Criterios de aceptación**

- Se aplica una tasa de combustible de 50 € por día a todos los barcos.
- Los veleros no tienen tasa de combustible.
- La tasa se calcula correctamente en función del rango de fechas de la reserva.
- El importe total incluye la tasa de combustible (excepto para veleros).
- El cliente ve desglosado el importe base y la tasa en el resumen de la reserva.

### HU-12 — Correo de confirmación con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi pedido.

**Criterios de aceptación**

- Se envía un correo electrónico tras confirmar la reserva.
- El correo incluye los datos del barco reservado.
- El correo incluye el rango de fechas de la reserva.
- El correo incluye el importe total.
- El correo incluye un código de seguimiento único.
- El código de seguimiento permite consultar el estado sin estar registrado.

### HU-14 — Consulta de estado de reserva por código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente no registrado, quiero consultar el estado de mi reserva usando el código de seguimiento recibido por correo, para saber el progreso de mi pedido.

**Criterios de aceptación**

- Existe una página de consulta de estado accesible sin autenticación.
- El cliente introduce el código de seguimiento.
- El sistema devuelve el estado actual de la reserva.
- Se muestra el estado, los datos del barco, las fechas y el importe.
- Si el código no existe, se muestra un mensaje de error.

### HU-19 — Inicio de sesión durante el proceso de reserva

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero iniciar sesión durante el proceso de reserva manteniendo la cesta, para no perder mis selecciones.

**Criterios de aceptación**

- El cliente puede acceder a un formulario de login durante el proceso de reserva.
- La cesta se mantiene tras iniciar sesión.
- El cliente queda autenticado y puede continuar con la reserva.
- Los datos de la cesta se asocian a la cuenta del cliente.

### HU-20 — Reserva sin registro previo

- **Prioridad**: Baja
- **Estimación**: S

**Descripción**

Como visitante, quiero realizar una reserva sin estar registrado previamente, para acceder rápidamente al servicio.

**Criterios de aceptación**

- El visitante puede completar una reserva sin tener una cuenta.
- Se solicitan los datos de contacto durante el proceso de reserva.
- Se genera un código de seguimiento para consultar el estado.
- El visitante recibe un correo de confirmación con el código.
- El visitante puede consultar el estado usando el código sin registrarse.
