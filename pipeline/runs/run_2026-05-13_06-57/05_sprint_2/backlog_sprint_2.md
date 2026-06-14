---
run_id: run_2026-05-13_06-57
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-13T07:11:55+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-13_06-57`

Total de historias: **7**

## Historias del sprint

### HU-04 — Reserva sin registro previo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero poder reservar un barco sin registrarme previamente, para agilizar el proceso de alquiler.

**Criterios de aceptación**

- El proceso de reserva permite continuar sin estar registrado.
- El cliente puede proporcionar sus datos de contacto durante el proceso de reserva.
- Si el cliente inicia sesión durante el proceso, la cesta se recupera y se continúa con el proceso.

### HU-09 — Cesta visible e interactiva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible e interactiva desde cualquier página de la aplicación, para gestionar mis selecciones fácilmente.

**Criterios de aceptación**

- La cesta es visible en todas las páginas de la aplicación.
- El cliente puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El cliente puede vaciar la cesta completamente.
- La cesta del administrador se vacía automáticamente al entrar como admin y no permite añadir productos.

### HU-10 — Proceso de reserva en tres pasos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar el proceso de reserva en tres pasos sin exigir registro previo, para alquilar un barco de forma rápida.

**Criterios de aceptación**

- El proceso de reserva consta de tres pasos claramente definidos.
- El cliente puede completar la reserva sin estar registrado.
- Los datos de la reserva se validan correctamente en cada paso.
- El cliente puede navegar entre pasos o cancelar el proceso.

### HU-11 — Métodos de pago

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago (PayPal Sandbox y contra-reembolso) para completar mi reserva.

**Criterios de aceptación**

- Se presentan dos opciones de pago: PayPal Sandbox y contra-reembolso.
- El cliente puede seleccionar uno de los métodos.
- El flujo de pago se adapta según el método seleccionado.
- El pago se procesa correctamente en ambos casos.

### HU-12 — Cálculo de tasa de combustible

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día en el cálculo del alquiler, excepto para los barcos en la categoría 'velero'.

**Criterios de aceptación**

- La tasa de combustible se calcula como 50 € por día.
- Los barcos en la categoría 'velero' no incluyen tasa de combustible.
- El total del alquiler incluye la tasa de combustible calculada correctamente.
- El cliente ve el desglose de costos en el resumen de la reserva.

### HU-13 — Confirmación de reserva por correo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico con los datos de mi reserva, incluyendo el código de seguimiento, para tener constancia de mi alquiler.

**Criterios de aceptación**

- Se envía un correo electrónico tras completar la reserva.
- El correo incluye los datos del barco, el rango de fechas y la información total del alquiler.
- El correo incluye el código de seguimiento único.
- El correo se envía a la dirección de correo proporcionada por el cliente.

### HU-14 — Estados de reserva

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero gestionar los estados de las reservas (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO) para controlar el ciclo de vida de cada alquiler.

**Criterios de aceptación**

- Las reservas tienen cuatro estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO.
- El estado inicial de una reserva es PENDIENTE DE PAGO.
- El estado se actualiza correctamente según el flujo de la reserva.
- El administrador puede cambiar el estado de una reserva desde el panel.
