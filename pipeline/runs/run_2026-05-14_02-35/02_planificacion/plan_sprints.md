---
run_id: run_2026-05-14_02-35
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T02:43:53+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-14_02-35`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer el camino crítico mínimo: autenticación de usuarios, catálogo de barcos con filtros, ficha de barco y cesta. Crear un PMV demoable donde el cliente puede navegar y seleccionar barcos.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-20`
- `HU-21`
- `HU-22`
- `HU-23`

**Entregable verificable**: El cliente puede registrarse, iniciar sesión, cerrar sesión, navegar el catálogo con filtros combinables, acceder a la ficha de un barco, seleccionar cantidad y añadir a la cesta. La cesta es visible en todas las páginas. La interfaz está en español, la zona horaria es Europe/Madrid y los datos de ejemplo están precargados en Docker.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva y pago: proceso de reserva en tres pasos, cálculo de tarifas con tasa de combustible, integración de PayPal Sandbox y contra-reembolso, confirmación por correo con código de seguimiento.

**Historias asignadas**

- `HU-07`
- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`

**Entregable verificable**: El cliente puede completar una reserva sin registro previo en tres pasos, seleccionar método de pago (PayPal Sandbox o contra-reembolso), recibir confirmación por correo con código de seguimiento único, y el importe total se calcula correctamente incluyendo la tasa de combustible diferenciada por categoría.

## Sprint 3

**Objetivo**: Cerrar el ciclo de vida de reservas, seguimiento y gestión administrativa: cancelación de reservas, consulta de estado por código de seguimiento, panel de administración completo, recordatorios automáticos y gestión de usuarios.

**Historias asignadas**

- `HU-12`
- `HU-13`
- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`

**Entregable verificable**: El cliente puede consultar reservas por código de seguimiento sin registrarse, el usuario autenticado ve sus reservas, puede cancelar reservas en estado PENDIENTE DE PAGO, el administrador gestiona barcos, clientes y reservas desde el panel, cambia estados de reservas, y el sistema envía recordatorios automáticos de pago pendiente.
