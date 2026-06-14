# Pipeline hibrido humano-IA - Hundidos

Pipeline experimental desarrollado para el TFG:

> Estudio comparativo entre un equipo humano y un pipeline hibrido humano-IA
> aplicado al desarrollo de un proyecto software real.

El pipeline utiliza CrewAI para generar de forma incremental una aplicacion
Django de alquiler de barcos. El proceso combina agentes LLM, validadores
deterministas y tres gates de revision humana.

## Estructura

```text
brief/                  Entrada funcional del experimento
src/pipeline/           Implementacion del pipeline
scripts/                Verificaciones auxiliares
runs/                   Artefactos de las ejecuciones
pipeline_specs.md       Contrato operativo del pipeline
pipeline_bitacora.md    Historial de decisiones y diagnosticos
pyproject.toml          Dependencias del pipeline
uv.lock                 Versiones exactas de las dependencias
```

La ejecucion sigue estas fases:

```text
01_requisitos
  -> Gate humano 1
02_planificacion
  -> Gate humano 2
03_arquitectura
  -> Gate humano 3
03b_scaffold
04_sprint_1
05_sprint_2
06_sprint_3
99_cierre
```

## Runs oficiales

Los tres runs utilizados como evidencia experimental oficial son:

| Codigo | Carpeta | Estado |
|---|---|---|
| IA_OFICIAL_01 | `runs/run_2026-05-18_15-09/` | Completo, 16/16 checks, 0 incidencias |
| IA_OFICIAL_02 | `runs/run_2026-05-18_16-37/` | Completo, 16/16 checks, 0 incidencias |
| IA_OFICIAL_03 | `runs/run_2026-05-19_02-15/` | Completo, 16/16 checks, 0 incidencias |

El producto final de cada run se encuentra en:

```text
runs/<run_oficial>/06_sprint_3/codigo/
```

Los runs de maduracion conservan requisitos, planes, revisiones, resultados y
trazas metodologicas. Sus carpetas `codigo/` no se incluyen en Git para evitar
duplicar productos intermedios. Los tres runs oficiales si conservan todo el
codigo generado y su base SQLite final.

La clasificacion completa se encuentra en `runs/inventario_runs.md`.

## Requisitos

- Windows PowerShell, Linux o macOS
- Python 3.11 recomendado
- `uv`
- Git
- Una clave de Anthropic para ejecutar nuevas generaciones

La configuracion activa utiliza Anthropic en todas las fases. El `Modelfile` y
las referencias a Ollama se conservan como evidencia de la fase de maduracion,
pero Ollama no es necesario para ejecutar la configuracion oficial actual.

## Entorno del pipeline

El pipeline y los productos Django utilizan entornos separados.

Desde la carpeta `pipeline`, instala las dependencias exactas del pipeline:

```powershell
py -3.11 -m pip install uv
uv sync --locked
```

Este comando crea `.venv/`. El entorno no se incluye en Git.

En Linux o macOS:

```bash
python3.11 -m pip install uv
uv sync --locked
```

Para activar el entorno manualmente en Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Tambien se pueden ejecutar los comandos directamente mediante `uv run`, sin
activar el entorno.

## Variables de entorno

Crea el archivo local `.env` a partir del ejemplo:

```powershell
Copy-Item .env.example .env
```

Edita `.env` e introduce una clave valida:

```text
ANTHROPIC_API_KEY=tu-clave
```

El archivo `.env` esta excluido de Git. Nunca debe publicarse. La clave de
Anthropic puede generar consumo facturable cuando se ejecuta un run nuevo.

## Verificacion del pipeline

Las verificaciones locales no realizan una generacion completa:

```powershell
uv run python scripts/verify_pipeline.py
```

La ejecucion correcta termina mostrando:

```text
=== Todas las verificaciones pasaron ===
```

## Ejecucion del pipeline

Para iniciar una ejecucion nueva:

```powershell
uv run crewai run
```

Tambien puede utilizarse:

```powershell
uv run python -m pipeline.main
```

Cada ejecucion crea una carpeta:

```text
runs/run_YYYY-MM-DD_HH-MM/
```

Durante las tres primeras fases, la operadora debe revisar el Markdown
generado y crear `gate_humano.md` en la carpeta correspondiente.

Las decisiones validas son:

```text
aceptado
rechazado
abortado
```

## Entorno de validacion Django

El entorno `.venv_Test/` esta separado de `.venv/` para que las dependencias
de los productos Django generados no alteren CrewAI.

Para recrearlo en Windows:

```powershell
py -3.11 -m venv .venv_Test
.\.venv_Test\Scripts\python.exe -m pip install --upgrade pip
.\.venv_Test\Scripts\python.exe -m pip install Django==3.2 Pillow==9.5.0 django-filter==23.1 requests==2.31.0 python-decouple==3.6 gunicorn==20.1.0
```

El pipeline utiliza por defecto:

```text
.venv_Test/Scripts/python.exe
```

Para seleccionar otro interprete:

```powershell
$env:DJANGO_CHECK_PYTHON="D:\ruta\a\python.exe"
```

Los entornos `.venv/` y `.venv_Test/` son locales y no se incluyen en Git.

## Probar un producto oficial

Las bases SQLite oficiales ya contienen migraciones, barcos, puertos,
fabricantes y usuarios de prueba. No es necesario ejecutar `seed_data` para
la primera comprobacion.

Desde la raiz de `pipeline`:

```powershell
$pythonValidacion = (Resolve-Path ".\.venv_Test\Scripts\python.exe").Path
cd .\runs\run_2026-05-18_15-09\06_sprint_3\codigo
& $pythonValidacion manage.py check
& $pythonValidacion manage.py migrate
& $pythonValidacion manage.py runserver
```

Para probar otro producto, sustituye la carpeta del run por:

```text
runs/run_2026-05-18_16-37/06_sprint_3/codigo/
runs/run_2026-05-19_02-15/06_sprint_3/codigo/
```

La aplicacion queda disponible en:

```text
http://127.0.0.1:8000/
```

Rutas principales:

- Login: `http://127.0.0.1:8000/accounts/login/`
- Administracion Django: `http://127.0.0.1:8000/admin/`
- Panel personalizado: `http://127.0.0.1:8000/admin-panel/`

Para cambiar de producto, detiene primero el servidor y vuelve a la raiz de
`pipeline` antes de entrar en la carpeta del siguiente run.

## Credenciales oficiales

Las siguientes credenciales fueron comprobadas contra los hashes almacenados
en cada base SQLite.

### IA_OFICIAL_01

Run: `run_2026-05-18_15-09`

```text
Administrador
Email: admin@hundidos.com
Contrasena: admin123

Cliente
Email: cliente@hundidos.com
Contrasena: cliente123
```

### IA_OFICIAL_02

Run: `run_2026-05-18_16-37`

```text
Administrador
Email: admin@hundidos.com
Contrasena: admin123

Cliente
Email: cliente@hundidos.com
Contrasena: cliente123
```

### IA_OFICIAL_03

Run: `run_2026-05-19_02-15`

```text
Administrador
Email: admin@hundidos.local
Contrasena: admin123

Cliente
Email: cliente@hundidos.local
Contrasena: cliente123
```

Estas bases son snapshots del experimento y pueden contener cuentas creadas
durante las comprobaciones manuales. No deben utilizarse como bases de
produccion.

## Datos y archivos excluidos

- `.env`: contiene la clave real de Anthropic.
- `.venv/`: entorno del pipeline.
- `.venv_Test/`: entorno de validacion Django.
- `**/_validacion_tmp/`: copias temporales creadas por la validacion final.
- `codigo/` de runs no oficiales: productos intermedios duplicados.

Se conservan:

- el codigo fuente del pipeline;
- prompts, configuracion y validadores;
- los artefactos documentales de todos los runs;
- intentos fallidos y decisiones de gates;
- el codigo completo de los tres runs oficiales;
- las tres bases SQLite oficiales;
- los informes `validacion_final.json` y `review_final.md`.

## Documentacion metodologica

- `brief/brief.md`: entrada funcional congelada.
- `pipeline_specs.md`: especificacion y reglas del instrumento.
- `pipeline_bitacora.md`: decisiones, cambios y diagnosticos.
- `runs/inventario_runs.md`: clasificacion de las ejecuciones.
- `runs/<run>/run_summary.json`: resumen de una ejecucion.
- `runs/<run>/99_cierre/manifest.json`: manifiesto del producto generado.
- `runs/<run>/99_cierre/validacion_final.json`: resultados de validacion.
