---
run_id: run_2026-05-15_09-52
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-15T09:58:14+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-15_09-52`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base de la aplicación con autenticación, catálogo de barcos y ficha de producto. El usuario puede registrarse, iniciar sesión y navegar el catálogo con filtros y búsqueda.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-20`
- `HU-21`

**Entregable verificable**: Un visitante puede registrarse, iniciar sesión, cerrar sesión, visualizar el catálogo de barcos con filtros combinables y búsqueda por nombre, acceder a la ficha de un barco y ver sus datos. La aplicación está configurada con zona horaria Europe/Madrid, locale español e interfaz completamente en español. Los datos de ejemplo están precargados.

## Sprint 2

**Objetivo**: Implementar el flujo completo de reserva, cesta y pago. El cliente puede añadir barcos a la cesta, completar una reserva en tres pasos sin registro previo, elegir método de pago y recibir confirmación con código de seguimiento.

**Historias asignadas**

- `HU-07`
- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`

**Entregable verificable**: Un cliente puede añadir barcos a la cesta desde la ficha, modificar cantidades, completar una reserva en tres pasos sin registro previo, seleccionar entre PayPal Sandbox y contra-reembolso, recibir un correo de confirmación con código de seguimiento, y el sistema calcula correctamente la tasa de combustible (50 € por día, excepto veleros).

## Sprint 3

**Objetivo**: Cerrar el ciclo de vida de reservas, implementar seguimiento y gestión administrativa completa. El cliente puede cancelar reservas, consultar estado por código de seguimiento, y el administrador gestiona barcos, clientes y reservas.

**Historias asignadas**

- `HU-13`
- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`

**Entregable verificable**: Un cliente puede cancelar reservas en estado PENDIENTE DE PAGO, consultar el estado de sus reservas desde su cuenta y por código de seguimiento sin estar registrado. El administrador puede gestionar barcos (alta, edición, baja), consultar y eliminar clientes respetando restricciones, consultar y cambiar estados de reservas. El sistema envía recordatorios de pago pendiente cuando falta un día para el inicio de la reserva.
