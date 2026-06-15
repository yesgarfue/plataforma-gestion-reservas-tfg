# Estudio comparativo de desarrollo software humano y humano-IA

Repositorio asociado al Trabajo de Fin de Grado:

> Estudio comparativo entre un equipo humano y un pipeline hibrido humano-IA
> aplicado al desarrollo de un proyecto software real.

El caso de estudio consiste en el desarrollo de una plataforma Django para la
gestion y reserva de embarcaciones. El repositorio conserva las dos alternativas
comparadas, la suite comun de evaluacion y los resultados finales del estudio.

## Organizacion del repositorio

### `baseline/`

Aplicacion desarrollada por el equipo humano y utilizada como linea base de la
comparacion.

Incluye:

- codigo fuente de la aplicacion Django;
- datos sinteticos de demostracion;
- instrucciones de instalacion y ejecucion;
- credenciales de prueba.

La instalacion se explica en `baseline/README.md`.

### `pipeline/`

Implementacion del pipeline hibrido humano-IA basado en CrewAI.

Incluye:

- codigo fuente del pipeline;
- brief y especificaciones del experimento;
- validadores y gates de revision humana;
- trazas y artefactos de las ejecuciones;
- tres runs oficiales con sus productos software finales.

La metodologia, instalacion y ejecucion se explican en
`pipeline/README.md`.

### `suite test/`

Suite funcional externa utilizada para evaluar con los mismos criterios el
baseline y los tres runs oficiales del pipeline.

Incluye:

- 27 pruebas funcionales con identificadores trazables;
- adaptadores para las distintas implementaciones;
- configuracion de rutas y credenciales de prueba;
- resultados automaticos en JSON y JSONL;
- una planilla puente de los resultados automaticos.

El archivo `suite test/resultados_suite_funcional.xlsx` no es el resultado
final del estudio. Su funcion es conservar y presentar la evidencia obtenida
mediante la ejecucion automatica.

La instalacion y los comandos de ejecucion se explican en
`suite test/README.md`.

### `analisis_resultados/`

Contiene la consolidacion y el analisis final del experimento.

Los resultados producidos por la suite automatica fueron posteriormente
revisados y corroborados manualmente. La fuente definitiva utilizada para las
conclusiones del TFG es:

```text
analisis_resultados/Planilla_Maestra_Evaluacion_TFG.xlsx
```

Las subcarpetas de resultados conservan evidencias y documentos auxiliares
empleados durante la consolidacion.

### `documentacion_complementaria/`

Indice de correspondencia entre los anexos formales de la memoria y el material
digital del repositorio.

Incluye:

- el Excel de planificacion general del TFG;
- un README por anexo con las rutas canonicas de consulta;
- referencias a evidencias, configuracion, instrumentos y procedimientos sin
  duplicar planillas, YAML, runs ni codigo.

El punto de entrada es `documentacion_complementaria/README.md`.

## Trazabilidad de los resultados

El flujo seguido para obtener los resultados fue:

```text
baseline y runs oficiales
        |
        v
suite funcional automatica
        |
        v
JSON, JSONL y planilla puente
        |
        v
revision y corroboracion manual
        |
        v
Planilla_Maestra_Evaluacion_TFG.xlsx
```

Por tanto:

- los JSON, JSONL y la planilla de `suite test/` son evidencia automatica;
- la planilla maestra de `analisis_resultados/` es el resultado consolidado
  final.

## Orden de lectura recomendado

1. `baseline/README.md`: instalacion y ejecucion del producto humano.
2. `pipeline/README.md`: funcionamiento del pipeline y runs oficiales.
3. `suite test/README.md`: metodologia y ejecucion de las pruebas.
4. `analisis_resultados/Planilla_Maestra_Evaluacion_TFG.xlsx`: resultados
   definitivos del estudio.
5. `documentacion_complementaria/README.md`: correspondencia con los anexos de
   la memoria.
