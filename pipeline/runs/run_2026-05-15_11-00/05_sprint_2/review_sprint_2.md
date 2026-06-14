---
run_id: run_2026-05-15_11-00
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-15T11:18:45+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Review automático

**ID de ejecución**: `run_2026-05-15_11-00`

## Arranque

- **Comando**: `python manage.py check`
- **OK**: `True`
- **Return code**: `0`
- **Timeout**: `False` (60s)

### stdout

```text
System check identified no issues (0 silenced).
```

## Incidencias ejecutables

- Ruta /admin-panel/ no responde correctamente: .
- La navegacion visible enlaza logout por GET, pero LogoutView solo define POST.

## Rutas revisadas

| Ruta | Ejecutada | OK | Status | Detalle |
|---|---:|---:|---:|---|
| `/` | `True` | `True` | `200` | http://127.0.0.1:52540/ |
| `/barcos/` | `True` | `True` | `200` | http://127.0.0.1:52540/barcos/ |
| `/cesta/` | `True` | `True` | `200` | http://127.0.0.1:52540/cesta/ |
| `/accounts/registro/` | `True` | `True` | `200` | http://127.0.0.1:52540/accounts/registro/ |
| `/accounts/login/` | `True` | `True` | `200` | http://127.0.0.1:52540/accounts/login/ |
| `/admin/` | `True` | `True` | `302` | /admin/login/?next=/admin/ |
| `/admin-panel/` | `True` | `False` | `404` |  |

## Templates revisadas

| Template | Ejecutada | OK | Detalle |
|---|---:|---:|---|
| `accounts/login.html` | `True` | `True` |  |
| `accounts/profile.html` | `True` | `True` |  |
| `accounts/register.html` | `True` | `True` |  |
| `base.html` | `True` | `True` |  |
| `cart/view.html` | `True` | `True` |  |
| `catalog/detail.html` | `True` | `True` |  |
| `catalog/list.html` | `True` | `True` |  |
| `home.html` | `True` | `True` |  |
| `reservations/confirmation.html` | `True` | `True` |  |
| `reservations/my_reservation_detail.html` | `True` | `True` |  |
| `reservations/my_reservations.html` | `True` | `True` |  |
| `reservations/step1.html` | `True` | `True` |  |
| `reservations/step2.html` | `True` | `True` |  |
| `reservations/step3.html` | `True` | `True` |  |
| `reservations/track.html` | `True` | `True` |  |
| `reservations/track_detail.html` | `True` | `True` |  |

## Cumplimiento por historia

| Historia | Estado |
|---|---|
| `HU-09` | `ok` |
| `HU-10` | `ok` |
| `HU-11` | `ok` |
| `HU-12` | `ok` |
| `HU-13` | `ok` |
| `HU-22` | `ok` |

## Archivos inspeccionados

- `.gitkeep`
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
- `cart/models.py`
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
- `core/urls.py`
- `core/views.py`
- `hundidos/__init__.py`
- `hundidos/asgi.py`
- `hundidos/settings.py`
- `hundidos/urls.py`
- `hundidos/wsgi.py`
- `manage.py`
- `reservations/__init__.py`
- `reservations/apps.py`
- `reservations/forms.py`
- `reservations/migrations/0001_initial.py`
- `reservations/migrations/__init__.py`
- `reservations/models.py`
- `reservations/urls.py`
- `reservations/views.py`
- `templates/accounts/login.html`
- `templates/accounts/profile.html`
- `templates/accounts/register.html`
- `templates/base.html`
- `templates/cart/view.html`
- `templates/catalog/detail.html`
- `templates/catalog/list.html`
- `templates/home.html`
- `templates/reservations/confirmation.html`
- `templates/reservations/my_reservation_detail.html`
- `templates/reservations/my_reservations.html`
- `templates/reservations/step1.html`
- `templates/reservations/step2.html`
- `templates/reservations/step3.html`
- `templates/reservations/track.html`
- `templates/reservations/track_detail.html`
