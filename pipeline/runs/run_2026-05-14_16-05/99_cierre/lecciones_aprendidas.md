# Lecciones aprendidas del run

**Run**: `run_2026-05-14_16-05`

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

## Preparacion manual requerida

- El `migrate` estandar no fue correcto. No se ejecuta `migrate --run-syncdb` como correccion dentro del validador.

## Gates humanos

- `01_requisitos/gate_humano.md`: gate=`1`, fase=`01_requisitos`, decision=`aceptado`
- `02_planificacion/gate_humano.md`: gate=`2`, fase=`02_planificacion`, decision=`aceptado`
- `03_arquitectura/gate_humano.md`: gate=`3`, fase=`03_arquitectura`, decision=`aceptado`

## Alcance de estas lecciones

Las metricas externas del estudio, como implementation rate, pass-rate de suite comun y log estructurado de incidencias, se calculan fuera del pipeline para no mezclar generacion con evaluacion comparativa.
