---
gate: 2
fase: 02_planificacion
decision: aceptado
timestamp_revision_inicio: 2026-05-18T16:52:09+02:00
timestamp_revision_fin: 2026-05-18T17:14:09+02:00
---

## Observaciones

Artefactos revisados: `backlog.md`, `plan_sprints.json` y `riesgos.json`.

- El backlog contiene 25 historias de usuario y cubre de forma amplia las áreas principales del brief.

- Sprint 1 concentra demasiadas historias y varias de ellas son técnicamente pesadas: filtros combinables, cesta, seguridad, seed data y Docker. Aunque tiene sentido construir la base del sistema al inicio, el sprint queda más cargado que Sprint 2 y Sprint 3. Esta observación no bloquea el avance, pero debe vigilarse para evitar que Sprint 1 se convierta en un cuello de botella.

Observaciones no bloqueantes:

- El Sprint 2 menciona en su entregable la consulta de reserva por código de seguimiento, pero la HU-16 está asignada al Sprint 3. Debe corregirse la redacción del Sprint 2 o mover HU-16 si se quiere que esa consulta forme parte del flujo completo de reserva.
- HU-12 contiene una formulación algo ambigua: primero dice que la tasa de 50 € 
- R-08 menciona imágenes base externas como `postgres o similar`, pero el brief exige SQLite. Debe evitarse introducir PostgreSQL como dependencia o expectativa del sistema.
- Algunas mitigaciones de riesgos son exigentes para un PMV, como pruebas de carga o auditorías de dependencias. Son útiles como alerta, pero no deben convertirse en condiciones obligatorias si bloquean el avance del pipeline.

Se acepta con observaciones porque el backlog es suficientemente completo, el plan respeta las tres iteraciones esperadas, el reparto es razonable y los riesgos identificados ayudan a proteger el desarrollo. Las observaciones deben revisarse especialmente en Gate 3 para asegurar que arquitectura concreta modelos, migraciones, rutas, seed data, Docker, README y límites técnicos de SQLite.

## Acción

Ninguna.