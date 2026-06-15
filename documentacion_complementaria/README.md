# Documentacion complementaria del TFG

Esta carpeta funciona como indice del material digital que complementa la
memoria. Los anexos formales contienen la informacion necesaria para comprender
el estudio; el repositorio conserva los archivos exhaustivos, ejecutables o
demasiado extensos para reproducirlos dentro del documento.

Cada archivo tiene una unica ubicacion canonica. Los indices de los anexos
enlazan esa ubicacion y no duplican planillas, YAML, runs, codigo ni resultados.

## Organizacion

```text
documentacion_complementaria/
|-- README.md
|-- general/
|   |-- README.md
|   `-- Planificacion_TFG.xlsx
|-- anexo_A_caso_base/README.md
|-- anexo_B_caso_IA/README.md
|-- anexo_C_instrumento_evaluacion/README.md
|-- anexo_D_configuracion_pipeline/README.md
`-- anexo_E_reproduccion_validacion/README.md
```

## Correspondencia con la memoria

| Bloque | Capitulos | Material digital principal |
|---|---|---|
| General | Capitulo 3 | [`general/Planificacion_TFG.xlsx`](general/Planificacion_TFG.xlsx) |
| Anexo A. Evidencias del caso base | Capitulos 4, 6, 8 y 9 | [`analisis_resultados/resultados_baseline/`](../analisis_resultados/resultados_baseline/) y [`baseline/docs_auditoria/`](../baseline/docs_auditoria/) |
| Anexo B. Evidencias del caso IA | Capitulos 7, 8 y 9 | [`analisis_resultados/resultados_pipeline/`](../analisis_resultados/resultados_pipeline/) y [`pipeline/runs/`](../pipeline/runs/) |
| Anexo C. Instrumento de evaluacion | Capitulos 4, 5, 8 y 9 | [`analisis_resultados/Planilla_Maestra_Evaluacion_TFG.xlsx`](../analisis_resultados/Planilla_Maestra_Evaluacion_TFG.xlsx) |
| Anexo D. Configuracion del pipeline | Capitulo 7 | [`pipeline/src/pipeline/crews/`](../pipeline/src/pipeline/crews/) y [`pipeline_config.yaml`](../pipeline/src/pipeline/config/pipeline_config.yaml) |
| Anexo E. Reproduccion y validacion | Capitulos 4, 5, 8 y 9 | [`suite test/`](../suite%20test/), [`baseline/`](../baseline/) y [`pipeline/`](../pipeline/) |

Los README de cada bloque explican el alcance de esos archivos y el orden de
consulta recomendado.

## Criterio de inclusion

1. La memoria puede comprenderse sin descargar el repositorio.
2. El repositorio conserva el detalle necesario para auditar o reproducir.
3. No se generan copias PDF de archivos YAML ni duplicados de la planilla.
4. Los runs oficiales permanecen junto al pipeline y sus paquetes seleccionados
   permanecen en `analisis_resultados/`.
5. Para una entrega estable debe publicarse una etiqueta o release y citar esa
   version, no depender indefinidamente de la rama `main`.
