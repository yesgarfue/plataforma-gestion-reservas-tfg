---
run_id: run_2026-05-14_16-53
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T17:07:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-14_16-53`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer la base de la aplicación con autenticación, catálogo navegable y ficha de barco. El usuario puede registrarse, iniciar sesión, explorar barcos con filtros y ver detalles de cada barco.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-21`
- `HU-22`

**Entregable verificable**: Un visitante puede registrarse, iniciar sesión, navegar el catálogo de barcos con filtros combinables (puerto, fabricante, precio, categoría, capacidad, fechas), acceder a la ficha de un barco y ver todos sus datos. La interfaz está completamente en español con zona horaria Europe/Madrid. La aplicación arranca con datos precargados (5 barcos, 2 puertos, 2 fabricantes, 2 categorías incluyendo velero, 1 admin y 1 cliente de prueba).

## Sprint 2

**Objetivo**: Implementar el flujo completo de cesta y reserva con dos métodos de pago, cálculo de tasa de combustible y confirmación por correo con código de seguimiento.

**Historias asignadas**

- `HU-06`
- `HU-07`
- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-20`

**Entregable verificable**: Un cliente puede añadir barcos a la cesta desde la ficha, modificar cantidades, iniciar sesión durante el proceso de reserva, completar una reserva en máximo 3 pasos sin registro previo, elegir entre PayPal Sandbox y contra-reembolso, recibir un correo con código de seguimiento, y ver el importe total con tasa de combustible aplicada (50€/día excepto veleros).

## Sprint 3

**Objetivo**: Cerrar funcionalidades de seguimiento, cancelación, gestión administrativa y pulido. El cliente puede consultar reservas, cancelarlas si están pendientes, y el administrador gestiona barcos, clientes y estados de reservas.

**Historias asignadas**

- `HU-12`
- `HU-13`
- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`

**Entregable verificable**: Un cliente puede cancelar reservas en estado PENDIENTE DE PAGO, consultar el estado de sus reservas por código de seguimiento o desde su cuenta, y recibe recordatorios por correo. Un administrador puede gestionar barcos (alta, edición, baja), clientes (consultar, eliminar respetando restricción de reservas pendientes), cambiar estados de reservas mediante transiciones válidas, y acceder a paneles de administración completos.
