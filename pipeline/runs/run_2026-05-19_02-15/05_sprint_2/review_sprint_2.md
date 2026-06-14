---
run_id: run_2026-05-19_02-15
fase: 05_sprint_2
agente: Script
modelo: deterministico
timestamp: 2026-05-19T03:02:14+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 2 — Review automático

**ID de ejecución**: `run_2026-05-19_02-15`

## Arranque

- **Comando**: `python manage.py check`
- **OK**: `True`
- **Return code**: `0`
- **Timeout**: `False` (60s)

### stderr

```text
System check identified some issues:

WARNINGS:
?: (urls.W005) URL namespace 'admin' isn't unique. You may not be able to reverse all URLs in this namespace

System check identified 1 issue (0 silenced).
```

## Incidencias ejecutables

- Ruta /admin-panel/ no responde correctamente: .

## Rutas revisadas

| Ruta | Ejecutada | OK | Status | Detalle |
|---|---:|---:|---:|---|
| `/` | `True` | `True` | `200` | http://127.0.0.1:54201/ |
| `/barcos/` | `True` | `True` | `200` | http://127.0.0.1:54201/barcos/ |
| `/cesta/` | `True` | `True` | `200` | http://127.0.0.1:54201/cesta/ |
| `/accounts/registro/` | `True` | `True` | `200` | http://127.0.0.1:54201/accounts/registro/ |
| `/accounts/login/` | `True` | `True` | `200` | http://127.0.0.1:54201/accounts/login/ |
| `/reserva/paso1/` | `True` | `True` | `200` | http://127.0.0.1:54201/reserva/paso1/ |
| `/reserva/paso2/` | `True` | `True` | `302` | /reserva/paso1/ |
| `/reserva/paso3/` | `True` | `True` | `302` | /reserva/paso1/ |
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
| `catalog/home.html` | `True` | `True` |  |
| `catalog/list.html` | `True` | `True` |  |
| `payments/cash_on_delivery.html` | `True` | `True` |  |
| `payments/email_pago_confirmado.html` | `True` | `True` |  |
| `reservations/confirmation.html` | `True` | `True` |  |
| `reservations/email_confirmacion.html` | `True` | `True` |  |
| `reservations/email_recordatorio.html` | `True` | `True` |  |
| `reservations/my_reservations.html` | `True` | `True` |  |
| `reservations/step1.html` | `True` | `True` |  |
| `reservations/step2.html` | `True` | `True` |  |
| `reservations/step3.html` | `True` | `True` |  |
| `reservations/tracking.html` | `True` | `True` |  |
| `reservations/tracking_detail.html` | `True` | `True` |  |

## Cumplimiento por historia

| Historia | Estado |
|---|---|
| `HU-07` | `ok` |
| `HU-08` | `ok` |
| `HU-09` | `ok` |
| `HU-10` | `ok` |
| `HU-11` | `ok` |
| `HU-12` | `ok` |
| `HU-14` | `ok` |

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
- `payments/__init__.py`
- `payments/apps.py`
- `payments/forms.py`
- `payments/migrations/0001_initial.py`
- `payments/migrations/__init__.py`
- `payments/models.py`
- `payments/services/__init__.py`
- `payments/services/cash_on_delivery.py`
- `payments/services/paypal.py`
- `payments/urls.py`
- `payments/views.py`
- `README.md`
- `requirements.txt`
- `reservations/__init__.py`
- `reservations/apps.py`
- `reservations/forms.py`
- `reservations/migrations/0001_initial.py`
- `reservations/migrations/__init__.py`
- `reservations/models.py`
- `reservations/services/__init__.py`
- `reservations/services/pricing.py`
- `reservations/services/tracking.py`
- `reservations/urls.py`
- `reservations/views.py`
- `static/.gitkeep`
- `templates/.gitkeep`
- `templates/accounts/login.html`
- `templates/accounts/profile.html`
- `templates/accounts/register.html`
- `templates/base.html`
- `templates/cart/view.html`
- `templates/catalog/detail.html`
- `templates/catalog/home.html`
- `templates/catalog/list.html`
- `templates/payments/cash_on_delivery.html`
- `templates/payments/email_pago_confirmado.html`
- `templates/reservations/confirmation.html`
- `templates/reservations/email_confirmacion.html`
- `templates/reservations/email_recordatorio.html`
- `templates/reservations/my_reservations.html`
- `templates/reservations/step1.html`
- `templates/reservations/step2.html`
- `templates/reservations/step3.html`
- `templates/reservations/tracking.html`
- `templates/reservations/tracking_detail.html`
