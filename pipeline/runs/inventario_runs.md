# Inventario de runs del pipeline

Este inventario no renombra ni mueve carpetas. Sirve como capa documental para
relacionar las carpetas `run_YYYY-MM-DD_HH-MM/` con la numeracion usada en la
bitacora y con la clasificacion metodologica de la memoria.

**Estado del inventario**: congelado el 2026-05-19T03:19:05+02:00. A partir
de este documento se trabajara con las carpetas de run aqui clasificadas. Las
reclasificaciones posteriores solo deberian corregir errores materiales de
inventario, no reinterpretar resultados.

## Criterio de clasificacion

- **Maduracion**: run usado para construir, depurar o estabilizar el pipeline.
- **Prueba manual/no documentada**: carpeta existente sin tratamiento
  metodologico en la bitacora.
- **Confirmacion/congelacion**: run que confirma que el instrumento esta
  operativo y fija el punto de congelacion.
- **Oficial IA**: run valido posterior a la congelacion usado como evidencia
  experimental principal de la memoria.

## Runs documentados en bitacora

| Numero bitacora | Carpeta | Clasificacion | Resultado/resumen segun bitacora | Uso en memoria |
|---|---|---|---|---|
| Run 1 | `run_2026-04-25_01-10` | Maduracion | Fase 01 sobre brief Hundidos. Cumple minimos cuantitativos, rechazado en gate por cobertura insuficiente. | Evidencia de maduracion. |
| Run 2 | `run_2026-04-25_10-11` | Maduracion | Fase 01 aceptada en gate. 22 RF + 6 RNF. | Evidencia de maduracion. |
| Run 3 | `run_2026-05-07_20-50` | Maduracion | Fase 01 dentro de Flow. Rechazado por RNF duplicado/mal clasificado y cobertura insuficiente. | Evidencia de maduracion. |
| Run 4 | `run_2026-05-07_23-50` | Maduracion | Fase 01 rechazada por inversion de requisito de seguridad. | Evidencia de maduracion. |
| Run 5 | `run_2026-05-08_12-03` | Maduracion | Fase 01 aceptada. Artefacto usado como base valida de requisitos. | Evidencia de maduracion. |
| Run 6 | `run_2026-05-08_22-18` | Maduracion | Validacion combinada de gate: rechazado, regeneracion y aceptado. | Evidencia de mecanismo de gates. |
| Run 7 | `run_2026-05-08_22-51` | Maduracion | Aborto directo en gate por consola. | Evidencia de mecanismo de aborto. |
| Run 8 | `run_2026-05-09_18-54` | Maduracion | Fallo antes de Gate 2 por calidad del kickoff de fase 02. | Evidencia de maduracion. |
| Run 9 | `run_2026-05-09_20-18` | Maduracion | Fallo antes de Gate 2; fase 01 con duplicados y RNF escasos. | Evidencia de variabilidad. |
| Run 10 | `run_2026-05-10_10-50` | Maduracion | Cadena fase 01 -> fase 02 -> cierre, gates 1 y 2 aceptados. | Evidencia de maduracion. |
| Run 11 | `run_2026-05-11_13-11` | Maduracion | Cadena fase 01 -> fase 02 -> fase 03 -> cierre, tres gates aceptados. | Evidencia de maduracion. |
| Run 12 | `run_2026-05-11_13-31` | Maduracion | Gate 3 rechaza primer diseno tecnico, regeneracion y aceptacion posterior. | Evidencia de gates en arquitectura. |
| Run 13 | `run_2026-05-12_13-29` | Maduracion | Documentado en bitacora como run de desarrollo temprano. Detalle pendiente de completar si se requiere. | Evidencia de maduracion. |
| Run 14 | `run_2026-05-12_15-34` | Maduracion | Documentado en bitacora como run de desarrollo temprano. Detalle pendiente de completar si se requiere. | Evidencia de maduracion. |
| Run 15 | `run_2026-05-12_16-48` | Maduracion | Tras analizarlo y probar manualmente el codigo, se decide separar `.venv` y `.venv_Test`. | Evidencia de maduracion tecnica. |
| Run 16 | `run_2026-05-13_06-57` | Maduracion | Flow completo viable. Conservado como run valido de construccion, no como run final medida. | Evidencia de maduracion. |
| Run 17 | `run_2026-05-13_15-33` | Maduracion | Mejora frente a Run 16; entrega migraciones, `migrate`, `seed_data`, `runserver`, pero mantiene incidencias funcionales. | Evidencia de maduracion. |
| Run 18 | `run_2026-05-13_23-50` | Maduracion | Se detiene en gate de requisitos tras agotar regeneraciones con fase 01 local. Motiva migrar fase 01 a cloud. | Evidencia de decision tecnica. |
| Run 19 | `run_2026-05-14_02-35` | Maduracion | Run tecnico pre-congelacion con fase 01 cloud. Completa Flow, pero no se usa como run final medida. | Evidencia de maduracion. |
| Run 20 | `run_2026-05-14_11-32` | Maduracion | Aborto en scaffold por `urls.py` de apps incluidas pero no entregadas. | Evidencia de control de scaffold. |
| Run 21 | `run_2026-05-14_16-05` | Maduracion | Completa Flow con regresion de arranque por dependencia externa `requests` y acoplamiento de template. | Evidencia de maduracion. |
| Run 22 | `run_2026-05-14_16-53` | Maduracion | Flow completo, producto arrancable, validacion final con incidencias; clasificado como parcial con incidencias. | Evidencia de maduracion pre-congelacion. |
| Run 23 | `run_2026-05-14_19-50` | Maduracion | Aborto temprano de Sprint 1 por rate limit 429 del proveedor LLM. | Evidencia de control operativo de rate limit. |
| Sin numero explicito | `run_2026-05-15_09-52` | Maduracion | Run que demuestra que `developer.max_tokens=8192` no basta para Sprint 1 por JSON truncado. | Evidencia de ajuste de cuota/tokens. |
| Confirmacion | `run_2026-05-15_11-00` | Confirmacion/congelacion | Completa end-to-end sin reintentos ni regeneraciones; validacion final `ok_global=true`, 16/16 checks ejecutados, 0 incidencias. | Punto de congelacion del instrumento. |
| Preflight de entorno de validacion | `run_2026-05-17_18-49` | Maduracion/post-congelacion no oficial | Run completo con validacion final ejecutada, pero `ok_global=false`, clasificacion `bloqueado_arranque`, 14 incidencias y 2 factores bloqueantes. | Evidencia de preflight fallido; no usar como run oficial. |

## Runs oficiales IA para la memoria

Los runs oficiales se lanzan tras la congelacion del instrumento. No deben
mezclarse con los runs de maduracion anteriores. Para que un run pueda usarse
como evidencia oficial debe tener `run_summary.json`, `manifest.json`,
`validacion_final.json` y cierre completo. Las carpetas
`analisis_resultados/resultados_pipeline/IA_OFICIAL_*/` contienen paquetes
documentales consolidados de los tres runs oficiales: manifests, gates,
artefactos, reviews de sprint, validacion final y cierre. La evidencia completa,
incluido el codigo incremental y final de cada run, permanece en `pipeline/runs/`.

| Codigo oficial | Carpeta de run origen | Carpeta de resultados | Estado |
|---|---|---|---|
| IA_OFICIAL_01 | `run_2026-05-18_15-09` | `analisis_resultados/resultados_pipeline/IA_OFICIAL_01/` | Valido. `resultado_final=completo`, `ok_global=true`, `apto_para_revision_funcional`, 16/16 checks ejecutados, 0 incidencias. |
| IA_OFICIAL_02 | `run_2026-05-18_16-37` | `analisis_resultados/resultados_pipeline/IA_OFICIAL_02/` | Valido. `resultado_final=completo`, `ok_global=true`, `apto_para_revision_funcional`, 16/16 checks ejecutados, 0 incidencias. |
| IA_OFICIAL_03 | `run_2026-05-19_02-15` | `analisis_resultados/resultados_pipeline/IA_OFICIAL_03/` | Valido. `resultado_final=completo`, `ok_global=true`, `apto_para_revision_funcional`, 16/16 checks ejecutados, 0 incidencias. |

## Conjunto congelado de trabajo

- Runs de maduracion: todos los anteriores a la congelacion, incluyendo los
  fallos documentados que justifican decisiones del pipeline.
- Run de confirmacion/congelacion: `run_2026-05-15_11-00`.
- Runs oficiales validos verificados para resultados finales: `IA_OFICIAL_01`,
  `IA_OFICIAL_02` e `IA_OFICIAL_03`.

## Ubicacion de resultados

- Los runs brutos permanecen en `pipeline/runs/`.
- Los resultados oficiales del baseline permanecen en `resultados_baseline/`.
- Los resultados oficiales del pipeline IA se guardan en
  `resultados_pipeline/IA_OFICIAL_01/`,
  `resultados_pipeline/IA_OFICIAL_02/` y
  `resultados_pipeline/IA_OFICIAL_03/`.
- Mientras las carpetas `resultados_pipeline/IA_OFICIAL_*/` no contengan copias
  completas, la fuente primaria de verdad son las carpetas originales bajo
  `pipeline/runs/`.
