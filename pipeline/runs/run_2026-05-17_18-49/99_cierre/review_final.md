# 99 — Review final determinista

**ID de ejecucion**: `run_2026-05-17_18-49`

**Protocolo**: `validacion_final_v1`

**OK global**: `False`

**Clasificacion**: `bloqueado_arranque`

## Resumen de checks

- Planificados: **16**
- Ejecutados: **6**
- No ejecutados: **10**

### Checks no ejecutados

| Check | Motivo |
|---|---|
| `ruta:/` | runserver no arranco correctamente |
| `ruta:/barcos/` | runserver no arranco correctamente |
| `ruta:/cesta/` | runserver no arranco correctamente |
| `ruta:/accounts/registro/` | runserver no arranco correctamente |
| `ruta:/accounts/login/` | runserver no arranco correctamente |
| `ruta:/reserva/paso1/` | runserver no arranco correctamente |
| `ruta:/reserva/paso2/` | runserver no arranco correctamente |
| `ruta:/reserva/paso3/` | runserver no arranco correctamente |
| `ruta:/admin/` | runserver no arranco correctamente |
| `ruta:/admin-panel/` | runserver no arranco correctamente |

## Comandos

| Check | Ejecutado | OK | Return code | Timeout |
|---|---:|---:|---:|---:|
| `check` | `True` | `False` | `1` | `False` |
| `migrate` | `True` | `False` | `1` | `False` |
| `seed_data` | `True` | `False` | `1` | `False` |
| `runserver` | `True` | `False` | `1` | `True` |

## Migraciones

- **OK**: `True`
- Apps con modelos: catalog, reservations
- Apps sin migraciones: ninguna

## Rutas minimas

| Ruta | Ejecutada | OK | Status | Detalle |
|---|---:|---:|---:|---|
| `/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/barcos/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/cesta/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/accounts/registro/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/accounts/login/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/reserva/paso1/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/reserva/paso2/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/reserva/paso3/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/admin/` | `False` | `False` | `` | runserver no arranco correctamente |
| `/admin-panel/` | `False` | `False` | `` | runserver no arranco correctamente |

## Templates criticas

| Template | Ejecutada | OK | Detalle |
|---|---:|---:|---|
| `reservations/step3.html` | `True` | `True` |  |

## Incidencias

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

## Factores bloqueantes

- El proyecto no supera manage.py check.
- El servidor Django no arranca para smoke tests.

## Preparacion manual requerida

- El `migrate` estandar no fue correcto. No se ejecuta `migrate --run-syncdb` como correccion dentro del validador.
