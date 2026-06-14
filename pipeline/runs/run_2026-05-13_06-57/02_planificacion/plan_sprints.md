---
run_id: run_2026-05-13_06-57
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-13T07:09:29+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-13_06-57`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base técnica de la aplicación con autenticación, catálogo navegable y ficha de barco. Demostrar un PMV funcional donde el cliente puede registrarse, explorar barcos y ver detalles.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-05`
- `HU-06`
- `HU-07`
- `HU-08`
- `HU-22`
- `HU-23`
- `HU-24`

**Entregable verificable**: La aplicación se ejecuta en Docker, el cliente puede registrarse e iniciar sesión, navegar el catálogo de barcos por categorías, buscar por nombre, aplicar filtros combinables, ver la ficha detallada de un barco, y la interfaz está completamente en español con zona horaria Europe/Madrid.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva y pago, incluyendo cesta interactiva, proceso de reserva en tres pasos, cálculo de costos con tasa de combustible, y confirmación por correo con código de seguimiento.

**Historias asignadas**

- `HU-04`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`
- `HU-14`

**Entregable verificable**: El cliente puede añadir barcos a la cesta, modificar cantidades, completar un proceso de reserva en tres pasos sin registrarse, elegir entre PayPal Sandbox y contra-reembolso, recibir confirmación por correo con código de seguimiento, y ver el cálculo correcto de la tasa de combustible (50 € por día, excepto veleros).

## Sprint 3

**Objetivo**: Cerrar funcionalidades de seguimiento, cancelación, gestión administrativa y pulido. Permitir consulta de reservas, cancelación condicional, recordatorios automáticos y panel administrativo completo.

**Historias asignadas**

- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`
- `HU-20`
- `HU-21`

**Entregable verificable**: El cliente puede cancelar reservas en estado PENDIENTE DE PAGO, consultar reservas por código de seguimiento o desde su cuenta, el administrador puede gestionar barcos y clientes, cambiar estados de reservas, y el sistema envía recordatorios automáticos un día antes de la fecha de inicio.
