---
run_id: run_2026-05-11_13-31
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-11T14:23:01+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-11_13-31`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base técnica de la aplicación con autenticación, catálogo de barcos y ficha de producto. Demostrar un PMV funcional donde el cliente puede registrarse, navegar el catálogo y ver detalles de barcos.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-05`
- `HU-06`
- `HU-07`
- `HU-08`
- `HU-21`
- `HU-22`

**Entregable verificable**: Aplicación Docker ejecutable con registro e inicio de sesión funcionales, catálogo de barcos organizado por categorías, filtrado por disponibilidad de fechas, ficha de barco con selección de cantidad, cesta visible en todas las páginas, y zona horaria/locale configurados correctamente.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva y pago, incluyendo el proceso de tres pasos sin registro previo, métodos de pago y confirmación por correo con código de seguimiento.

**Historias asignadas**

- `HU-04`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`
- `HU-13`
- `HU-14`
- `HU-15`

**Entregable verificable**: Cliente puede completar reserva en tres pasos sin registro previo, seleccionar entre PayPal Sandbox y contra-reembolso, recibir correo de confirmación con código de seguimiento, y reservas se crean con estado PENDIENTE DE PAGO o PAGADO según el método elegido.

## Sprint 3

**Objetivo**: Cerrar funcionalidades de seguimiento, cancelación y gestión administrativa completa. Pulir la aplicación para producción.

**Historias asignadas**

- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`
- `HU-20`

**Entregable verificable**: Cliente puede cancelar reservas en estado PENDIENTE DE PAGO, consultar estado de reserva por código de seguimiento sin autenticación, administrador puede gestionar barcos, clientes y reservas desde panel propio con cambio de estados, y todas las funcionalidades están integradas y pulidas.
