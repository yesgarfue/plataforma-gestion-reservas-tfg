---
gate: 2
fase: 02_planificacion
decision: aceptado
timestamp_revision_inicio: 2026-05-17T19:09:57+02:00
timestamp_revision_fin: 2026-05-17T19:26:57+02:00

---

## Observaciones

Artefactos revisados: `backlog.json`, `plan_sprints.json` y `riesgos.json`.

La planificacion es coherente con el registro de requisitos aceptado en Gate 1. El backlog contiene 22 historias de usuario y cubre las areas principales del brief: autenticacion, catalogo, filtros, ficha de barco, cesta, reserva en tres pasos, metodos de pago, confirmacion por correo, codigo de seguimiento, estados de reserva, panel de administracion, datos seed y configuracion tecnica.

El plan de sprints esta estructurado en tres iteraciones y el reparto es razonable: Sprint 1 establece base tecnica, autenticacion, catalogo, filtros y datos seed; Sprint 2 implementa cesta, reserva, pago y calculo de tarifas; Sprint 3 completa seguimiento, gestion administrativa y funcionalidades de cierre.

Los riesgos identificados son tecnicamente relevantes: PayPal Sandbox, calculo de tasa de combustible, concurrencia con SQLite, complejidad del flujo de reserva, filtros combinables, envio de correos, datos seed, version Django 3.2, Docker y dependencias entre sprints.

Observaciones no bloqueantes:

- El backlog hereda del Gate 1 una priorizacion muy concentrada en `Alta`; solo HU-14 aparece como `Media`. Esto reduce la capacidad de distinguir entre funcionalidades nucleares y complementarias.
- HU-06 mantiene filtros adicionales como categoria y capacidad, que proceden del registro de requisitos pero pueden ampliar el alcance respecto al minimo del brief. Deben vigilarse durante arquitectura y desarrollo.
- HU-09 menciona que si el cliente inicia sesion durante la reserva se heredan sus datos al volver del login, pero convendria que la arquitectura asegure tambien la conservacion de la cesta durante ese cambio de sesion.
- HU-13 mantiene estados adicionales (`EN USO`, `DEVUELTO`) ademas de `PENDIENTE DE PAGO` y `PAGADO`. No bloquea, pero debe evitarse que complique innecesariamente el flujo minimo requerido.
- Algunos riesgos proponen mitigaciones exigentes para el contexto del PMV, por ejemplo pruebas de carga o ejecucion de herramientas de seguridad. Se consideran utiles como alerta, pero no deben confundirse con criterios obligatorios de cierre del pipeline.

Decision: aceptado con observaciones porque la planificacion es completa, trazable y suficiente para pasar a arquitectura. Las observaciones deben tenerse en cuenta en Gate 3 para evitar aumento innecesario de alcance y asegurar el contrato ejecutable.

## Acción

Ninguna.

