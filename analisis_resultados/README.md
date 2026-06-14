# Analisis y resultados del TFG

Esta carpeta contiene las evidencias utilizadas durante el analisis y la
planilla maestra con los resultados consolidados del estudio comparativo.

## Resultado final

La fuente oficial de resultados es:

```text
Planilla_Maestra_Evaluacion_TFG.xlsx
```

La planilla aplica las variables y metricas definidas en los capitulos 4 y 5
del TFG. Para interpretar su fundamento metodologico, hipotesis y criterios de
calculo debe consultarse conjuntamente con dichos capitulos.

El archivo Excel se conserva como fuente principal porque mantiene las hojas de
detalle, formulas, filtros y trazabilidad entre evidencias y resultados.

Una version PDF puede incluirse adicionalmente para facilitar la lectura, pero
se considera una copia de consulta. En caso de diferencia, prevalece el archivo
Excel.

## Estructura

### `resultados_baseline/`

Evidencias documentales del proyecto desarrollado por el equipo humano:

- documentos de planificacion y seguimiento;
- actas, revisiones y retrospectivas;
- documentos de gobernanza;
- reconstruccion tecnica utilizada durante el analisis.

La reconstruccion tecnica describe el estado observado del producto. No
representa una modificacion posterior del baseline.

### `resultados_pipeline/`

Seleccion de evidencias de los tres runs oficiales del pipeline:

- manifiestos y resumenes de ejecucion;
- decisiones de los gates humanos;
- artefactos generados;
- backlog y reviews de los sprints;
- validacion final y lecciones aprendidas.

Estos documentos se conservan tal como fueron producidos durante el experimento.
No se corrigen rutas, mensajes, valores ni resultados generados por el modelo,
porque forman parte de la evidencia experimental.

Los artefactos completos y el codigo generado permanecen disponibles en
`pipeline/runs/`. Los archivos `ORIGEN.md` relacionan cada conjunto de
resultados con su run oficial.

## Trazabilidad

El proceso de obtencion de resultados fue:

```text
baseline y runs oficiales
        |
        v
suite funcional automatica
        |
        v
evidencias y resultados preliminares
        |
        v
revision y corroboracion manual
        |
        v
Planilla_Maestra_Evaluacion_TFG.xlsx
```

Los resultados automaticos de la suite se encuentran en `suite test/`. La
planilla maestra incorpora la comprobacion manual posterior y constituye el
resultado consolidado empleado en las conclusiones del TFG.
