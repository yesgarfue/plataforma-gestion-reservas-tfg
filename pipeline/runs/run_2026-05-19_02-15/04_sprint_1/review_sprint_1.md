---
run_id: run_2026-05-19_02-15
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-19T03:00:05+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Review automático

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

- Ruta /reserva/paso1/ no responde correctamente: System check identified some issues:<br><br>WARNINGS:<br>?: (urls.W005) URL namespace 'admin' isn't unique. You may not be able to reverse all URLs in this namespace<br><br>System check identified 1 issue (0 silenced).<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET /barcos/ HTTP/1.1" 200 12869<br>[19/May/2026 03:00:04] "GET /cesta/ HTTP/1.1" 200 4324<br>[19/May/2026 03:00:04] "GET /accounts/registro/ HTTP/1.1" 200 5974<br>[19/May/2026 03:00:04] "GET /accounts/login/ HTTP/1.1" 200 5535<br>Internal Server Error: /reserva/paso1/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:04] "GET /reserva/paso1/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso2/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso2/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso3/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso3/ HTTP/1.1" 500 66821<br>[19/May/2026 03:00:05] "GET /admin/ HTTP/1.1" 302 0<br>Not Found: /admin-panel/<br>[19/May/2026 03:00:05] "GET /admin-panel/ HTTP/1.1" 404 2902.
- Ruta /reserva/paso2/ no responde correctamente: System check identified some issues:<br><br>WARNINGS:<br>?: (urls.W005) URL namespace 'admin' isn't unique. You may not be able to reverse all URLs in this namespace<br><br>System check identified 1 issue (0 silenced).<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET /barcos/ HTTP/1.1" 200 12869<br>[19/May/2026 03:00:04] "GET /cesta/ HTTP/1.1" 200 4324<br>[19/May/2026 03:00:04] "GET /accounts/registro/ HTTP/1.1" 200 5974<br>[19/May/2026 03:00:04] "GET /accounts/login/ HTTP/1.1" 200 5535<br>Internal Server Error: /reserva/paso1/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:04] "GET /reserva/paso1/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso2/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso2/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso3/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso3/ HTTP/1.1" 500 66821<br>[19/May/2026 03:00:05] "GET /admin/ HTTP/1.1" 302 0<br>Not Found: /admin-panel/<br>[19/May/2026 03:00:05] "GET /admin-panel/ HTTP/1.1" 404 2902.
- Ruta /reserva/paso3/ no responde correctamente: System check identified some issues:<br><br>WARNINGS:<br>?: (urls.W005) URL namespace 'admin' isn't unique. You may not be able to reverse all URLs in this namespace<br><br>System check identified 1 issue (0 silenced).<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET /barcos/ HTTP/1.1" 200 12869<br>[19/May/2026 03:00:04] "GET /cesta/ HTTP/1.1" 200 4324<br>[19/May/2026 03:00:04] "GET /accounts/registro/ HTTP/1.1" 200 5974<br>[19/May/2026 03:00:04] "GET /accounts/login/ HTTP/1.1" 200 5535<br>Internal Server Error: /reserva/paso1/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:04] "GET /reserva/paso1/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso2/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso2/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso3/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso3/ HTTP/1.1" 500 66821<br>[19/May/2026 03:00:05] "GET /admin/ HTTP/1.1" 302 0<br>Not Found: /admin-panel/<br>[19/May/2026 03:00:05] "GET /admin-panel/ HTTP/1.1" 404 2902.
- Ruta /admin-panel/ no responde correctamente: .

## Rutas revisadas

| Ruta | Ejecutada | OK | Status | Detalle |
|---|---:|---:|---:|---|
| `/` | `True` | `True` | `200` | http://127.0.0.1:53996/ |
| `/barcos/` | `True` | `True` | `200` | http://127.0.0.1:53996/barcos/ |
| `/cesta/` | `True` | `True` | `200` | http://127.0.0.1:53996/cesta/ |
| `/accounts/registro/` | `True` | `True` | `200` | http://127.0.0.1:53996/accounts/registro/ |
| `/accounts/login/` | `True` | `True` | `200` | http://127.0.0.1:53996/accounts/login/ |
| `/reserva/paso1/` | `True` | `False` | `500` | System check identified some issues:<br><br>WARNINGS:<br>?: (urls.W005) URL namespace 'admin' isn't unique. You may not be able to reverse all URLs in this namespace<br><br>System check identified 1 issue (0 silenced).<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET /barcos/ HTTP/1.1" 200 12869<br>[19/May/2026 03:00:04] "GET /cesta/ HTTP/1.1" 200 4324<br>[19/May/2026 03:00:04] "GET /accounts/registro/ HTTP/1.1" 200 5974<br>[19/May/2026 03:00:04] "GET /accounts/login/ HTTP/1.1" 200 5535<br>Internal Server Error: /reserva/paso1/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:04] "GET /reserva/paso1/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso2/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso2/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso3/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso3/ HTTP/1.1" 500 66821<br>[19/May/2026 03:00:05] "GET /admin/ HTTP/1.1" 302 0<br>Not Found: /admin-panel/<br>[19/May/2026 03:00:05] "GET /admin-panel/ HTTP/1.1" 404 2902 |
| `/reserva/paso2/` | `True` | `False` | `500` | System check identified some issues:<br><br>WARNINGS:<br>?: (urls.W005) URL namespace 'admin' isn't unique. You may not be able to reverse all URLs in this namespace<br><br>System check identified 1 issue (0 silenced).<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET /barcos/ HTTP/1.1" 200 12869<br>[19/May/2026 03:00:04] "GET /cesta/ HTTP/1.1" 200 4324<br>[19/May/2026 03:00:04] "GET /accounts/registro/ HTTP/1.1" 200 5974<br>[19/May/2026 03:00:04] "GET /accounts/login/ HTTP/1.1" 200 5535<br>Internal Server Error: /reserva/paso1/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:04] "GET /reserva/paso1/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso2/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso2/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso3/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso3/ HTTP/1.1" 500 66821<br>[19/May/2026 03:00:05] "GET /admin/ HTTP/1.1" 302 0<br>Not Found: /admin-panel/<br>[19/May/2026 03:00:05] "GET /admin-panel/ HTTP/1.1" 404 2902 |
| `/reserva/paso3/` | `True` | `False` | `500` | System check identified some issues:<br><br>WARNINGS:<br>?: (urls.W005) URL namespace 'admin' isn't unique. You may not be able to reverse all URLs in this namespace<br><br>System check identified 1 issue (0 silenced).<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET / HTTP/1.1" 200 14283<br>[19/May/2026 03:00:03] "GET /barcos/ HTTP/1.1" 200 12869<br>[19/May/2026 03:00:04] "GET /cesta/ HTTP/1.1" 200 4324<br>[19/May/2026 03:00:04] "GET /accounts/registro/ HTTP/1.1" 200 5974<br>[19/May/2026 03:00:04] "GET /accounts/login/ HTTP/1.1" 200 5535<br>Internal Server Error: /reserva/paso1/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:04] "GET /reserva/paso1/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso2/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso2/ HTTP/1.1" 500 66821<br>Internal Server Error: /reserva/paso3/<br>Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\exception.py", line 47, in inner<br>    response = get_response(request)<br>               ^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 188, in _get_response<br>    self.check_response(response, callback)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\handlers\base.py", line 309, in check_response<br>    raise ValueError(<br>ValueError: The view reservations.urls.<lambda> didn't return an HttpResponse object. It returned None instead.<br>[19/May/2026 03:00:05] "GET /reserva/paso3/ HTTP/1.1" 500 66821<br>[19/May/2026 03:00:05] "GET /admin/ HTTP/1.1" 302 0<br>Not Found: /admin-panel/<br>[19/May/2026 03:00:05] "GET /admin-panel/ HTTP/1.1" 404 2902 |
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

## Cumplimiento por historia

| Historia | Estado |
|---|---|
| `HU-01` | `ok` |
| `HU-02` | `ok` |
| `HU-03` | `ok` |
| `HU-04` | `ok` |
| `HU-05` | `ok` |
| `HU-06` | `ok` |
| `HU-21` | `ok` |
| `HU-22` | `ok` |
| `HU-23` | `ok` |

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
- `payments/migrations/0001_initial.py`
- `payments/migrations/__init__.py`
- `payments/models.py`
- `payments/urls.py`
- `README.md`
- `requirements.txt`
- `reservations/__init__.py`
- `reservations/apps.py`
- `reservations/migrations/0001_initial.py`
- `reservations/migrations/__init__.py`
- `reservations/models.py`
- `reservations/urls.py`
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
