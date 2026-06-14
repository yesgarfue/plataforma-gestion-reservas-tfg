---
documento: pipeline_specs
proyecto: Hundidos - Pipeline IA (Caso 02)
version: 1.3
estado: congelado
fecha_creacion: 2026-04-24
fecha_congelacion: 2026-05-15
fecha_actualizacion: 2026-05-17
autor: Yesica Garate Fuentes
---

# Pipeline Specs - Hundidos (Caso IA)

Documento tecnico interno del pipeline. No es un capitulo del TFG: es el
checklist operativo que fija como debe comportarse el pipeline congelado antes
de lanzar runs medidos.

Esta version 1.3 actualiza el documento operativo con las decisiones registradas
en la bitacora hasta el cierre de `run_2026-05-15_11-00`. Ese run confirma que
el instrumento completa el recorrido end-to-end, ejecuta el cierre documental y
supera la validacion final determinista con `ok_global=true`.

Desde la congelacion del 2026-05-15, las siguientes ejecuciones ya no deben
usarse para seguir ajustando prompts, validadores o contratos. Si aparecen
incidencias, se registran como resultados experimentales, salvo errores
materiales del entorno que impidan lanzar el instrumento.

## Cambios Principales Frente A v1.2

- El spec pasa de `en_revision` a `congelado`.
- Se actualiza la referencia de cierre: Run 16 deja de ser el punto vigente y
  `run_2026-05-15_11-00` queda como run de confirmacion del instrumento.
- `developer.max_tokens` vigente pasa a `24000`, coherente con
  `pipeline_config.yaml` tras la subida de cuota Anthropic a Nivel 2.
- La validacion final deja de estar pendiente: fue ejecutada con 16 checks
  planificados, 16 ejecutados, 0 no ejecutados, 0 incidencias y
  `ok_global=true` en el run de confirmacion.
- Se documentan los cambios generales derivados de Run 22: deteccion de
  comandos Django en apps no instaladas, templates criticas flexibles para
  paso 3, diagnosticos con final de traceback y reglas generales sobre rutas
  canonicas, `management/commands/` y template tags.
- Se documenta el control de rate limit 429: el Flow espera `retry-after` si
  existe o una ventana conservadora antes de consumir el siguiente reintento.
- `manifest.json`, `review_final.md`, `readme.md` y
  `lecciones_aprendidas.md` quedan como parte probada del cierre en
  `99_cierre/`.

---

## Bloque 0 - Contexto Y Punto De Partida

- Pipeline desarrollado sobre CrewAI Flow.
- Entrada funcional unica: `brief/brief.md`.
- El proyecto humano de comparacion es Hundidos, una aplicacion Django +
  SQLite.
- El pipeline IA es hibrido humano-LLM: combina gates humanos con generacion
  LLM y validaciones deterministas.
- Objetivo del PMV: ejecutar el pipeline de principio a fin sobre Hundidos,
  produciendo un producto Django inspeccionable y ejecutable bajo un banco de
  pruebas estable.
- La bitacora (`pipeline_bitacora.md`) conserva el historial de decisiones,
  fallos, cambios y runs. Este spec fija el estado operativo vigente.

### Clasificacion De Runs

Para evitar ambiguedad metodologica se distinguen tres categorias:

- **Run de construccion/maduracion**: ejecucion real usada para estabilizar el
  instrumento experimental. Es evidencia valida del proceso, pero no se usa
  como medicion principal de las hipotesis.
- **Run completo de Flow**: ejecucion que llega a `cerrar_run` sin abortar en
  gates, esquema, Sprint 0 o limites de reintento. Puede terminar con
  `resultado_final = completo`, aunque el producto final aun tenga fallos
  funcionales.
- **Run final medida**: ejecucion lanzada tras congelar el protocolo final. No
  admite edicion manual del producto generado ni ajustes de prompts/codigo
  durante la medicion. Sus fallos se registran como resultados del experimento.

Run 16 pertenece a las dos primeras categorias, pero no a la tercera. Run 22 se
considera run de maduracion pre-congelacion con producto parcialmente funcional
e incidencias concretas. Run 23 se clasifica como incidencia operativa de rate
limit antes de producir entrega de Sprint 1. `run_2026-05-15_11-00` se toma como
run de confirmacion y punto de congelacion del instrumento.

### Frontera De Congelacion

Hasta la congelacion final se permitieron ajustes al instrumento experimental:
prompts, validadores, entorno de prueba y documentacion tecnica. Tras la
congelacion final del 2026-05-15:

- no se edita codigo generado por el LLM;
- no se corrigen manualmente bugs del producto;
- no se ajustan prompts durante la run medida;
- no se modifica el pipeline para rescatar una run ya lanzada;
- cualquier cambio posterior implica nueva version de spec y nueva run;
- los fallos funcionales de runs medidos se reportan como resultados, no como
  motivos para seguir afinando el instrumento.

---

## Bloque 1 - Modelos Y Entornos

### Perfiles LLM Vigentes

Los modelos viven en `src/pipeline/config/pipeline_config.yaml`.

| Perfil | Fase | Provider | Modelo | Parametros relevantes |
|---|---|---|---|---|
| `default` | Fase 01, Analista | Ollama local | `ollama/hundidos-analista:latest` | parametros documentados en `generation.default` |
| `pm` | Fase 02, Planificacion | Anthropic | `anthropic/claude-haiku-4-5` | `temperature=0.0`, `max_tokens=8192` |
| `architect` | Fase 03, Arquitectura | Anthropic | `anthropic/claude-haiku-4-5` | `temperature=0.0`, `max_tokens=8192` |
| `developer` | Fase 04: Sprint 0-3, Desarrollo | Anthropic | `anthropic/claude-haiku-4-5` | `temperature=0.0`, `max_tokens=24000` |

### Justificacion Del Uso Cloud

La Fase 01 permanece local para conservar el componente Ollama del pipeline.
Fase 02, Fase 03 y Fase 04 (desarrollo) se migraron a Anthropic porque los runs reales
mostraron que el modelo local 7B no era estable con salidas Pydantic extensas,
JSON grande y contexto acumulado bajo la restriccion de 4 GB VRAM.

Esto no invalida el enfoque hibrido: el resultado metodologico es un pipeline
humano-LLM que usa modelo local donde es viable y modelo cloud donde la carga
estructurada excede el hardware disponible.

### Entornos Python

Se separan dos entornos:

- `.venv`: entorno de ejecucion del pipeline IA. Contiene CrewAI, Pydantic,
  LiteLLM/Anthropic, YAML y dependencias de orquestacion.
- `.venv_Test`: entorno fijo de validacion del producto Django generado.
  Contiene Django y dependencias necesarias para ejecutar `manage.py check`.

El pipeline no instala automaticamente dependencias del producto generado y no
mezcla `requirements.txt` de los runs dentro del entorno `.venv` del pipeline.

### Validacion Django

`src/pipeline/utils/django_runner.py` resuelve el interprete de validacion asi:

1. Si existe `DJANGO_CHECK_PYTHON`, usa esa ruta.
2. Si no existe, usa `.venv_Test/Scripts/python.exe` en Windows o
   `.venv_Test/bin/python` en entornos POSIX.
3. Si no hay interprete valido, devuelve `ArranqueResult(ok=False)` con error
   claro. No usa silenciosamente `sys.executable`.

---

## Bloque 2 - Agentes Y Componentes

### Roles Vigentes

| Agente / Componente | Rol | Entrada | Salida | Crew / Modulo |
|---|---|---|---|---|
| Analista | Extrae requisitos funcionales y no funcionales | `brief.md`, feedback humano si hay regeneracion | `RegistroRequisitos` | `requisitos_crew` |
| PM | Genera backlog, plan de sprints y riesgos | requisitos aceptados | `Backlog`, `PlanSprints`, `Riesgos` | `planificacion_crew` |
| Arquitecto | Define diseno tecnico Django | requisitos, backlog, plan y riesgos aceptados | `DisenoTecnico` | `arquitectura_crew` |
| Desarrollador | Genera scaffold y sprints incrementales | diseno tecnico, backlog del sprint, codigo previo, review anterior | `EntregaSprint` | `desarrollo_crew` |
| Review automatico | Evalua senales de cumplimiento y arranque Django | backlog sprint, codigo, resultado `manage.py check` | `ReviewSprint` | `utils/review_builder.py` |
| Validador final | Verifica minimos tecnicos del producto generado sin modificarlo | codigo final de Sprint 3 | `validacion_final.json`, `review_final.md` | `utils/final_validator.py` |
| Manifest | Trazabilidad estructurada del run | state, hashes, config, gates, reviews, validacion final | `manifest.json` | `utils/manifest.py` |
| Closer | Cierre documental final | manifest/resumen/gates/reviews | `readme.md`, `lecciones_aprendidas.md` | `closer/closer.py` |

### Decisiones Vigentes

- Una crew por fase.
- No hay QA agent LLM.
- La verificacion minima del producto se hara mediante validador determinista,
  no mediante juicio LLM subjetivo.
- No se divide el Desarrollador en backend/templates.
- Los prompts viven en YAML dentro de cada crew.
- La escritura fisica de codigo no la hace el LLM: la hace el Flow despues de
  validar `EntregaSprint`.
- La validacion final observara y registrara resultados, pero no corregira
  archivos del entregable.

---

## Bloque 3 - Flujo Del Run

Flujo operativo vigente:

```text
setup_run
  -> 01_requisitos
  -> Gate 1
  -> 02_planificacion
  -> Gate 2
  -> 03_arquitectura
  -> Gate 3
  -> 03b_scaffold
  -> 04_sprint_1
  -> 05_sprint_2
  -> 06_sprint_3
  -> 99_validacion_final
  -> 99_cierre_documental
  -> cerrar_run
```

### Gates Humanos

Hay tres gates humanos:

- Gate 1 tras requisitos.
- Gate 2 tras planificacion.
- Gate 3 tras arquitectura.

No hay gates humanos entre `03b_scaffold` y los sprints. Los sprints se
evaluan mediante validaciones deterministas y reviews automaticos.

### Sprint 0 / `03b_scaffold`

Sprint 0 es una fase tecnica previa al Sprint 1. Su objetivo es generar una
plantilla Django minima y ejecutable para reducir el tamano de salida del
Sprint 1.

Reglas:

- `numero_sprint` de la entrega es `0`.
- No implementa historias de usuario.
- Debe producir una base Django que pase `manage.py check`.
- Si `manage.py check` falla en Sprint 0, el Run aborta antes del Sprint 1.
- Sprint 0 debe tender a entregar solo `manage.py`, paquete de proyecto,
  `settings.py`, `urls.py`, `wsgi.py/asgi.py`, estructura minima de apps,
  `apps.py`, `__init__.py` y marcadores `.gitkeep` cuando proceda.

### Sprints 1-3

- Sprint 1 parte del codigo generado por `03b_scaffold`.
- Sprint 2 copia el codigo de Sprint 1 antes de aplicar su entrega.
- Sprint 3 copia el codigo de Sprint 2 antes de aplicar su entrega.
- Si `manage.py check` falla en Sprint 1-3, no aborta automaticamente: el
  fallo se registra en `review_sprint_N.json/md`.
- Si la generacion de una `EntregaSprint` valida agota reintentos, el Run
  aborta con `abortado_por_limite`.

### Validacion Final / Cierre

El Flow incorpora una validacion final determinista despues de Sprint 3 y un
cierre documental determinista dentro de `99_cierre/`. El cierre escribe
`manifest.json`, `readme.md` y `lecciones_aprendidas.md`. Estos artefactos no
corrigen el producto generado ni anaden juicio LLM; solo consolidan evidencia
ya producida por el Flow.

El cierre completo fue probado en `run_2026-05-15_11-00`: la validacion final
se ejecuto completa, `manifest.json` se genero y el Closer produjo
`readme.md` y `lecciones_aprendidas.md`. Por eso esta version 1.3 queda
congelada.

---

## Bloque 4 - Artefactos

### Patron General

Los artefactos estructurados se guardan como JSON canonico y, cuando aplica,
como Markdown para revision humana. El JSON es la fuente de verdad.

El codigo generado vive dentro de la carpeta `codigo/` de cada fase tecnica o
sprint.

### Tabla De Artefactos Vigente

| Fase | JSON | Markdown | Codigo / otros | Productor |
|---|---|---|---|---|
| 01 | `registro_requisitos.json` | `registro_requisitos.md` | `gate_humano.md` | Analista + operadora |
| 02 | `backlog.json` | `backlog.md` | `gate_humano.md` | PM + operadora |
| 02 | `plan_sprints.json` | `plan_sprints.md` |  | PM |
| 02 | `riesgos.json` | `riesgos.md` |  | PM |
| 03 | `diseno_tecnico.json` | `diseno_tecnico.md` | `gate_humano.md` | Arquitecto + operadora |
| 03b | `entrega_scaffold.json` | - | `codigo/`, `scaffold_check.json` | Desarrollador + Flow |
| 04 | `backlog_sprint_1.json`, `entrega_sprint_1.json`, `review_sprint_1.json` | `backlog_sprint_1.md`, `review_sprint_1.md` | `codigo/` | script + Desarrollador + review |
| 05 | `backlog_sprint_2.json`, `entrega_sprint_2.json`, `review_sprint_2.json` | `backlog_sprint_2.md`, `review_sprint_2.md` | `codigo/` | script + Desarrollador + review |
| 06 | `backlog_sprint_3.json`, `entrega_sprint_3.json`, `review_sprint_3.json` | `backlog_sprint_3.md`, `review_sprint_3.md` | `codigo/` | script + Desarrollador + review |
| 99 | `validacion_final.json`, `manifest.json` | `review_final.md`, `readme.md`, `lecciones_aprendidas.md` | `_validacion_tmp/codigo` | Validador final + Manifest + Closer |
| Run | `run_summary.json` | - | - | Flow |

### Estado De `manifest.json`

El manifest vive en `99_cierre/manifest.json` y se genera al cierre del run de
forma determinista. Recoge hashes de `brief.md`, `pipeline_specs.md` y
`pipeline_config.yaml`, modelos configurados, versiones principales, fases,
gates, artefactos principales y resumen de la validacion final. No sustituye a
`run_summary.json`: este permanece en la raiz del run como resumen operativo
minimo del Flow.

---

## Bloque 5 - Estructura De Carpetas

Estructura operativa:

```text
pipeline/
  brief/brief.md
  pipeline_specs.md
  pipeline_bitacora.md
  pyproject.toml
  .venv/                 # entorno del pipeline
  .venv_Test/            # entorno fijo para validar Django generado
  src/pipeline/
    main.py
    state.py
    config/pipeline_config.yaml
    crews/
      requisitos_crew/
      planificacion_crew/
      arquitectura_crew/
      desarrollo_crew/
    gates/human_gate.py
    validation/schemas.py
    validation/validators.py
    utils/
      django_runner.py
      io_utils.py
      llm_factory.py
      manifest.py
      renderers.py
      review_builder.py
      sprint_backlog_builder.py
    closer/closer.py
    legacy/
  runs/run_YYYY-MM-DD_HH-MM/
    01_requisitos/
    02_planificacion/
    03_arquitectura/
    03b_scaffold/
    04_sprint_1/
    05_sprint_2/
    06_sprint_3/
    99_cierre/
    _attempts/
    logs/
  product/
```

`product/` no se actualiza automaticamente. La consolidacion del producto
final es una decision manual de la operadora.

---

## Bloque 6 - Contratos Y Validaciones

### Nivel 1 - Esquema Pydantic

Modelos principales:

- `RegistroRequisitos`
- `Backlog`
- `PlanSprints`
- `Riesgos`
- `DisenoTecnico`
- `BacklogSprint`
- `ArchivoCodigo`
- `EntregaSprint`
- `ArranqueResult`
- `ReviewSprint`

Si la salida LLM no valida por esquema, cuenta como reintento automatico y se
preserva el intento fallido en `_attempts/`.

### Nivel 2 - Contenido Minimo

Reglas deterministas principales:

- Requisitos: minimo cuantitativo de RF/RNF.
- Backlog: minimo de historias y campos obligatorios.
- Plan: exactamente 3 sprints, cobertura completa del backlog y sin duplicados.
- Riesgos: minimo de riesgos y campos obligatorios.
- Diseno tecnico: debe mencionar Django 3.2, SQLite y PayPal en `stack`.
- EntregaSprint:
  - `numero_sprint` permitido: 0, 1, 2 o 3.
  - `archivos` no puede estar vacio.
  - rutas relativas dentro de `codigo/`; se rechazan rutas absolutas, `..` y
    rutas tipo `C:/...`.
  - no se permiten paths duplicados.
  - se rechaza contenido vacio salvo para `__init__.py` y `.gitkeep`.
  - si se requiere base Django, la entrega debe incluir `manage.py`,
    `settings.py` y `urls.py`.

### Nivel 3 - Arranque Django

`ejecutar_manage_check(codigo_dir, timeout_s)` ejecuta:

```text
python manage.py check
```

pero usando el interprete de validacion Django (`DJANGO_CHECK_PYTHON` o
`.venv_Test`), no el Python del pipeline.

Resultados:

- `ok`
- `returncode`
- `stdout_resumen`
- `stderr_resumen`
- `timeout_s`
- `timeout`

Ademas, los resumenes de salida larga conservan tanto el inicio como el final
del texto para no perder la ultima linea util de tracebacks extensos. Esto
permite diagnosticar errores como `TemplateDoesNotExist`, filtros de template
invalidos o imports ausentes sin tener que abrir el log completo.

### Validacion Final Del Producto

Implementada en `utils/final_validator.py`. La validacion final se ejecuta
sobre el codigo final de `06_sprint_3/codigo/` o sobre una copia temporal
equivalente. No edita archivos del entregable.

La validacion incluye controles generales anadidos durante la maduracion:

- deteccion estatica de apps que contienen `management/commands/*.py` pero no
  aparecen en `INSTALLED_APPS`;
- resolucion flexible de la template critica del paso 3, aceptando
  `reservations/step3.html` y el nombre historico
  `reservations/checkout_step3.html` si el producto lo entrega;
- validacion de la template realmente existente para evitar acoplar el cierre a
  un nombre interno no fijado por el contrato tecnico.

### Contrato De Producto Ejecutable Hundidos

El prompt del Desarrollador refleja este contrato operativo. No amplia el
brief: explicita que significa entregar un producto Django ejecutable dentro
del pipeline.

- El producto final debe poder prepararse con `python manage.py migrate`,
  `python manage.py seed_data` y `python manage.py runserver`.
- Si el producto define modelos propios, debe entregar migraciones iniciales
  para las apps afectadas. No debe depender de `makemigrations` ni de
  `migrate --run-syncdb` para completar el entregable.
- Todo formulario que reciba datos del usuario debe validar campos
  obligatorios, tipo, formato, longitud, rangos y coherencia antes de guardar
  o avanzar de paso.
- Ejemplos minimos de validacion: email con `EmailField`, telefono con formato
  razonable, fechas con inicio no anterior a hoy y fin posterior a inicio, y
  cantidades como enteros positivos.
- Toda ruta declarada debe responder sin error 500. Si requiere login, sesion,
  cesta o paso previo, debe redirigir de forma controlada o mostrar mensaje.
- El flujo de reserva debe ser robusto desde paso 1 hasta paso 3.
- Las rutas principales del brief deben quedar inspeccionables: home,
  catalogo, detalle de barco, cesta, registro, login, reserva paso 1, reserva
  paso 2, reserva paso 3, seguimiento, admin Django y admin-panel.
- Si se entrega un comando en `management/commands/`, la app que lo contiene
  debe estar incluida en `INSTALLED_APPS` para que Django pueda descubrirlo.
- No se deben usar filtros ni tags de template no estandar salvo que se
  entreguen como `templatetags` propios y se carguen explicitamente con
  `{% load %}` en cada template que los use. Los calculos de negocio deben
  resolverse preferentemente en vistas, modelos o servicios antes del render.
- Las rutas canonicas del contrato publico deben exponerse en su ruta exacta.
  Si una app se monta mediante `include()` bajo un prefijo, el producto debe
  montar tambien las rutas canonicas en raiz o proporcionar alias compatibles.

Comprobaciones minimas previstas:

- existencia de `manage.py`;
- `python manage.py check`;
- deteccion de carpetas `migrations/` para apps propias con modelos;
- `python manage.py migrate` estandar sobre una base de datos limpia;
- registro de si `migrate --run-syncdb` seria necesario como diagnostico
  secundario, sin usarlo para ocultar el fallo del `migrate` estandar;
- ejecucion de `python manage.py seed_data` si el comando existe;
- arranque corto con `runserver`;
- compilacion de la template critica del paso 3;
- prueba minima de rutas clave mediante HTTP:
  - `/`;
  - `/barcos/`;
  - `/cesta/`;
  - `/accounts/registro/`;
  - `/accounts/login/`;
  - `/reserva/paso1/`;
  - `/reserva/paso2/`;
  - `/reserva/paso3/`;
  - `/admin/`;
  - `/admin-panel/`.

El resultado se escribira en `99_cierre/validacion_final.json` con al menos:

- `ok_global`;
- `check`;
- `migraciones`;
- `migrate`;
- `seed_data`;
- `runserver`;
- `rutas`;
- `incidencias`;
- `preparacion_manual_requerida`;
- `observaciones`.

Tambien se generara `99_cierre/review_final.md` como vista humana
determinista del JSON. El JSON sigue siendo la fuente de verdad.

El bloque `review_final` debe incluir:

- version del protocolo de validacion;
- checks planificados;
- checks ejecutados;
- checks no ejecutados y motivo;
- incidencias;
- factores bloqueantes;
- clasificacion final.

Estos campos permiten comparar runs oficiales posteriores y contar en cuantos
runs se ejecuto cada comprobacion, separando fallos del producto generado,
fallos de entorno y checks no ejecutados por bloqueo previo.

La validacion final no corrige errores como ausencia de migraciones, errores
500 en rutas o validaciones incompletas de formularios. Esos defectos se
registran como resultado del producto generado.

En `run_2026-05-15_11-00` la validacion final confirmo el estado congelado del
instrumento: 16 checks planificados, 16 ejecutados, 0 no ejecutados, 0
incidencias, 0 factores bloqueantes, `ok_global=true` y clasificacion
`apto_para_revision_funcional`.

---

## Bloque 7 - Politica De Gates Y Reintentos

### Gates

La operadora no edita artefactos generados por LLM. Solo puede:

- aceptar;
- rechazar con observaciones accionables;
- abortar.

El gate produce una plantilla de `gate_humano.md` si no existe. La operadora
rellena o corrige la decision, observaciones y accion. Los campos `gate`,
`fase` y `decision` son obligatorios y se validan de forma estricta para evitar
errores de copia entre gates. Los timestamps documentales del acta humana se
permiten para auditoria, pero no son la fuente oficial de tiempo: el tiempo
oficial de revision lo calcula el Flow mediante `duracion_s_gate_humano`.

El Flow lee `gate_humano.md` tras el handshake por consola.

### Reintentos

| Tipo | Limite |
|---|---|
| Reintentos automaticos por fallo tecnico/esquema/contenido | 3 |
| Regeneraciones humanas por gate rechazado | 3 |

Los dos presupuestos son independientes. Si se agotan, el Run aborta con
`abortado_por_limite`, salvo aborto humano explicito (`abortado_en_gate`).

Si una llamada LLM falla por rate limit 429, el Flow lo trata como incidencia
operativa temporal del proveedor. Antes de consumir el siguiente reintento,
espera el valor `retry-after` si el SDK lo expone; si no existe, espera una
ventana conservadora de 90 segundos. Esta politica evita convertir un mismo
limite temporal en tres fallos inmediatos del pipeline.

---

## Bloque 8 - Politica De Errores

Estados globales vigentes:

- `pendiente`
- `completo`
- `abortado_en_gate`
- `abortado_por_limite`
- `bloqueado_arranque`
- `abortado_por_cambio_spec`

Nota: `completo` indica que el Flow llego al cierre sin abortar por los estados
anteriores. No implica por si solo que el producto final haya superado la
validacion final.

Reglas:

- Si una fase no produce artefacto valido tras 3 reintentos automaticos, el Run
  aborta por limite.
- Si un gate humano aborta, el Run termina con `abortado_en_gate`.
- Si Sprint 0 no arranca, el Run aborta antes del Sprint 1.
- Si Sprint 1-3 no arrancan, el fallo se registra en review y el Run continua.
- Si falta el entorno Django de validacion, `ArranqueResult.ok=False` con error
  claro.
- Si la validacion final detecta fallos de producto, el run puede seguir
  cerrando con trazabilidad completa, pero `validacion_final.json` debe reflejar
  `ok_global=false`.
- La validacion final no ejecuta correcciones sobre el producto generado.

Timeouts vigentes desde `pipeline_config.yaml`:

| Concepto | Valor |
|---|---|
| llamada LLM | 1800 s |
| `manage.py check` | 60 s |
| Docker build | 600 s |

Docker build esta previsto pero no implementado en validacion final.

---

## Bloque 9 - Ejecucion

### Comando

```powershell
crewai run
```

desde la raiz del proyecto.

### Precondiciones

- `.venv` activo y con dependencias del pipeline.
- `.env` o entorno con `ANTHROPIC_API_KEY` para perfiles cloud.
- Ollama disponible para fase 01.
- `.venv_Test` creado y ejecutable para validar Django generado.
- `.venv_Test` debe contener al menos Django 3.2 y dependencias compatibles
  con el codigo generado.

Ejemplo de comprobacion del entorno Django:

```powershell
.\.venv_Test\Scripts\python.exe --version
.\.venv_Test\Scripts\python.exe -c "import django; print(django.get_version())"
```

### Cierre Actual

El cierre escribe `run_summary.json` y resume por consola las fases ejecutadas.
La validacion final escribe `validacion_final.json` y `review_final.md`. El
cierre documental escribe tambien
`99_cierre/manifest.json`, `99_cierre/readme.md` y
`99_cierre/lecciones_aprendidas.md`.

Las metricas comparativas externas del TFG, como implementation rate,
pass-rate de una suite comun y log estructurado de incidencias, se definen y
ejecutan fuera del pipeline. El pipeline produce evidencia para alimentarlas,
pero no mezcla generacion del producto con evaluacion comparativa externa.

### Intervencion Manual Permitida

Durante la run final medida la operadora puede:

- ejecutar comandos de observacion/verificacion definidos en el protocolo;
- aceptar, rechazar o abortar en los tres gates humanos;
- registrar observaciones factuales en la bitacora.

Durante la run final medida la operadora no puede:

- editar codigo generado por el LLM;
- corregir templates, vistas, formularios, migraciones o datos seed;
- ejecutar `makemigrations` para completar el producto tras la generacion;
- usar `migrate --run-syncdb` como sustituto silencioso de migraciones
  ausentes.

`migrate --run-syncdb` puede usarse solo como diagnostico secundario para
inspeccionar comportamiento funcional, registrandolo explicitamente como
preparacion manual y no como cumplimiento del criterio principal de migracion.

---

## Bloque 10 - Estado Congelado Y Pendientes Externos

El pipeline queda congelado tras `run_2026-05-15_11-00`. Ya no quedan
pendientes internos bloqueantes para lanzar ejecuciones de prueba de la memoria.

Se mantienen como pendientes externos o decisiones fuera del instrumento:

- conservar `.venv` y `.venv_Test` como precondicion operativa antes de cada
  run medido;
- documentar las ejecuciones oficiales en un artefacto separado de resultados
  experimentales, referenciando `runs/`, manifiestos, validaciones finales y
  metricas;
- decidir si Docker se evalua como nivel C separado en la comparativa externa,
  ya que no forma parte de la validacion final congelada;
- no actualizar automaticamente `product/`; cualquier consolidacion del
  producto final sigue siendo una decision manual posterior y debe distinguirse
  de la salida generada por el pipeline.

---

## Checklist De Congelacion

- [x] Fase 01 con Ollama local.
- [x] Fase 02 con Anthropic cloud.
- [x] Fase 03 con Anthropic cloud.
- [x] Fase 04 con Anthropic cloud y `developer.max_tokens=24000`.
- [x] Gates humanos 1, 2 y 3.
- [x] Derivacion determinista de backlogs de sprint.
- [x] Desarrollo devuelve `EntregaSprint`; el Flow escribe archivos.
- [x] Sprint 0 / `03b_scaffold` incorporado.
- [x] Validacion Django separada via `.venv_Test` / `DJANGO_CHECK_PYTHON`.
- [x] Sprint 0 aborta si no arranca.
- [x] Prompt de Sprint 0 restringido a scaffold minimo.
- [x] `.venv` y `.venv_Test` comprobados por la operadora con Python 3.11.7.
- [x] Prompt del Desarrollador ajustado para migraciones, seed data, rutas
      minimas y validaciones de formulario.
- [x] Reglas generales incorporadas para `management/commands/`,
      template tags, rutas canonicas y diagnostico de tracebacks.
- [x] Control de rate limit 429 incorporado.
- [x] Validacion final determinista definida, implementada y probada.
- [x] Manifest completo definido e implementado en `99_cierre/manifest.json`.
- [x] Closer determinista implementado para `readme.md` y
      `lecciones_aprendidas.md`.
- [x] Cierre completo probado en `run_2026-05-15_11-00`.
- [x] `pipeline_specs.md` v1.3 congelado tras el run de confirmacion.
