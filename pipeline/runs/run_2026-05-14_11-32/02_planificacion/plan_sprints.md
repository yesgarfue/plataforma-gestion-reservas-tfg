---
run_id: run_2026-05-14_11-32
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T11:41:59+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-14_11-32`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer el camino crítico mínimo: autenticación, catálogo de barcos con filtros, ficha de barco y cesta. Es el PMV demoable.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-16`
- `HU-17`

**Entregable verificable**: El cliente puede registrarse, iniciar sesión, cerrar sesión, navegar el catálogo con filtros combinables, ver la ficha de un barco, seleccionar cantidad y añadir a la cesta. La cesta es visible desde cualquier página. La aplicación está configurada en zona horaria Europe/Madrid, locale español, y arranca con datos precargados en Docker.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva, métodos de pago, confirmación con código de seguimiento y cálculo de tasa de combustible.

**Historias asignadas**

- `HU-07`
- `HU-08`
- `HU-09`
- `HU-10`

**Entregable verificable**: El cliente puede completar una reserva en tres pasos sin registro previo, elegir entre PayPal Sandbox y contra-reembolso, recibir confirmación por correo con código de seguimiento, y la tasa de combustible se calcula correctamente (50 € por día, excepto veleros con 0 €).

## Sprint 3

**Objetivo**: Cerrar estados de reserva, cancelaciones, seguimiento, gestión administrativa completa y pulido final.

**Historias asignadas**

- `HU-11`
- `HU-12`
- `HU-13`
- `HU-14`
- `HU-15`

**Entregable verificable**: El cliente puede consultar el estado de sus reservas por código de seguimiento o desde su cuenta, cancelar reservas en estado PENDIENTE DE PAGO. El administrador puede gestionar barcos, clientes y reservas desde el panel de administración, cambiar estados de reservas, y el sistema envía recordatorios de reservas pendientes.
