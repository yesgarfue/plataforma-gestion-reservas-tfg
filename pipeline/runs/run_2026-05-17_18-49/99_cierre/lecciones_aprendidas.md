# Lecciones aprendidas del run

**Run**: `run_2026-05-17_18-49`

## Resultado observado

- Resultado del Flow: `completo`
- OK global de validacion final: `False`
- Clasificacion: `bloqueado_arranque`
- Checks ejecutados: `6/16`

## Incidencias de validacion final

- manage.py check no fue correcto.
- manage.py migrate --noinput no fue correcto.
- seed_data no se ejecuto correctamente o no existe.
- runserver no arranco correctamente.
- Ruta / no supero smoke test: runserver no arranco correctamente.
- Ruta /barcos/ no supero smoke test: runserver no arranco correctamente.
- Ruta /cesta/ no supero smoke test: runserver no arranco correctamente.
- Ruta /accounts/registro/ no supero smoke test: runserver no arranco correctamente.
- Ruta /accounts/login/ no supero smoke test: runserver no arranco correctamente.
- Ruta /reserva/paso1/ no supero smoke test: runserver no arranco correctamente.
- Ruta /reserva/paso2/ no supero smoke test: runserver no arranco correctamente.
- Ruta /reserva/paso3/ no supero smoke test: runserver no arranco correctamente.
- Ruta /admin/ no supero smoke test: runserver no arranco correctamente.
- Ruta /admin-panel/ no supero smoke test: runserver no arranco correctamente.

## Preparacion manual requerida

- El `migrate` estandar no fue correcto. No se ejecuta `migrate --run-syncdb` como correccion dentro del validador.

## Gates humanos

- `01_requisitos/gate_humano.md`: gate=`1`, fase=`01_requisitos`, decision=`aceptado`
- `02_planificacion/gate_humano.md`: gate=`2`, fase=`02_planificacion`, decision=`aceptado`
- `03_arquitectura/gate_humano.md`: gate=`3`, fase=`03_arquitectura`, decision=`aceptado`

## Alcance de estas lecciones

Las metricas externas del estudio, como implementation rate, pass-rate de suite comun y log estructurado de incidencias, se calculan fuera del pipeline para no mezclar generacion con evaluacion comparativa.
