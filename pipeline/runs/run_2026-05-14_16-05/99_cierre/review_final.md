# 99 — Review final determinista

**ID de ejecucion**: `run_2026-05-14_16-05`

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
- Apps con modelos: accounts, catalog, reservations
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
| `reservations/checkout_step3.html` | `True` | `False` | Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\runs\run_2026-05-14_16-05\99_cierre\_validacion_tmp\codigo\manage.py", line 22, in <module><br>    main()<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\runs\run_2026-05-14_16-05\99_cierre\_validacion_tmp\codigo\manage.py", line 18, in main<br>    execute_from_command_line(sys.argv)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\__init__.py", line 419, in execute_from_command_line<br>    utility.execute()<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\__init__.py", line 413, in execute<br>    self.fetch_command(subcommand).run_from_argv(self.argv)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\base.py", line 354, in run_from_argv<br>    self.execute(*args, **cmd_options)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\base.py", line 398, in execute<br>    output = self.handle(*args, **options)<br>             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\commands\shell.py", line 87, in handle<br>    exec(options['command'], globals())<br>  File "<string>", line 2, in <module><br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\template\loader.py", line 19, in get_template<br>    raise TemplateDoesNotExist(template_name, chain=chain)<br>django.template.exceptions.TemplateDoesNotExist: reservations/checkout_step3.html |

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
- Template reservations/checkout_step3.html no compila: Traceback (most recent call last):
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\runs\run_2026-05-14_16-05\99_cierre\_validacion_tmp\codigo\manage.py", line 22, in <module>
    main()
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\runs\run_2026-05-14_16-05\99_cierre\_validacion_tmp\codigo\manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\__init__.py", line 419, in execute_from_command_line
    utility.execute()
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\__init__.py", line 413, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\base.py", line 354, in run_from_argv
    self.execute(*args, **cmd_options)
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\base.py", line 398, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\commands\shell.py", line 87, in handle
    exec(options['command'], globals())
  File "<string>", line 2, in <module>
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\template\loader.py", line 19, in get_template
    raise TemplateDoesNotExist(template_name, chain=chain)
django.template.exceptions.TemplateDoesNotExist: reservations/checkout_step3.html.

## Factores bloqueantes

- El proyecto no supera manage.py check.
- El servidor Django no arranca para smoke tests.

## Preparacion manual requerida

- El `migrate` estandar no fue correcto. No se ejecuta `migrate --run-syncdb` como correccion dentro del validador.
