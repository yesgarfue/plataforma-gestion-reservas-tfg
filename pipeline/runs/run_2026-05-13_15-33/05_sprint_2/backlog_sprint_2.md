---
run_id: run_2026-05-13_15-33
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-13T15:53:10+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Backlog del sprint

**ID de ejecución**: `run_2026-05-13_15-33`

Total de historias: **8**

## Historias del sprint

### HU-07 — Selección de cantidad y adición a cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero seleccionar la cantidad de unidades de un barco desde su ficha y añadirlo a la cesta, para preparar mi reserva.

**Criterios de aceptación**

- La ficha del barco muestra un campo para seleccionar cantidad.
- El cliente puede añadir el barco a la cesta con la cantidad seleccionada.
- Se muestra una confirmación de que el barco ha sido añadido a la cesta.
- La cantidad debe ser un número entero positivo.

### HU-08 — Cesta visible y modificable

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página y poder modificar las cantidades o vaciarla, para gestionar mis reservas antes de finalizar la compra.

**Criterios de aceptación**

- La cesta es visible desde cualquier página de la aplicación.
- El cliente puede ampliar y reducir la cantidad de unidades de cada barco en la cesta.
- El cliente puede revisar el estado de la cesta desde el catálogo.
- El cliente puede vaciar la cesta completamente.
- Se muestra el total de la cesta actualizado en tiempo real.

### HU-09 — Vaciado de cesta al entrar como administrador

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador, quiero que la cesta se vacíe al cambiar a modo administrador y no poder añadir barcos al carro, para evitar confusiones entre roles.

**Criterios de aceptación**

- Al cambiar a modo administrador, la cesta se vacía automáticamente.
- El administrador no puede añadir barcos a la cesta.
- Se muestra un mensaje indicando que el modo administrador no permite usar la cesta.

### HU-10 — Proceso de reserva en tres pasos sin registro previo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero completar una reserva en no más de tres pasos sin necesidad de estar registrado previamente, para agilizar el proceso de compra.

**Criterios de aceptación**

- El proceso de reserva consta de máximo tres pasos.
- El registro previo no es obligatorio para realizar una reserva.
- Se solicitan los datos del cliente (nombre, correo, teléfono) durante el proceso.
- Se solicitan los datos de pago durante el proceso.
- El cliente puede completar la reserva sin haber creado una cuenta.

### HU-11 — Métodos de pago: PayPal Sandbox y contra-reembolso

- **Prioridad**: Media
- **Estimación**: L

**Descripción**

Como cliente, quiero elegir entre dos métodos de pago (PayPal Sandbox y contra-reembolso) para completar mi reserva.

**Criterios de aceptación**

- El cliente puede seleccionar PayPal Sandbox como método de pago.
- El cliente puede seleccionar contra-reembolso como método de pago.
- La integración con PayPal Sandbox permite procesar pagos en línea.
- El método contra-reembolso registra la reserva sin procesar pago inmediato.

### HU-12 — Correo de confirmación con código de seguimiento

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero recibir un correo electrónico tras finalizar la reserva con los datos del barco, rango de fechas, importe total y código de seguimiento, para tener constancia de mi reserva.

**Criterios de aceptación**

- Al finalizar la reserva, se envía un correo electrónico al cliente.
- El correo incluye los datos del barco reservado.
- El correo incluye el rango de fechas de la reserva.
- El correo incluye el importe total.
- El correo incluye un código de seguimiento único.
- El código de seguimiento permite consultar el estado de la reserva.

### HU-13 — Tasa de combustible por día

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero aplicar una tasa de combustible de 50 € por día a cada reserva, excepto si el barco es de categoría 'velero', para reflejar los costos operativos.

**Criterios de aceptación**

- Se aplica una tasa de combustible de 50 € por día a la reserva.
- La tasa de combustible no se aplica si el barco es de categoría 'velero'.
- El importe total de la reserva incluye la tasa de combustible calculada correctamente.
- El cliente ve el desglose de costos (precio del barco + tasa de combustible) antes de confirmar.

### HU-26 — Inicio de sesión durante el proceso de reserva

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como cliente, quiero poder iniciar sesión durante el proceso de reserva, para acceder a mis datos guardados sin completar el registro.

**Criterios de aceptación**

- Durante el proceso de reserva, se ofrece la opción de iniciar sesión.
- El cliente puede ingresar sus credenciales sin abandonar el flujo de reserva.
- Tras iniciar sesión, los datos del cliente se cargan automáticamente.
- El cliente puede continuar con la reserva sin necesidad de completar el registro.
