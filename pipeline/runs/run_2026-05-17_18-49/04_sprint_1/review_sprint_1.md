---
run_id: run_2026-05-17_18-49
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-17T19:50:47+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Review automático

**ID de ejecución**: `run_2026-05-17_18-49`

## Arranque

- **Comando**: `python manage.py check`
- **OK**: `True`
- **Return code**: `0`
- **Timeout**: `False` (60s)

### stderr

```text
System check identified some issues:

WARNINGS:
?: (urls.W005) URL namespace 'reservations' isn't unique. You may not be able to reverse all URLs in this namespace

System check identified 1 issue (0 silenced).
```

## Incidencias ejecutables

- Ruta /admin-panel/ no responde correctamente: .

## Rutas revisadas

| Ruta | Ejecutada | OK | Status | Detalle |
|---|---:|---:|---:|---|
| `/` | `True` | `True` | `200` | http://127.0.0.1:52023/ |
| `/barcos/` | `True` | `True` | `200` | http://127.0.0.1:52023/barcos/ |
| `/cesta/` | `True` | `True` | `200` | http://127.0.0.1:52023/cesta/ |
| `/accounts/registro/` | `True` | `True` | `200` | http://127.0.0.1:52023/accounts/registro/ |
| `/accounts/login/` | `True` | `True` | `200` | http://127.0.0.1:52023/accounts/login/ |
| `/reserva/paso1/` | `True` | `True` | `200` | http://127.0.0.1:52023/reserva/paso1/ |
| `/admin/` | `True` | `True` | `302` | /admin/login/?next=/admin/ |
| `/admin-panel/` | `True` | `False` | `404` |  |

## Templates revisadas

| Template | Ejecutada | OK | Detalle |
|---|---:|---:|---|
| `accounts/account.html` | `True` | `True` |  |
| `accounts/login.html` | `True` | `True` |  |
| `accounts/register.html` | `True` | `True` |  |
| `base.html` | `True` | `True` |  |
| `cart/view.html` | `True` | `True` |  |
| `catalog/detail.html` | `True` | `True` |  |
| `catalog/list.html` | `True` | `True` |  |
| `home.html` | `True` | `True` |  |
| `reservations/confirmation.html` | `True` | `True` |  |
| `reservations/my_reservations.html` | `True` | `True` |  |
| `reservations/step1.html` | `True` | `True` |  |
| `reservations/step2.html` | `True` | `True` |  |
| `reservations/step3.html` | `True` | `True` |  |
| `reservations/tracking.html` | `True` | `True` |  |

## Cumplimiento por historia

| Historia | Estado |
|---|---|
| `HU-01` | `ok` |
| `HU-02` | `ok` |
| `HU-03` | `ok` |
| `HU-04` | `ok` |
| `HU-05` | `ok` |
| `HU-06` | `ok` |
| `HU-07` | `ok` |
| `HU-21` | `ok` |
| `HU-22` | `ok` |

## Archivos inspeccionados

- `.gitignore`
- `accounts/__init__.py`
- `accounts/apps.py`
- `accounts/forms.py`
- `accounts/migrations/0001_initial.py`
- `accounts/migrations/__init__.py`
- `accounts/models.py`
- `accounts/urls.py`
- `accounts/views.py`
- `admin_panel/__init__.py`
- `admin_panel/apps.py`
- `admin_panel/urls.py`
- `cart/__init__.py`
- `cart/apps.py`
- `cart/migrations/0001_initial.py`
- `cart/migrations/__init__.py`
- `cart/services.py`
- `cart/urls.py`
- `cart/views.py`
- `catalog/__init__.py`
- `catalog/apps.py`
- `catalog/migrations/0001_initial.py`
- `catalog/migrations/__init__.py`
- `catalog/models.py`
- `catalog/urls.py`
- `catalog/views.py`
- `core/__init__.py`
- `core/apps.py`
- `core/management/__init__.py`
- `core/management/commands/__init__.py`
- `core/management/commands/seed_data.py`
- `Dockerfile`
- `hundidos/__init__.py`
- `hundidos/asgi.py`
- `hundidos/settings.py`
- `hundidos/urls.py`
- `hundidos/wsgi.py`
- `manage.py`
- `README.md`
- `requirements.txt`
- `reservations/__init__.py`
- `reservations/apps.py`
- `reservations/forms.py`
- `reservations/migrations/0001_initial.py`
- `reservations/migrations/__init__.py`
- `reservations/models.py`
- `reservations/urls.py`
- `reservations/views.py`
- `templates/accounts/account.html`
- `templates/accounts/login.html`
- `templates/accounts/register.html`
- `templates/base.html`
- `templates/cart/view.html`
- `templates/catalog/detail.html`
- `templates/catalog/list.html`
- `templates/home.html`
- `templates/reservations/confirmation.html`
- `templates/reservations/my_reservations.html`
- `templates/reservations/step1.html`
- `templates/reservations/step2.html`
- `templates/reservations/step3.html`
- `templates/reservations/tracking.html`
