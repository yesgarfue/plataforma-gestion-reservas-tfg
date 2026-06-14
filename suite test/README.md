# Suite de pruebas funcionales de Hundidos

Suite externa comun para evaluar las implementaciones Django de Hundidos
desarrolladas en el baseline y en los tres runs oficiales del pipeline hibrido
humano-IA.

La suite no modifica `baseline/` ni `pipeline/`. Trata cada producto como una
aplicacion arrancada y accesible mediante HTTP, con adaptadores minimos para
rutas, campos, credenciales de prueba y textos visibles.

## Objetivo metodologico

Esta suite alimenta:

- `M6 Implementation Rate`: requisitos observables cumplidos sobre requisitos evaluables.
- `M7 Pass-rate suite de tests`: pruebas superadas sobre pruebas ejecutadas.
- `M-operatividad`: estado ordinal de ejecucion funcional.

Los IDs de prueba son estables y trazables (`T-AUTH-01`, `T-CAT-01`,
`T-RES-01`, etc.). La matriz de requisitos se encuentra en
`hundidos_tests/metrics/requirements_matrix.yml`.

## Requisitos

- Python 3.11 o compatible.
- Las aplicaciones que se quieran evaluar instaladas y preparadas segun sus
  respectivos README.
- Un navegador Chromium instalado mediante Playwright.

## Instalacion de la suite

Desde la raiz del repositorio:

```powershell
cd "suite test"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Si PowerShell impide activar el entorno, los mismos comandos pueden ejecutarse
directamente con `.\.venv\Scripts\python.exe`.

## Comprobacion de la instalacion

Con el entorno de la suite activado:

```powershell
python -m pytest --version
python -m playwright --version
python -c "import yaml; print('PyYAML OK')"
python -m pytest --help | Select-String -- "--base-url"
```

Los cuatro comandos deben terminar sin errores. La ultima comprobacion confirma
que el complemento de Playwright ha registrado la opcion `--base-url`.

## Ejecucion

Primero se debe arrancar el producto que se quiera evaluar en el puerto
correspondiente. Despues, desde otra consola y con el entorno de la suite
activado, se ejecuta uno de los siguientes comandos:

```powershell
cd "suite test"
.\.venv\Scripts\Activate.ps1

# Equipo humano
python -m pytest --target baseline --base-url http://127.0.0.1:8000

# Pipeline humano-IA: IA_OFICIAL_01
python -m pytest --target run01 --base-url http://127.0.0.1:8001

# Pipeline humano-IA: IA_OFICIAL_02
python -m pytest --target run02 --base-url http://127.0.0.1:8002

# Pipeline humano-IA: IA_OFICIAL_03
python -m pytest --target run03 --base-url http://127.0.0.1:8003
```

Las rutas, los campos, los selectores y las credenciales de prueba se definen
en:

- `config/baseline.yml`: producto desarrollado por el equipo humano.
- `config/pipeline.yml`: productos generados por el pipeline.

El argumento `--base-url` tiene prioridad sobre la URL incluida en estos
archivos.

### Credenciales de prueba

La suite utiliza cuentas seed incluidas en las bases de datos de demostracion.
Para los clientes, si ninguna credencial configurada funciona, algunas pruebas
pueden crear una cuenta temporal mediante el formulario de registro. Las
pruebas del panel administrativo si necesitan una cuenta administradora seed
valida.

En los runs `IA_OFICIAL_01` e `IA_OFICIAL_02` se utilizan las cuentas
`admin@hundidos.com` y `cliente@hundidos.com`. En `IA_OFICIAL_03` se utilizan
`admin@hundidos.local` y `cliente@hundidos.local`. Las contrasenas de prueba
estan documentadas en el README del pipeline y configuradas en
`config/pipeline.yml`.

## Salidas

Por defecto, los resultados se crean en `suite test/results/`:

- `results_<target>.jsonl`: una linea JSON por prueba.
- `summary_<target>.json`: resumen agregado para M6, M7 y M-operatividad.

Los resultados oficiales incluidos en el repositorio son:

- `results_baseline.jsonl` y `summary_baseline.json`.
- `results_run01.jsonl` y `summary_run01.json`.
- `results_run02.jsonl` y `summary_run02.json`.
- `results_run03.jsonl` y `summary_run03.json`.

El archivo `resultados_suite_funcional.xlsx` **tambien se incluye en el
repositorio**, pero no representa el resultado final del estudio. Es una
planilla puente construida a partir de la ejecucion automatica de la suite:

- `00_lectura`: instrucciones y criterios de lectura.
- `01_reporte_puente`: resultados automaticos comparativos de baseline y
  pipeline.
- `02_requisitos_M6`: evaluacion de requisitos para la metrica M6.
- `03_resumen`: resumen generado a partir de los resultados automaticos.

Los JSON/JSONL son la evidencia bruta y reproducible de las ejecuciones
automaticas. El Excel de esta carpeta facilita la lectura y el traslado de esa
evidencia, por lo que se conservan ambos.

Posteriormente, los resultados automaticos fueron revisados y corroborados
manualmente. El resultado consolidado y definitivo utilizado para las
conclusiones del TFG se encuentra en:

```text
analisis_resultados/Planilla_Maestra_Evaluacion_TFG.xlsx
```

Por tanto, la planilla maestra es la fuente final del estudio, mientras que
`results/` y `resultados_suite_funcional.xlsx` documentan la ejecucion
automatica previa y permiten mantener la trazabilidad del proceso.

Estados:

- `passed`: comportamiento observable verificado.
- `failed`: la prueba se ejecuto y no cumplio.
- `blocked`: no pudo ejecutarse por precondicion funcional o tecnica de la app.
- `skipped`: no aplica por configuracion explicita del adaptador.

## Politica de adaptadores

Los tests deben mantenerse orientados a comportamiento. El adaptador solo puede declarar:

- rutas publicas;
- nombres de campos HTML;
- textos o selectores visibles;
- credenciales seed;
- valores de datos seed conocidos.

No debe inspeccionar modelos, vistas ni base de datos para decidir si una prueba pasa.
