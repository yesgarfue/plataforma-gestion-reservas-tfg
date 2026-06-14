---
run_id: run_2026-05-12_16-48
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-12T17:03:51+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_16-48`

Total de historias: **7**

## Historias del sprint

### HU-04 — Reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero realizar una reserva sin necesidad de registrarme previamente, para agilizar el proceso de compra.

**Criterios de aceptación**

- El cliente puede completar una reserva sin tener una cuenta registrada.
- Se solicitan los datos del cliente durante el proceso de reserva.
- El cliente recibe un código de seguimiento para consultar el estado de su reserva.

### HU-08 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver, modificar y vaciar mi cesta desde cualquier página, para gestionar mis compras antes de finalizar.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Cuando el administrador entra en modo administrador, la cesta se vacía y no puede añadir artículos.

### HU-09 — Proceso de reserva en tres pasos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin exigir registro previo, para finalizar mi compra de forma rápida.

**Criterios de aceptación**

- El proceso de reserva consta de no más de tres pasos.
- Se solicitan los datos del cliente durante el proceso.
- Se solicitan los datos de pago durante el proceso.
- El cliente puede completar la reserva sin estar registrado.
- Se calcula el precio total incluyendo la tasa de combustible cuando aplique.

### HU-10 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago para completar mi reserva, para usar la opción que me resulte más conveniente.

**Criterios de aceptación**

- Se ofrecen dos métodos de pago: PayPal Sandbox y contra-reembolso.
- El cliente puede seleccionar el método de pago durante el proceso de reserva.
- El pago se procesa según el método seleccionado.
- Se valida que los datos de pago sean correctos antes de procesar.

### HU-11 — Confirmación de reserva y código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva y un código de seguimiento, para poder consultar el estado de mi pedido.

**Criterios de aceptación**

- Tras completar la reserva, se envía un correo electrónico al cliente.
- El correo contiene los datos del barco reservado, el rango de fechas y el código de seguimiento.
- El cliente recibe el código de seguimiento para consultar el estado de su reserva.
- El correo se envía de forma fiable en el entorno configurado.

### HU-12 — Cálculo de precio con tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero calcular el precio total de la reserva aplicando la tasa de combustible según la categoría del barco, para cobrar el importe correcto.

**Criterios de aceptación**

- Los alquileres se miden por día.
- Se aplica una tasa de combustible de 50 €/día para barcos que no sean de categoría 'velero'.
- Para barcos de categoría 'velero', no se aplica tasa de combustible.
- El precio total se calcula correctamente en el proceso de reserva.

### HU-13 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas para reflejar su ciclo de vida, desde la creación hasta la devolución.

**Criterios de aceptación**

- Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO.
- Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO.
- El estado de la reserva se actualiza correctamente en el sistema.
