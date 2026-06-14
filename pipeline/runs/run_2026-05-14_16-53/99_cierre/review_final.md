# 99 — Review final determinista

**ID de ejecucion**: `run_2026-05-14_16-53`

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
| `seed_data` | `True` | `False` | `1` | `False` |
| `runserver` | `True` | `True` | `0` | `False` |

## Migraciones

- **OK**: `True`
- Apps con modelos: accounts, catalog, reservations
- Apps sin migraciones: ninguna

## Rutas minimas

| Ruta | Ejecutada | OK | Status | Detalle |
|---|---:|---:|---:|---|
| `/` | `True` | `True` | `200` | http://127.0.0.1:62357/ |
| `/barcos/` | `True` | `True` | `200` | http://127.0.0.1:62357/barcos/ |
| `/cesta/` | `True` | `False` | `404` |  |
| `/accounts/registro/` | `True` | `True` | `200` | http://127.0.0.1:62357/accounts/registro/ |
| `/accounts/login/` | `True` | `True` | `200` | http://127.0.0.1:62357/accounts/login/ |
| `/reserva/paso1/` | `True` | `True` | `302` | /reserva/cesta/ |
| `/reserva/paso2/` | `True` | `True` | `302` | /reserva/paso1/ |
| `/reserva/paso3/` | `True` | `True` | `302` | /reserva/paso1/ |
| `/admin/` | `True` | `True` | `302` | /admin/login/?next=/admin/ |
| `/admin-panel/` | `True` | `True` | `302` | /accounts/login/?next=/admin-panel/ |

## Templates criticas

| Template | Ejecutada | OK | Detalle |
|---|---:|---:|---|
| `reservations/checkout_step3.html` | `True` | `False` | Traceback (most recent call last):<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\runs\run_2026-05-14_16-53\99_cierre\_validacion_tmp\codigo\manage.py", line 22, in <module><br>    main()<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\runs\run_2026-05-14_16-53\99_cierre\_validacion_tmp\codigo\manage.py", line 18, in main<br>    execute_from_command_line(sys.argv)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\__init__.py", line 419, in execute_from_command_line<br>    utility.execute()<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\__init__.py", line 413, in execute<br>    self.fetch_command(subcommand).run_from_argv(self.argv)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\base.py", line 354, in run_from_argv<br>    self.execute(*args, **cmd_options)<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\base.py", line 398, in execute<br>    output = self.handle(*args, **options)<br>             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^<br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\core\management\commands\shell.py", line 87, in handle<br>    exec(options['command'], globals())<br>  File "<string>", line 2, in <module><br>  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Lib\site-packages\django\template\loader.py", line 19, in get_template<br>    raise TemplateDoesNotExist(template_name, chain=chain)<br>django.template.exceptions.TemplateDoesNotExist: reservations/checkout_step3.html |

## Incidencias

- seed_data no se ejecuto correctamente o no existe.
- Ruta /cesta/ no supero smoke test: status 404.
- Template reservations/checkout_step3.html no compila: Traceback (most recent call last):
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\runs\run_2026-05-14_16-53\99_cierre\_validacion_tmp\codigo\manage.py", line 22, in <module>
    main()
  File "D:\University\TFG\PRUEBAS\multiagentes\pipeline\runs\run_2026-05-14_16-53\99_cierre\_validacion_tmp\codigo\manage.py", line 18, in main
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

- _(sin factores bloqueantes)_

## Preparacion manual requerida

- _(no detectada)_
