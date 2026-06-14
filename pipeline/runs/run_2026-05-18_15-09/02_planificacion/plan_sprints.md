---
run_id: run_2026-05-18_15-09
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-18T15:29:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Plan de sprints

**ID de ejecución**: `run_2026-05-18_15-09`

Número de sprints: **3**

## Sprint 1

**Objetivo**: Establecer el camino crítico mínimo del proyecto: infraestructura base, autenticación de usuarios, catálogo navegable y ficha de barco. Este sprint entrega un PMV demoable donde el cliente puede explorar barcos, ver detalles y preparar la cesta, sentando las bases para el flujo de reserva en sprints posteriores.

**Historias asignadas**

- `HU-01`
- `HU-02`
- `HU-03`
- `HU-04`
- `HU-05`
- `HU-06`
- `HU-20`
- `HU-21`

**Entregable verificable**: **Funcionalidad operativa:** Registro e inicio de sesión de clientes, catálogo de barcos organizado por categorías con búsqueda y filtros combinables (puerto, fabricante, precio, categoría, capacidad, fechas), ficha de barco con visualización de datos e imagen, zona horaria Europe/Madrid y locale español configurados, datos precargados (5 barcos, 2 puertos, 2 fabricantes, 2 categorías incluyendo velero, usuarios de prueba). **Dependencias desbloqueadas:** Modelo de datos de barcos, usuarios y categorías completamente funcional; autenticación lista para heredar datos en reserva; catálogo filtrable listo para integrar cesta y reserva. **Checks mínimos:** manage.py check sin errores, seed_data ejecutable y cargado, rutas de registro/login/logout accesibles, catálogo visible con al menos 5 barcos, filtros funcionan independientemente, ficha de barco accesible desde catálogo, zona horaria y locale correctos en fechas mostradas. **Riesgo principal:** Si los filtros combinables no se implementan correctamente, el cliente no podrá navegar eficientemente el catálogo en sprints posteriores; si el modelo de datos es incompleto, la cesta y reserva fallarán.

## Sprint 2

**Objetivo**: Implementar el flujo completo de compra: cesta persistente, proceso de reserva en tres pasos sin registro previo, métodos de pago (PayPal Sandbox y contra-reembolso), cálculo de tasa de combustible, generación de código de seguimiento y confirmación por correo. Este sprint cierra el ciclo de venta y desbloquea la gestión de estados y seguimiento en el sprint final.

**Historias asignadas**

- `HU-07`
- `HU-08`
- `HU-09`
- `HU-10`
- `HU-11`
- `HU-12`

**Entregable verificable**: **Funcionalidad operativa:** Cesta visible y modificable desde cualquier página, proceso de reserva en máximo 3 pasos sin exigir registro previo, heredanza de datos si hay sesión iniciada, selección de método de pago (PayPal Sandbox y contra-reembolso), cálculo automático de tasa de combustible (50€/día excepto veleros), generación de código de seguimiento único, envío de correo de confirmación con datos de reserva e importe total, estados de reserva (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO) implementados. **Dependencias desbloqueadas:** Modelo de reserva completamente funcional; integración de PayPal Sandbox operativa; sistema de correos configurado; códigos de seguimiento generados y únicos; estados de reserva listos para transiciones administrativas en sprint 3. **Checks mínimos:** Cesta persiste al navegar, proceso de reserva completable en 3 pasos máximo, cliente no registrado puede reservar, datos heredados correctamente si hay sesión, PayPal Sandbox integrado (aunque sea en modo sandbox), contra-reembolso seleccionable, correo de confirmación enviado con código de seguimiento, tasa de combustible calculada correctamente (50€ para no-veleros, 0€ para veleros), importe total mostrado antes de confirmar. **Riesgo principal:** PayPal Sandbox puede no estar disponible durante desarrollo o demo; mitigación: contra-reembolso debe estar completamente funcional como alternativa. Si el cálculo de tasa de combustible falla, el importe será incorrecto y afectará todas las reservas.

## Sprint 3

**Objetivo**: Cerrar funcionalidades de seguimiento, gestión administrativa y pulido: cancelación de reservas, consulta por código de seguimiento, panel administrativo completo (barcos, clientes, reservas), recordatorio de pago pendiente. Este sprint entrega un producto completo y operativo con todas las capacidades de administración y seguimiento.

**Historias asignadas**

- `HU-13`
- `HU-14`
- `HU-15`
- `HU-16`
- `HU-17`
- `HU-18`
- `HU-19`

**Entregable verificable**: **Funcionalidad operativa:** Cancelación de reservas en estado PENDIENTE DE PAGO, consulta de reserva por código de seguimiento sin necesidad de registro, consulta de reservas del cliente autenticado desde su cuenta, panel administrativo con gestión de barcos (alta, edición, baja), gestión de clientes (consulta y eliminación con restricción de reservas pendientes), gestión de reservas (consulta y cambio de estado mediante transiciones aplicables), envío automático de correo de recordatorio cuando falta un día para inicio de reserva en estado PENDIENTE DE PAGO. **Dependencias desbloqueadas:** Sistema de seguimiento completamente operativo; panel administrativo funcional; todas las transiciones de estado de reserva implementadas; sistema de correos de recordatorio automático. **Checks mínimos:** Cancelación de reserva PENDIENTE DE PAGO elimina la reserva del sistema, consulta por código de seguimiento accesible sin login, cliente autenticado ve sus reservas con detalles, panel administrativo accesible solo para administrador, CRUD de barcos funcional, eliminación de cliente bloqueada si tiene reservas pendientes, cambio de estado de reserva mediante botones de transición, correo de recordatorio enviado automáticamente 1 día antes del inicio. **Riesgo principal:** El sistema de correos automáticos (recordatorio) depende de SMTP configurado correctamente; si falla, los recordatorios no se enviarán. Las transiciones de estado de reserva deben validarse correctamente para evitar estados inconsistentes. Si la restricción de eliminación de clientes con reservas pendientes no se implementa, se pueden perder datos de auditoría.
