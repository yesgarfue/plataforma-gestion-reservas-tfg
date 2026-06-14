# 99 — Review final determinista

**ID de ejecucion**: `run_2026-05-13_15-33`

**Protocolo**: `validacion_final_v1`

**OK global**: `False`

**Clasificacion**: `parcial_con_incidencias`

## Resumen de checks

- Planificados: **16**
- Ejecutados: **16**
- No ejecutados: **0**

## Comandos

| Check | Ejecutado | OK | Return code | Timeout |
|---|---:|---:|---:|---:|
| `check` | `True` | `True` | `0` | `False` |
| `migrate` | `True` | `True` | `0` | `False` |
| `seed_data` | `True` | `True` | `0` | `False` |
| `runserver` | `True` | `True` | `0` | `False` |

## Migraciones

- **OK**: `True`
- Apps con modelos: accounts, catalog, reservations
- Apps sin migraciones: ninguna

## Rutas minimas

| Ruta | Ejecutada | OK | Status | Detalle |
|---|---:|---:|---:|---|
| `/` | `True` | `True` | `200` | http://127.0.0.1:53292/ |
| `/barcos/` | `True` | `True` | `200` | http://127.0.0.1:53292/barcos/ |
| `/cesta/` | `True` | `True` | `200` | http://127.0.0.1:53292/cesta/ |
| `/accounts/registro/` | `True` | `False` | `404` |  |
| `/accounts/login/` | `True` | `False` | `404` |  |
| `/reserva/paso1/` | `True` | `True` | `200` | http://127.0.0.1:53292/reserva/paso1/ |
| `/reserva/paso2/` | `True` | `True` | `200` | http://127.0.0.1:53292/reserva/paso2/ |
| `/reserva/paso3/` | `True` | `True` | `200` | http://127.0.0.1:53292/reserva/paso3/ |
| `/admin/` | `True` | `True` | `302` | /admin/login/?next=/admin/ |
| `/admin-panel/` | `True` | `True` | `302` | /login/?next=/admin-panel/ |

## Templates criticas

| Template | Ejecutada | OK | Detalle |
|---|---:|---:|---|
| `reservations/checkout_step3.html` | `True` | `True` |  |

## Incidencias

- Ruta /accounts/registro/ no supero smoke test: status 404.
- Ruta /accounts/login/ no supero smoke test: status 404.

## Factores bloqueantes

- _(sin factores bloqueantes)_

## Preparacion manual requerida

- _(no detectada)_
