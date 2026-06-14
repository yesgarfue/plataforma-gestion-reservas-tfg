---
run_id: run_2026-05-17_18-49
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-17T19:43:33+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-17_18-49`

Total de historias: **6**

## Historias del sprint

### HU-08 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página, poder ampliar o reducir la cantidad de unidades de cada barco, revisar su estado y vaciarlo si es necesario.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta.
- Al entrar en modo administrador, la cesta se vacía automáticamente.

### HU-09 — Proceso de reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva sin haberme registrado previamente, proporcionando mis datos durante el proceso en no más de tres pasos.

**Criterios de aceptación**

- El cliente puede iniciar el proceso de reserva desde la cesta sin estar registrado.
- El proceso de reserva se realiza en no más de tres pasos.
- Durante el proceso se solicitan los datos del cliente (nombre, correo, teléfono, etc.) y datos de pago.
- El cliente puede completar la reserva sin registro previo.
- Si el cliente inicia sesión durante el proceso de reserva, sus datos se heredan al volver de la página de login.

### HU-10 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero poder pagar mi reserva mediante PayPal Sandbox o contra-reembolso, para elegir el método que prefiero.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- La integración de PayPal utiliza el entorno Sandbox, no producción.
- El cliente es redirigido al flujo de pago correspondiente según el método seleccionado.

### HU-11 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico de confirmación con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi reserva posteriormente.

**Criterios de aceptación**

- Al finalizar la reserva, el cliente recibe un correo electrónico de confirmación.
- El correo contiene los datos del barco, el rango de fechas, el importe total y un código de seguimiento.
- El código de seguimiento es único y permite consultar el estado de la reserva sin estar registrado.

### HU-12 — Cálculo de tarifa con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el importe total de la reserva considerando el precio diario del barco, la cantidad de días y una tasa de combustible, para mostrar el precio correcto al cliente.

**Criterios de aceptación**

- Los alquileres se miden por día.
- Se aplica una tasa de combustible de 50 euros por día para todos los barcos.
- Para barcos de categoría velero, la tasa de combustible es 0 euros.
- El importe total se calcula correctamente: (precio_diario * cantidad_dias * cantidad_barcos) + (tasa_combustible * cantidad_dias * cantidad_barcos).
- El importe total se muestra al cliente antes de confirmar la reserva.

### HU-13 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas para reflejar su ciclo de vida, permitiendo transiciones válidas entre estados.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO, implicando su eliminación del sistema.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas mediante botones por transición aplicable.
- Las transiciones de estado respetan las reglas de negocio.
