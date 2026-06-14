---
gate: 1
fase: 01_requisitos
timestamp_inicio: 2026-04-25T01:30:00+02:00
timestamp_fin: 2026-04-25T13:30:00+02:00
decision: rechazado
---

## Observaciones

El registro producido por el Analista cumple los mínimos cuantitativos
del Bloque 6 (15 RF + 3 RNF) y respeta el vocabulario literal del brief
("barco", "cliente", "puerto", "fabricante", "cesta", "código de
seguimiento", "velero"). No se detectan alucinaciones (requisitos
inventados fuera del brief).

Sin embargo, la cobertura es insuficiente. El registro deja fuera
funcionalidades centrales del brief que aparecen explícitamente en su
sección 3 y deben formar parte del alcance:

  - Estados de reserva (PAGADO, PENDIENTE DE PAGO, EN USO, DEVUELTO) y
    reglas asociadas: cancelación únicamente si está en estado
    PENDIENTE DE PAGO; recordatorio por email un día antes del inicio
    si la reserva sigue pendiente; cambio de estado por el administrador.
    (Brief, sección 3.6.)
  - Métodos de pago: PayPal Sandbox y contra-reembolso.
    (Brief, sección 3.5.)
  - Posibilidad de reservar sin registro previo, con recogida de datos
    mínimos durante el proceso, y recuperación de la cesta tras inicio
    de sesión durante la compra. (Brief, secciones 3.1 y 3.5.)
  - Vaciado de la cesta al entrar en modo administrador y prohibición
    de añadir al carro como administrador. (Brief, sección 3.4.)
  - Selección de cantidad de unidades desde la ficha del barco.
    (Brief, sección 3.3.)
  - Restricción del administrador para eliminar usuarios: solo si no
    tienen reservas pendientes. (Brief, sección 3.1.)
  - Gestión administrativa de reservas (consulta y cambio de estado).
    (Brief, sección 3.8.)
  - Marcado de barcos no disponibles en el filtro de fechas (etiqueta
    "No disponible" sin ocultarlos). (Brief, sección 3.2.)

Los RNF están además recortados al mínimo y omiten restricciones
técnicas explícitas del brief sección 4: framework Django 3.2,
base de datos SQLite, zona horaria Europe/Madrid, empaquetado en
contenedor Docker, datos seed mínimos al arranque. El RNF-03 actual
("El lenguaje es Python") es trivial y no añade valor frente a la
restricción real del stack.

El patrón observado es que el modelo se ha quedado en el umbral
cuantitativo de 15 RF + 3 RNF sin priorizar la cobertura de las
secciones 3 y 4 del brief. Esto se interpreta como efecto de un prompt
que comunica el umbral mínimo pero no el criterio de cobertura.

## Acción

Regenerar la fase 01 con un prompt ajustado en `agents.yaml` y
`tasks.yaml` que:

  1. Sustituya el umbral mínimo "15 RF y 3 RNF" por una guía de
     cobertura por secciones del brief: cada subsección de la sección 3
     (3.1 a 3.8) debe estar representada por al menos un RF, y cada
     bloque de la sección 4 (restricciones técnicas) debe estar
     representado por al menos un RNF.
  2. Incluya en el `backstory` o en la `description` de la task un
     listado explícito de las áreas funcionales a cubrir (sin
     prescribir redacciones concretas, solo áreas).
  3. Mantenga la prohibición de inventar fuera del brief, intacta.
  4. Mantenga el mínimo cuantitativo del validator (≥15 RF, ≥3 RNF) sin
     cambios en `validators.py`: no se ajusta el listón, se ajusta la
     guía al agente.

Snapshots del prompt v1 conservados en este mismo directorio
(`agents_v1.yaml`, `tasks_v1.yaml`) para trazabilidad de la mejora.