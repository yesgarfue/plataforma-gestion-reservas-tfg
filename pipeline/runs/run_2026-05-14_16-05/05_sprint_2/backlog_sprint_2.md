---
run_id: run_2026-05-14_16-05
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-14T16:16:40+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_16-05`

Total de historias: **7**

## Historias del sprint

### HU-07 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página, poder ampliar o reducir la cantidad de unidades de cada barco, revisar su estado y vaciarlo si es necesario.

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

Como cliente, quiero completar una reserva sin haberme registrado previamente, en no más de tres pasos, proporcionando mis datos y datos de pago.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta.
- El proceso de reserva se realiza en no más de tres pasos.
- No se exige registro previo para completar una reserva.
- Durante el proceso se solicitan los datos del cliente y los datos de pago.
- Si hay sesión iniciada, los datos del cliente se heredan automáticamente.

### HU-09 — Pago mediante PayPal Sandbox

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero pagar mi reserva mediante PayPal Sandbox, para utilizar mi cuenta de PayPal de prueba.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal como método de pago durante el proceso de reserva.
- El cliente es redirigido a PayPal Sandbox para completar el pago.
- Tras completar el pago en PayPal, el cliente es redirigido a la aplicación.
- La reserva se marca como PAGADO tras un pago exitoso en PayPal.

### HU-10 — Pago mediante contra-reembolso

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero pagar mi reserva mediante contra-reembolso, para pagar al recibir el barco.

**Criterios de aceptación**

- El cliente puede seleccionar contra-reembolso como método de pago durante el proceso de reserva.
- La reserva se marca como PENDIENTE DE PAGO tras seleccionar contra-reembolso.
- El cliente recibe un correo de confirmación con los datos de la reserva y el código de seguimiento.

### HU-11 — Confirmación de reserva con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico tras finalizar la reserva con los datos del barco, el rango de fechas, el importe total y un código de seguimiento.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico.
- El correo contiene los datos del barco alquilado.
- El correo contiene el rango de fechas de la reserva.
- El correo contiene el importe total de la reserva.
- El correo contiene un código de seguimiento único para consultar el estado de la reserva.

### HU-12 — Cálculo de precio con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el precio total de la reserva considerando el precio diario del barco, el número de días y una tasa de combustible de 50 euros por día, excepto para barcos de categoría velero donde la tasa es 0 euros.

**Criterios de aceptación**

- El precio total se calcula como: (precio_diario + tasa_combustible) * número_de_días.
- La tasa de combustible es 50 euros por día para todas las categorías excepto velero.
- Para barcos de categoría velero, la tasa de combustible es 0 euros.
- El precio total se muestra al cliente antes de confirmar la reserva.

### HU-13 — Inicio de sesión durante el proceso de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero iniciar sesión durante el proceso de reserva y recuperar mi cesta al volver de la página de login, para continuar con mi compra sin perder los datos.

**Criterios de aceptación**

- El cliente puede acceder a un enlace de login durante el proceso de reserva.
- Tras iniciar sesión, el cliente es redirigido de vuelta al proceso de reserva.
- La cesta se mantiene intacta tras el login.
- Los datos del cliente se heredan automáticamente en el formulario de reserva.
