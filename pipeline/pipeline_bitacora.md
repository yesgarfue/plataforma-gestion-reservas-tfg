# Pipeline - Bitácora de decisiones

## 2026-04-24 — Diagnóstico y reinicio controlado del Caso 02
#### Estado de partida
- Código existente con brief de películas, no de Hundidos.
- Fase PM funcional (Caso2PMFlow en main.py): genera 01_requisitos,02_backlog, 03_sprint_plan con un único agente PM. Validación por esquema y reintentos operativos.
- Fase de ejecución no ha llegado a producir código Django en ninguna ejecución. Bloqueo repetido en la descomposición del diseño técnico (contratos 09/09a/09b/10/10a).
- Dos agentes en ejecución (Django Developer, Template Developer), no los 4 roles diferenciados (Analista, PM, Arquitecto, Desarrollador) prometidos en la memoria.
- Sin gates humanos entre fases: solo un gate dentro del sprint.
- Sin carpeta run_* aislada por ejecución.
#### Diagnóstico
Se detectó un patrón de sobreingeniería similar al observado en casos de prueba anteriores y ya reconocido como lección aprendida en el capítulo 6 de la memoria. El esfuerzo se centró en fijar y validar el diseño técnico antes de completar el recorrido end-to-end, lo que impidió alcanzar el PMV.
#### Acciones tomadas
1. Se preserva y archiva 'casos_de_prueba/` como copia congelada del estado actual. Sirve como evidencia de los casos de prueba (Caso 01 y Caso 02) para la sección 7.2.
2. Se mantiene 'pipeline/` como carpeta de trabajo activa, con recorte.
3. Se reutilizaran lor archivos necesarios para la construccion del pipeline (main.py, schemas.py, renderers.py, io_utils.py, estructura outputs/json + docs + _attempts)
4. Se reescribe la fase de ejecución por sprints con un único agente Desarrollador, sin contratos congelados descompuestos ni validación contractual cruzada.
5. Se añaden agentes Analista, Arquitecto y Closer (PMV = 4 agentes funcionales + cierre), alineados con la memoria y la guía.
6. Se añaden los tres gates humanos prometidos: tras Requisitos, tras Planificación, tras Arquitectura.
7. Se añade manifest.json al inicio de cada ejecución.
8. Se añade aislamiento por ejecución: run_YYYY-MM-DD_HH-MM/.
9. Brief de películas se sustituye por brief de Hundidos. Brief queda congelado antes de la ejecución medida oficial
10. Modelo candidato único para PMV: qwen2.5-coder:7b (restricción por 4GB VRAM en RTX 3050 Laptop). Demas modelos quedan descartados. 
11. QA agent LLM no se incorpora en el PMV. La validación estructural la hace validador determinista; la validación de contenido, el gate humano.
12. Cloud LLM queda fuera del PMV. Se menciona en la memoria como decisión de viabilidad económica. Cambio a cloud si ocurre sería reemplazo de MODEL_ID, documentado como ajuste post-PMV.
#### Siguiente paso
Definir el pipeline_specs.md, documento técnico interno del pipeline.


## 2026-04-24 — Decisiones sobre brief y gates humanos
#### Brief
- Contenido: funcionalidades aterrizadas a alquiler de barcos + decisiones de dominio consolidadas con el patrocinador (actas 16/23/27 Oct, 4 Nov
  2024) + stack técnico definido (Django 3.2 + SQLite + PayPal sandbox + contra-reembolso) + criterios de aceptación (checklist del docente).
- Justificación: medir capacidad de gestión y desarrollo, no de adivinar dominio.
- El brief incorpora ajustes reales del proyecto baseline:
  * tres filtros combinables (puertos, fabricantes, precio)
  * filtro de fechas en catálogo con etiqueta "No disponible"
  * dropdowns para puertos y fabricantes (no texto libre)
  * inicio de sesión integrado en proceso de compra
  * cantidad seleccionable en tarjeta de catálogo
  * tasa de combustible (50€/día, gratis en veleros)
  * estados de reserva: PAGADO / PENDIENTE DE PAGO
  * código de seguimiento por email
  * cancelación solo si pendiente de pago
  * admin no puede eliminar usuarios con reservas pendientes
- El brief NO incluye funcionalidades que el baseline propuso y fueron rechazadas por el patrocinador (fianza 20%, no devolución en cancelación).
#### Gate humano - política fijada
- El gate humano tiene tres opciones: aceptar, rechazar con observaciones (regenerar), abortar.
- La operadora humana NO edita manualmente los artefactos producidos por los agentes. Cualquier corrección pasa por regeneración.
- Si tras MAX_REGENERATIONS el artefacto sigue sin ser aceptable, se registra como fallo del Run. Esto es resultado válido del experimento, no un problema a tapar.
- Esta política se congela antes de la ejecución medida
#### Brief CONGELADO
- Al congelar el brief hubo dudas sobre qué funcionalidades del baseline eran parte del alcance formal y cuáles fueron añadidos no requeridos por el patrocinador;  se decide ceñirse al alcance aprobado en actas.
- Fecha_congelacion: 2026-04-24, version 1.0
 

## 2026-04-24 — pipeline_specs.md congelado
Versión 1.0 congelada. Cualquier cambio a partir de ahora requiere nueva congelación e invalida Runs posteriores a la modificación.


## 2026-04-24 — Decisión técnica 
El MD de cada artefacto lo genera un renderer determinista en Python a partir del Pydantic validado, no el LLM. 
Motivo: alinea con el spec ("JSON es fuente de verdad") y elimina una vía de alucinación. En tasks.yaml usamos output_pydantic=<Modelo> para que CrewAI valide la salida del agente contra el esquema automáticamente.


## 2026-04-24 — Preparación de la base técnica del pipeline
Se consolidaron varios componentes internos necesarios para que el pipeline pudiera generar, validar, registrar y presentar sus artefactos de forma controlada y trazable.
- Añadido funcion 'ensure_dir' para asegurar la creación de carpetas.
- Añadido 'now_iso_madrid' para registrar fechas y horas en la zona horaria de Madrid.
- Añadido para registrar huellas verificables de los artefactos 'sha256_dict`.
- Reescrito 'renderers.py`, los renderers recibían diccionarios y devolvían texto Markdown; ahora reciben modelos Pydantic ya validados y generan el Markdown a partir de ellos.
- Reescrito 'schemas.py`, definiendo los modelos Pydantic principales del pipeline: 'RegistroRequisitos`, 'Backlog`, 'PlanSprints`, 'Riesgos' y 'DisenoTecnico`. Pydantic valida solo la estructura, mientras que las comprobaciones de contenido mínimo y coherencia cruzada se gestionarán en 'validators.py`. 
- Se configuró 'extra="forbid"` para rechazar campos inventados por el LLM.
- Añadido 'state.py`, encargado de representar el estado interno del pipeline.
- Los gates humanos no se guardan dentro del estado, sino que se leen desde disco cuando hace falta, manteniendo clara la separación entre estado interno del pipeline y revisión humana externa.


## 2026-04-24 — Inicio de la primera crew (requisitos_crew). 
Estructura de carpetas creada siguiendo convención CrewAI: crews/<nombre>_crew/config/{agents,tasks}.yaml + <nombre>_crew.py con @CrewBase. 
Decisiones tomadas para el YAML del Analista: 
- Prompt íntegro en español, dado que el brief y el artefacto son en español y el modelo es qwen2.5-coder:7b (multilingüe con sesgo al idioma del prompt del sistema); 
- El brief NO va en el backstory del agente, va en el input de la task (reusabilidad del rol); 
- El LLM se instancia en Python desde pipeline_config.yaml en vez de declararse en YAML, para centralizar los parámetros en un único sitio congelado y hashable.


## 2026-04-24 — agents.yaml y tasks.yaml de la requisitos_crew escrito. 
- Prompt íntegro en español por coherencia con brief/artefacto/modelo
- El rol se define como un agente al proyecto Hundidos, no lo presenta como analista genérico
- El objetivo incluye los umbrales del Bloque 6 (≥15 RF, ≥3 RNF) para alinear al agente con el validator determinista (la calidad semántica sigue juzgándola el gate humano)
- El contexto del agente es largo (~2300 caracteres) con reglas de contenido, estilo, vocabulario literal del brief, y prohibición explícita de inventar fuera de alcance, esto es deliberado para compensar el tamaño reducido del 7B local
- Las instrucciones del task.yaml tienen el brief y el identificador de la ejecucion actual agregado como {brief} y {run_id}
- Se proporciana ejemplo explícito minimalista en expected_output(salida) (2 RF + 1 RNF) para mostrar estructura sin que el modelo copie cantidades
- Reglas de formato agresivamente repetidas ("solo JSON, sin markdown, sin prefacio") porque un 7B local necesita instrucción redundante.
- Se ajustará tras ver el resultado en la salida real.


## 2026-04-24 — Primera crew construida. 
- Archivos: utils/llm_factory.py (reutilizable por las 4 crews) y crews/requisitos_crew/requisitos_crew.py (clase @CrewBase con 1 agente y 1 task). 
- Construcción del LLM con parámetros correctos desde pipeline_config.yaml, construcción del Crew con agente "Analista", task con output_pydantic=RegistroRequisitos.


## 2026-04-24 — Detalle técnico detectado al construir el LLM: 
- litellm despoja el prefijo de proveedor del string del modelo cuando lo guarda en el atributo .model del objeto LLM. Es decir, LLM(model="ollama/qwen2.5-coder:7b") guarda "qwen2.5-coder:7b" en .model; el prefijo "ollama/" se usa solo internamente para enrutar la petición al servidor correcto.


## 2026-04-24 — Error en primera ejecución del pipeline: 
*Completions.create() got an unexpected keyword argument 'num_ctx'*
- El fallo no estaba en la lógica del pipeline, sino en la forma de pasar parámetros específicos del modelo local a través de la cadena de integración 'CrewAI → LiteLLM → Ollama`.
- El parámetro 'num_ctx' pertenece a Ollama y permite configurar el tamaño de la ventana de contexto del modelo. Sin embargo, al pasarlo directamente como argumento raíz en 'LLM()`, CrewAI/LiteLLM lo trató como si fuera un parámetro compatible con la API OpenAI-style utilizada internamente por LiteLLM. Esa API no reconoce 'num_ctx`, por lo que la llamada falló antes de llegar correctamente a Ollama.
- En lugar de pasar el parametro mediante 'extra_body={"options": {...}}`, se definio parámetros de generación directamente en un 'Modelfile' de Ollama y crear un modelo derivado para el pipeline.
- Lección para el capítulo 7: los errores de integración entre capas pueden aparecer cuando se mezclan parámetros específicos de un proveedor con APIs intermedias genéricas. Para reducir deuda técnica, conviene ubicar cada configuración en la capa correspondiente: CrewAI orquesta, LiteLLM enruta y Ollama gestiona los parámetros propios del modelo local.


##  2026-04-24 — Fix aplicado vía Modelfile Ollama: 
- Creación del modelo derivado hundidos-analista con num_ctx=8192, temperature=0.2, top_p=0.9, seed=42 bakeados. 
- El pipeline_config.yaml pasa a apuntar al modelo derivado y los parámetros de generación se mantienen en el YAML solo como campos _documentada para trazabilidad/manifest, no se leen desde código. 
- llm_factory.get_llm() simplificado: solo pasa model, base_url, timeout al constructor LLM de CrewAI.

---

## 2026-04-25 — Cierre fase 01 
#### Fase 01: Ciclo de gate humano completo
- Run 1 (run_2026-04-25_01-10): primera ejecución del pipeline end-to-end sobre el brief de Hundidos. Cumplió mínimos cuantitativos(15 RF + 3 RNF) pero rechazado en gate humano por cobertura insuficiente: omisión de subsecciones 3.5 (pagos), 3.6 (estados de reserva), parte de 3.1 (reglas admin), 3.4 (cesta-admin); RNFs triviales que no cubren restricciones técnicas explícitas del brief sección 4.
- Diagnóstico: el LLM 7B optimiza umbrales numéricos de forma literal; las reglas de cobertura cualitativa requieren ser explicitadas en el prompt como listado, no implícitas.
#### Decisiones técnicas de la sesión
- Acción: prompt v2 con regla explícita de cobertura por subsecciones del brief (3.1 a 3.8) + bloques de sección 4. Se conservan versiones anteriores para trazabilidad en run_2026-04-25_01-10.
- Modificar parametros del Modelfile: num_ctx=8192 + temperature=0.2 + seed=42 
#### Resultados
- Run 2 (run_2026-04-25_10-11): aceptado en gate. 22 RF + 6 RNF, cobertura 8/8 de subsecciones de sección 3 y 5 bloques de sección 4. Tres correcciones tipográficas manuales documentadas en gate_humano.md (uniquement → únicamente, eliminación de referencia interna 3.1, corrección de sentido invertido en RF-11 sobre cesta-admin).


## 2026-04-25 — Plan Fase 02
- Migración main.py → crewai.Flow[pipelineState]
- Implementación del gate humano programático (mecanismo que lee la decisión humana, interpreta si fue aceptado, rechazado o abortado y decide qué camino seguir).
- Planificacion_crew con un agente PM y tres tasks secuenciales (backlog → plan_sprints → riesgos), enfoque "una crew por fase"


## 2026-04-25 — Consideraciones sobre Cloud LLM
- NO introducir cloud en esta fase del PMV. Mantener TFG con alcance original (humano-baseline vs IA-pipeline-local). Posible experimento secundario en capítulo 7 cuando el pipeline esté completo, sin que afecte hipótesis principales.

---

## 2026-05-07 — Subpaso 8a: Migración del orquestador a CrewAI Flow
#### Resumen
- 'main.py' reescrito con Flow con tres pasos encadenados: 'setup_run' (`@start`) → 'ejecutar_fase_01_requisitos' (`@liste (setup_run)`) → 'cerrar_run' (`@listen(ejecutar_fase_01_requisitos)`).
- Comportamiento externo idéntico al script lineal: mismas carpetas en 'runs/run_*/`, mismos artefactos, mismo 'run_summary.json`. El contrato de arranque se preserva: 'pyproject.toml' no cambia, 'crewai run' y 'pipeline.main:kickoff' siguen siendo los puntos de entrada.
#### Decisión: reintentos automáticos como bucle interno, no como nodos del Flow
- Los 3 reintentos automáticos se mantienen como loop dentro de 'ejecutar_fase_01_requisitos`, no como pasos `@listen' separados ya que son política interna de la fase, no estados del pipeline. Modelarlos como nodos del Flow inflaría el grafo sin ganancia y complicaría el gate humano real.
####  Verificación
- Implementacion del archivo 'verify_pipeline.py`: instancia 'pipeline`, verifica que 'state' arranca con defaults correctos a través del 'StateProxy' que CrewAI inyecta, comprueba presencia de los tres métodos del Flow y que 'kickoff' se exporta a nivel de módulo. No ejecuta el Flow para no consumir Ollama. 
#### Hallazgo: StateProxy en lugar de pipelineState directo
- CrewAI envuelve 'flow.state' en un 'StateProxy' que delega al modelo Pydantic real. 'isinstance(flow.state, pipelineState)` falla aunque el acceso a campos funciona perfectamente. Detectado al ejecutar el verify por primera vez. El paso 10 se ajustó para verificar comportamiento (campos y defaults) en lugar de identidad de clase.Todas las verificaciones correctas.

---

## 2026-05-07 — Bug del cliente OpenAI-compatible y timeouts dentro del Flow
#### Síntoma
Al ejecutar el primer 'crewai run' con la nueva arquitectura Flow, fallaba con 'Failed to connect to OpenAI API: Request timed out`, agotando los 3 reintentos automáticos en cuestión de minutos. El script lineal anterior funcionaba sin problemas con la misma 'requisitos_crew`, el mismo 'llm_factory.py' y el mismo 'pipeline_config.yaml`.
#### Diagnóstico
Inspección del LLM efectivo del agente vía prints temporales reveló:
*Agente.llm: OpenAICompatibleCompletion, model=hundidos-analista, base_url=http://localhost:11434/v1*
Dos cosas distintas al comportamiento esperado del Run 02:
1. CrewAI/litellm escogía el cliente 'OpenAICompatibleCompletion' en lugar del cliente nativo de Ollama. Se sospecha que es un efecto del contexto 'asyncio.run()` que el Flow ejecuta internamente.
2. Ese cliente apuntaba al endpoint OpenAI-compatible de Ollama(`/v1`) y exigía el id de modelo en su forma canónica con tag, no la abreviada que la API nativa acepta.

Para aislar capas se construyó 'scripts/test_llm_solo.py`, que invoca el mismo 'LLM' fuera de cualquier Flow/Agent/Crew. Resultados de los tests aislados:
- Prompt corto ("HOLA"): respuesta correcta en 10s.
- Prompt largo (~5000 caracteres de JSON): respuesta correcta en 3,1 minutos (mucho menos de los ~20 minutos que duró el Run 02).
Conclusión: el LLM directo no tiene problema de timeout. El problema estaba en algún timeout HTTP que se aplicaba dentro del Flow y no fuera, probablemente un default de litellm bajo cuando se ejecuta en el contexto async del Flow.
#### Solución aplicada (combinada)
1. **`pipeline_config.yaml`**: nombre del modelo con tag explícito.
       Antes:    name: "ollama/hundidos-analista"
       Después:  name: "ollama/hundidos-analista:latest"
2. **`pipeline_config.yaml`**: timeout subido de 300 a 1800 segundos.
       Antes:    llm_call_s: 300
       Después:  llm_call_s: 1800
3. **`llm_factory.py`**: variables de entorno 'LITELLM_REQUEST_TIMEOUT' y 'OPENAI_TIMEOUT' seteadas con el mismo valor que 'timeout`, para forzar a litellm a respetar el timeout incluso cuando se ejecuta dentro del contexto async del Flow.
       os.environ["LITELLM_REQUEST_TIMEOUT"] = str(timeout_s)
       os.environ["OPENAI_TIMEOUT"] = str(timeout_s)
Los tres cambios se aplicaron juntos. No se aisló cuál de ellos era estrictamente necesario; el conjunto resolvió el problema.
#### Validación
Run del 2026-05-07_20-50 ejecutado dentro del Flow:
- 30 RF + 7 RNF generados.
- 0 reintentos automáticos consumidos.
- 'resultado_final = completo`.
- Tiempo de ejecución sin medir con precisión, pero del orden de los Runs anteriores (~15-25 minutos), lo cual confirma que la causa no era de rendimiento sino de timeouts mal calibrados.
#### Lecciones para la memoria
- Cuando se introduce una capa de orquestación (Flow), el contexto async puede cambiar comportamientos de capas inferiores (litellm) que el código previo no exponía. Los tests aislados (`test_llm_solo.py`) son útiles para separar capas durante el debugging.
- Los nombres de modelo en endpoints OpenAI-compatible no se resuelven con la misma laxitud que en la API nativa. Forma canónica con tag obligatoria.
- Los 'timeout=` declarados en el constructor 'LLM(...)` no siempre llegan a la capa HTTP de litellm; hay que reforzarlos con variables de entorno cuando se ejecuta en contexto async.
#### Pendiente
- Recalcular el hash de 'pipeline_config.yaml`. Los cambios alteran el hash que el manifest del Run documentará. Como estamos en fase de construcción del pipeline (no en ejecución medida oficial), el cambio queda anotado aquí; cuando se cierre el pipeline y se arranque la ejecución medida, este será el hash congelado.
- Telemetría externa de CrewAI (`telemetry.crewai.com`): tira un warning DNS si la red la bloquea. No es bloqueante. Documentado en este punto para no volver a depurar lo mismo.

---

## 2026-05-08 — Cierre de la fase 01 dentro del Flow (ciclo gate completo)
#### Tres Runs ejecutados dentro del Flow con el mismo prompt y mismo modelo
**Run 3 (run_2026-05-07_20-50)**: 30 RF + 7 RNF. Validación automática superada. Rechazado en gate humano por dos defectos:
- RNF-06 y RNF-07 con métrica idéntica ("interfaz en español") bajo categorías distintas, uno mal clasificado como Seguridad
- Cobertura insuficiente de la sección 4 del brief. 
Regeneración solicitada con observaciones documentadas en gate_humano.md.
**Run 4 (run_2026-05-07_23-50)**: 21 RF + 8 RNF. Validación automática superada. Rechazado en gate humano por **inversión del requisito de seguridad**: el brief sección 4 dice "contraseñas no almacenadas en texto plano", el modelo generó "contraseñas almacenadas en texto plano, prioridad Baja". Defecto de fidelidad al brief, no corregible manualmente sin violar la política de gate (no editar artefactos LLM).
Regeneración 1 de 3 consumida.
**Run 5 (run_2026-05-08_12-03)**: 28 RF + 6 RNF. Validación automática superada. **Aceptado en gate humano con observaciones**: cobertura buena de la sección 3 (8/8 subsecciones), no hay duplicados ni inversiones de sentido. Hallazgos no bloqueantes documentados: falta el RNF de datos seed (sección 4 del brief no está representada al 100%, 7 de 8 bloques cubiertos), y RNF-06 (Seguridad) redactado de forma genérica sin recoger los componentes concretos del brief (CSRF, validación de formularios).
Regeneraciones consumidas: 2 de 3.
- Tres Runs consecutivos con el mismo input produjeron registros cuantitativamente distintos (30/21/28 RF; 7/8/6 RNF) y cualitativamente distintos en patrones de error (duplicación → inversión de sentido → omisión + vaguedad). Esto justifica la presencia del gate humano iterativo en el pipeline y proporciona material directo para la sección de resultados.
- Migración a Flow cerrado y validado: Fase 01 (Run 5) con artefacto aceptado disponible en 'runs/run_2026-05-08_12-03/01_requisitos/`.


## 2026-05-08 — Subpaso 8b: gate humano programático (human_gate.py)
- Implementación de 'src/pipeline/gates/human_gate.py' con atributos fase, fase_dir, artefacto_md, numero_gate, regeneraciones_consumidas, max_regeneraciones=3 -> GateResult`.
- 'GateResult' (Pydantic, 'extra="forbid"`): decision ('aceptado'|'rechazado'|'abortado'), observaciones, accion, timestamp_inicio, timestamp_fin, duracion_s.
- Imprime header del gate por consola: número de gate, fase, ruta absoluta del MD a revisar, ruta donde escribir gate_humano.md, regeneraciones consumidas/totales, política de rechazo.
- Espera handshake 'ok' o 'abort`. 'abort' retorna decision="abortado" sin leer disco. 'ok' dispara la lectura y validación de 'fase_dir / "gate_humano.md"`.
- Validación del MD: frontmatter YAML obligatorio, 'decision' ∈ {aceptado, rechazado, abortado}, y si 'decision == "rechazado"` exige sección `## Acción' no vacía. Errores de validación son recuperables: reimprime el problema y vuelve a pedir ok/abort.
- Avisos blandos (no invalidan el gate): si los campos 'gate' o 'fase' del frontmatter discrepan de los argumentos, se imprime warning pero se acepta. Decisión consciente: probable error de copia-pega humano.
- Parser manual de `## Sección' (`_extraer_seccion`): tolera sufijos como `## Acción (solo si rechazado)`.
- 'human_gate' NO actualiza 'pipelineState' ni incrementa 'regeneraciones_humanas`.
- 'fase_dir' inexistente lanza 'GateError' antes de pedir input. Evita que la operadora descubra el problema después de revisar el MD.
- Verificacion en el paso 11 del 'scripts/verify_pipeline.py`: cubre los cinco caminos del gate (aceptado / rechazado válido / rechazado sin acción / decisión inválida / abort directo) + GateError por fase_dir inválido, todo sin input humano real (monkeypatch de 'builtins.input' con un iterador de respuestas).
- Validación manual end-to-end con un scratch test contra 'runs/run_2026-05-08_12-03/01_requisitos/gate_humano.md`: el gate retornó 'decision="aceptado"` correctamente, observaciones y acción extraídas como esperado.
 
  
## 2026-05-08 — Subpaso 8c: gate humano integrado en el Flow
- Gate 1 enchufado en 'pipelineFlow' tras la fase 01. Toda la lógica vive en el helper privado '_kickoff_requisitos_con_gate_humano`, invocado desde 'ejecutar_fase_01_requisitos`.
- Bucle 'while' interno que orquesta: kickoff con reintentos automáticos (existente) → escritura de artefactos → 'human_gate()`→ ramificación según 'GateResult.decision`.
- Tres ramas implementadas:
  - 'aceptado' → 'gate_decision="aceptado"`, 'resultado_final="completo"`.
  - 'abortado' → 'gate_decision="abortado"`, 'resultado_final="abortado_en_gate"`.
  - 'rechazado' con presupuesto disponible → incrementa 'regeneraciones_humanas`, resetea 'reintentos_automaticos' a 0, formatea bloque de feedback, vuelve al kickoff. Sin presupuesto → 'gate_decision="rechazado"`, 'resultado_final="abortado_por_limite"`.
- Reintentos automáticos agotados antes del gate → no se abre el gate; 'resultado_final="abortado_por_limite"` con 'gate_decision="N/A"` (valor por defecto). Distinción semántica: `"N/A"` = el gate nunca se celebró, `"rechazado"` = el gate se celebró y el operador rechazó hasta agotar presupuesto.

Se descartó usar `@router`/`@listen("decision")` de CrewAI para representar la ramificación del gate como nodos del Flow. 
- Razón: el bucle de regeneración (rechazado → regenera → vuelve al gate) no encaja limpiamente como grafo dirigido sin trucos. La opción elegida mantiene simetría con la decisión ya tomada en 8a sobre los reintentos automáticos: política interna de la fase, encapsulada en un método, no expuesta como nodos del grafo. Implicación: el grafo del Flow (setup_run → fase_01 → cerrar_run) es más simple de lo que el pipeline realmente hace; conviene que el diagrama del capítulo 6 de la memoria muestre la ramificación lógica explícitamente, aunque internamente sea un 'while`.
#### Feedback humano vía placeholder `{feedback_humano}` en tasks.yaml
- El feedback humano **se añade** al prompt original, no lo sustituye. Las reglas de cobertura, vocabulario y formato del tasks.yaml siguen vigentes; la operadora aporta correcciones específicas sobre la generación previa.
- Se añade el placeholder al final del campo 'description' de 'extraer_requisitos`. En la primera generación se pasa 'feedback_humano=""` (placeholder inerte). En regeneraciones, se pasa un bloque delimitado con `------ INSTRUCCIONES DE REGENERACIÓN (operadora humana) ------ ... ------ FIN INSTRUCCIONES DE REGENERACIÓN ------` que contiene observaciones y acción de la operadora del gate previo. El bloque queda al final del prompt, tras el brief.
- Validación previa antes de tocar el Flow: script aislado 'scripts/test_feedback_placeholder.py' que ejecutó dos kickoffs contra Ollama con 'feedback_humano=""` (160.8s, 15 RF + 6 RNF) y con contenido (198.5s, 18 RF + 8 RNF). CrewAI 1.14.2 interpola correctamente el string vacío sin necesidad de marcador inocuo.
'_kickoff_requisitos_con_gate_humano' envuelve a '_kickoff_requisitos_con_reintentos`. Simétrico con la organización ya existente de helpers privados.
##### Reintentos automáticos: reset entre regeneraciones humanas
- Un artefacto puede, en el peor caso, generarse hasta 12 veces. Cada regeneración humana arranca con presupuesto fresco de 3 reintentos automáticos. El 'run_summary.json' registra el contador de la **última** regeneración, no el acumulado. Si en algún momento se necesita el acumulado para la memoria, se añadirá un campo 'reintentos_automaticos_total' aparte; ahora no se necesita.
##### 'duracion_s_gate_humano`: acumulación entre regeneraciones
- `+=` tras cada llamada a 'human_gate()`. Refleja tiempo humano total invertido en gates de esta fase, no solo el del gate aceptado final. Coherente con 'duracion_s_ejec' que ya acumula entre intentos del LLM.
##### Bug latente arreglado de paso
- '_escribir_artefactos_requisitos' rellenaba 'regeneraciones_previas' del frontmatter con un 0 hardcodeado. Ahora lee 'status.regeneraciones_humanas`.Verificado en el Run de validación: 'regeneraciones_previas: 1' aparece correctamente tras la regeneración.
##### Naming de attempts entre regeneraciones
- '_guardar_intento_fallido' ahora nombra los archivos como 'fase01_regen<N>_intento<M>.txt`. Evita pisar attempts entre regeneraciones humanas distintas. La carpeta '_attempts/` queda vacía si la fase fue limpia (intento 1 OK), comportamiento aceptable.


## 2026-05-08 — Alternativa oficial descartada: `@human_feedback' nativo de CrewAI
CrewAI ofrece la opción 'human_input=True' en tareas, que pausa la ejecución y solicita feedback al operador antes de cerrar la task. **Se descarta** para este pipeline por dos razones:
1. **Granularidad equivocada**. 'human_input' opera dentro de la task; el gate del Bloque 5 opera **entre fases**, sobre el artefacto consolidado y validado, no sobre la salida cruda de la task. Mover el gate dentro de la task confundiría capas.
2. **Trazabilidad documental**. El gate del pipeline produce un artefacto explícito (`gate_humano.md`) con frontmatter,  observaciones y acción, que queda en disco como evidencia del Run. 'human_input' opera con un 'input()` simple cuyo contenido no se persiste de forma estructurada. Para un experimento con evidencia auditable, el gate explícito en disco es indispensable.


## 2026-05-08 — Observación sobre la dinámica del feedback
#### Tres Runs ejecutados dentro del Flow para validación end-to-end
Run de validación combinada (Run 6)`run_2026-05-08_22-18' cubrió rechazado → regeneración → aceptado. Acción del gate de rechazo: "todos los requisitos funcionales con prioridad 'Alta'". La regeneración obedeció la instrucción específica, **pero también reescribió el registro completo**: pasó de 33 a 29 requisitos totales (caída notable en RNF, de 7 u 8 a 3). Esto **no es bug** del feedback ni del pipeline; es propiedad del enfoque elegido:
- El kickoff es una nueva generación desde cero, no una edición incremental. El modelo no ve el JSON anterior; solo ve brief + reglas del prompt + bloque de feedback. Reescribe todo el registro porque eso es lo único que sabe hacer.
- En consecuencia, el "feedback humano de regeneración" en este pipeline funciona como **reformulación del problema**, no como edición. La operadora no corrige el artefacto; reformula la tarea y el modelo la rehace.
- **(Run 6)`run_2026-05-08_22-18`**: rechazado → regeneración → aceptado. 29 RF + 3 RNF. 'regeneraciones_humanas=1`, 'gate_decision=aceptado' 'duracion_s_gate_humano=327.7s' (suma de los dos gates), 'regeneraciones_previas=1' en frontmatter. "INSTRUCCIONES DE REGENERACIÓN" visible en logs de la 2ª kickoff.
- **(Run 7)`run_2026-05-08_22-51`**: abort directo en consola sin tocar 'gate_humano.md`. 'resultado_final=abortado_en_gate`, 'gate_decision=abortado`, 'regeneraciones_humanas=0`, 'duracion_s_gate_humano=33.9s`. Exit code 1.
- El escenario "aceptado a la primera, sin regeneración" queda cubierto implícitamente por el primer ciclo del Run combinado, ya que la primera generación se completó sin reintentos antes del rechazo manual.

--

## 2026-05-09 — Subpaso 8d y 8e: YAMLs de la planificacion_crew
- Se seguira la logica implementada en requisitos_crew
- **Un único agente 'pm' (Project Manager del proyecto Hundidos)**, con role/goal/backstory anclados al proyecto. El backstory desarrolla las tres responsabilidades (backlog, plan de sprints, riesgos) con sus reglas específicas.
- 'config/tasks.yaml`: tres tasks secuenciales — 'construir_backlog`, 'planificar_sprints`, 'analizar_riesgos' — cada una con su 'description`, 'expected_output' (esquema JSON con ejemplo ilustrativo y reglas de formato innegociables) y 'agent: pm`.
- **Una crew, un PM, tres tasks** Un único 'output_pydantic' por task. Una task con tres outputs concatenados habría obligado a
  inventar un wrapper Pydantic artificial.
- **Validación de fase 02 al final** Un único gate humano evaluará los tres artefactos como bloque al final de fase 02. Si rechaza, regenera las tres tasks. Se reutiliza 'human_gate.py' sin modificar, y asume el coste de regenerar artefactos no afectados por el rechazo en favor de simplicidad del PMV. Reintento automático del kickoff completo si alguno de los validators (`validate_backlog_contenido`, 'validate_plan_sprints_contenido`, 'validate_riesgos_contenido`) falla. CrewAI ejecuta las tres tasks internamente; no es posible validar entre tasks.
- **Input al PM = solo registro de requisitos JSON, no el brief** Coherente con el principio de fronteras de responsabilidad explícita por agente: si el registro de fase 01 omitió algo, fase 02 también lo omite. La trazabilidad por fases se mantiene. El PM no consulta el brief.
- **`registro_requisitos_json' solo en la primera task** 'construir_backlog' recibe el JSON serializado con 'model_dump_json(indent=2)`. 'planificar_sprints' y
  'analizar_riesgos' lo reciben transitivamente vía 'context' de CrewAI. Decisión revisable si los Runs muestran desconexión del registro en las tasks 2 o 3; por defecto, sin redundancia para no inflar el contexto.
- **`{feedback_humano}` en las tres tasks** En primera generación, placeholder inerte (string vacío). En regeneraciones, las tres tasks leen el bloque "INSTRUCCIONES DE REGENERACIÓN (operadora humana)" producido por '_formatear_feedback_humano`, ya implementado.
- **`context' de 'analizar_riesgos`: backlog + plan_sprints** Riesgos se razona a la luz del plan real, no en abstracto. Permite identificar riesgos como dependencias cruzadas entre sprints o concentración excesiva de carga en un sprint.


## 2026-05-09 — Decisiones metodológicas sobre los riesgos del proyecto
**NO se incluyen en el artefacto los riesgos del proceso IA** (alucinaciones, desviación de alcance, variabilidad inter-Run).
- Razón: el PM produce un artefacto del proyecto Hundidos, no del meta-experimento. Mezclarlos rompería la simetría con el Registro de Riesgos del baseline humano. Los riesgos del proceso IA se documentan en 'pipeline_bitacora.md' y se discutirán como hallazgos del experimento en el capítulo 9 de la memoria.


## 2026-05-09 — Verificación
- Test de construcción ejecutado manualmente, la clase se construye sin errores, 1 agente con rol, 'Project Manager del proyecto Hundidos', 3 tasks con descripciones correctas, 'Process: sequential`.
- Ningún kickoff real ejecutado todavía


## 2026-05-09 — Subpaso 8f: integración de fase 02 al Flow + gate 2
Integrada la fase 02 (planificacion_crew) al pipelineFlow como listener encadenado tras fase 01, con gate humano único sobre los tres artefactos(backlog + plan_sprints + riesgos)
- human_gate acepta 'artefactos_md: list[Path]`. Permite gates sobre 1..N artefactos sin asumir cantidad. Para gate 1 y gate 3 (un solo MD) se pasa lista de un elemento; para gate 2, los tres MD.
- Recogida de outputs del kickoff por 'isinstance' sobre 'tasks_output[i].pydantic`, no por orden posicional. Robusto a reordenaciones futuras de @task; si algún slot queda sin rellenar o duplicado, devuelve (None, None, None) y el llamante lo trata como reintento automático.


## 2026-05-09 — Observación sobre la dinámica del gate_humano para planificacion
#### Dos Runs ejecutados dentro del Flow para validación end-to-end
Los dos Runs reales lanzados en este subpaso Run 8 (`run_2026-05-09_18-54`) con max_iter=3 y Run 9 (`run_2026-05-09_20-18`) con max_iter=15 fallaron antes de abrir el gate 2 por problemas de calidad del kickoff de fase 02, no por la integración del 8f. 
Síntomas observados:
- Con max_iter=3: degradación progresiva del backlog en cada reintento automático ("Maximum iterations reached. Requesting final answer."), de 13 historias bien razonadas a 1 historia genérica desligada del brief, con id_ejecucion inventado.
- Con max_iter=15: en el primer Run con este valor, intento 1 produjo un PlanSprints con 4 historias del backlog sin asignar; intento 2 produjo un JSON con cascada de llaves de cierre (desborde del contexto del modelo) que CrewAI no pudo parsear, atrapando al proceso en un bucle interno de reparación que requirió aborto manual.
- Hipótesis a explorar: ampliar 'num_ctx' en el Modelfile de 8192 a 16384 (el output de las tres tasks combinadas se aproxima al límite actual y el modelo desborda), reformular las task descriptions para reducir tokens del prompt, o reducir el alcance de las tasks (p.ej. backlog más conciso, sin criterios de aceptación tan extensos).
- En Run 9 (`run_2026-05-09_20-18) la fase 01 produjo un registro con duplicados (RF-35 y RF-36 idénticos) y RNF escasos, peor que en Runs del 8c. No se ha tocado nada de fase 01 en el 8f, así que es variabilidad del 7B. 
- Si lo anterior no basta, reconsiderar el mínimo del backlog (11 → 8) como mejora documentada.

--

## 2026-05-10 — Cierre del 8f y decisión metodológica: migración de fase 02 a modelo cloud
Lo que NO se logró cerrar es un Run end-to-end con gate 2 abierto y aceptado: los Runs reales fallaron sistemáticamente en el kickoff de fase 02 antes de abrir el gate(outputs malformados al acercarse al límite de contexto del modelo, cascadas de llaves de cierre, IDs inventados, tasks que olvidan partes del input, etc). Tras tres sesiones de calibración (subiendo max_iter, ampliando num_ctx, revisando prompts de las tasks), se concluye que el problema no es de prompt ni de parámetros: es un mismatch estructural entre el modelo qwen2.5-coder:7b ejecutado en una RTX 3050 Laptop con 4 GB de VRAM y la carga de fase 02 (tres tasks encadenadas con esquemas Pydantic complejos y output JSON extenso). Por tanto, se toma la decisión metodológica de **migrar el modelo de fase 02 a una API cloud, manteniendo fase 01 con el modelo local**. La decisión se documentara en la memoria.
- El modelo de fase 02 (PM) pasa a ejecutarse contra una API cloud.
- El perfil "default" del pipeline_config.yaml se mantiene apuntando a Ollama hundidos-analista para el Analista de fase 01.
- Se añade un perfil "pm" que apunta al modelo cloud.
- llm_factory.py se generaliza para soportar dos providers (Ollama local + cloud) y leer la API key desde variables de entorno.
- El manifest del Run y el run_summary.json registran qué modelo se usó en cada fase (trazabilidad por perfil).
- La arquitectura del Flow, los gates, los validators, los renderers, los schemas, las tasks YAML, la integración del 8f. Todo intacto.
- Fase 01 sigue local.
- El experimento sigue siendo "pipeline IA híbrido humano-LLM". El brief y la metodología no exigen ejecución 100% local. Lo que se documenta como hallazgo es que las restricciones de hardware locales (4 GB VRAM en GPU consumer) imponen un límite práctico al modelo que puede sostener la fase con mayor carga estructural.
- La decisión refuerza una propiedad del experimento: el pipeline híbrido es viable ante restricciones de hardware mediante uso selectivo de modelos cloud para fases de mayor exigencia.


## 2026-05-10 — Cierre end-to-end del 8f
#### Dos Runs ejecutados dentro del Flow para validación end-to-end
**Run 10 'run_2026-05-10_10-50`**: cadena completa fase 01 → fase 02 → cierre,con gate 1 y gate 2 aceptados, sin reintentos automáticos ni regeneraciones humanas, 'resultado_final = "completo"`.
- Fase 01(gate humano incluido): Total Run < 4 minutos (vs. 30+ minutos abortados con modelo local).
  - Tiempos:73.4 s.
  - Artefactos producidos: 20 RF + 7 RNF
  - Configuración usada: ollama/hundidos-analista:latest (local)
- Fase 02(gate humano incluido)
  - Tiempos:109.7 s
  - Artefactos producidos: 26 HU en backlog, 3 sprints, 10 riesgos. 6 archivos físicos en '02_planificacion/` (backlog, plan_sprints, riesgos en JSON + MD), todos pasaron validators y revisión humana.
  - Configuración usada: API key de Claude Haiku 4.5 en .env.

--

## 2026-05-11 — Subpaso 1a: integración de fase 03 (Arquitectura) + Gate 3
- Se reutiliza toda la logica anterior construida en requisitos_crew y planificacion_crew
- Se añade un perfil 'architect' en 'pipeline_config.yaml`, apuntando al mismo modelo cloud usado por fase 02 (`anthropic/claude-haiku-4-5`). Motivo: la decisión metodológica del 8f demostró empíricamente que las fases con salida estructurada compleja son más estables en cloud que en el modelo local qwen2.5-coder:7b bajo la restricción de 4 GB VRAM. Se mantiene fase 01 en Ollama local.
- 'arquitectura_crew' se implementa como single-task. Se descarta dividir en subtasks de modelos/rutas/plantillas para no reintroducir sobreingeniería ni dependencias 'context' innecesarias. El objetivo es PMV funcional y trazable, no arquitectura perfecta.
- Se pasan los cuatro artefactos aceptados: 'registro_requisitos`, 'backlog`, 'plan_sprints' y 'riesgos`. Sobre los riesgos la
  justificación: los riesgos aceptados informan decisiones técnicas prudentes (PayPal, contra-reembolso, SQLite, seed data, correo, Docker), sin añadir
  alcance funcional.
- Al existir una sola task, todo entra por 'inputs' del kickoff (`registro_requisitos_json`, 'backlog_json`, 'plan_sprints_json`, 'riesgos_json`, 'feedback_humano`, 'run_id`).
- El backlog y el plan de sprints delimitan el alcance implementable. El registro de requisitos se conserva como contrato semántico y fuente de reglas de dominio, pero no autoriza al Arquitecto a inventar funcionalidades que no estén justificadas por historias de usuario.
- No se modifica 'DisenoTecnico`. La riqueza adicional que permite el modelo cloud se pide dentro de los campos ya existentes: 'stack`, 'apps_django`, 'modelos`, 'rutas`. No se añaden campos como 'plantillas`, 'servicios' o 'flujo_pago' para evitar cambiar el contrato congelado.


## 2026-05-11 — Ejecución de la fase 03 - Arquitectura dentro del Flow para validación end-to-end
**Run 11 'run_2026-05-11_13-11`** Cadena completa fase 01 → gate 1 → fase 02 → gate 2 → fase 03 → gate 3 → cierre, con 'resultado_final = "completo"`.
Resumen:
  - Fase 01: gate aceptado, 0 reintentos automáticos, 0 regeneraciones humanas.
  - Fase 02: gate aceptado, 0 reintentos automáticos, 0 regeneraciones humanas.
  - Fase 03: gate aceptado, 0 reintentos automáticos, 0 regeneraciones humanas.
  - Duración de ejecución de fase 03: 23.1 s.
  - Artefactos producidos: '03_arquitectura/diseno_tecnico.json' y '03_arquitectura/diseno_tecnico.md`.

**Run 12 'run_2026-05-11_13-31`** Cadena completa con gate 1 y gate 2 aceptados, primer diseño técnico rechazado en Gate 3, regeneración de fase 03 y posterior aceptación del diseño regenerado. 'resultado_final = "completo"`.
Resumen:
  - Fase 03: 'regeneraciones_humanas = 1`.
  - Fase 03: 'reintentos_automaticos = 0`.
  - Fase 03: 'gate_decision = "aceptado"`.
  - Duración acumulada de ejecución de fase 03: 35.1 s.
  - El 'gate_humano.md' final documenta aceptación tras comprobar mayor detalle en rutas, modelos y archivos principales.

La fase 03 queda integrada y validada mecánicamente y por flujo real. El Run ya no cierra tras fase 02: cierra tras Gate 3. El pipeline produce 'diseno_tecnico.json' y 'diseno_tecnico.md`, permite aceptar/rechazar/abortar en Gate 3 y respeta la política de regeneraciones humanas definida en el spec.


## 2026-05-11 — Plan de cierre (Subpasos 1a, 1b) end-to-end tras fase 03
- Se reutiliza toda la logica anterior construida en requisitos_crew, planificacion_crew y arquitectura_crew
- No habrá gates humanos entre sprints, conforme al spec. La supervisión humana queda en gates 1, 2 y 3.
- El Desarrollador implementará lo planificado sprint a sprint usando 'diseno_tecnico.json`, el backlog del sprint correspondiente, el código previo y el review automático del sprint anterior cuando exista.
- Si un sprint genera código pero 'manage.py check' falla, se registra la incidencia en el review y el Run continúa. Si el LLM no produce una entrega
  válida tras los reintentos automáticos, se considera fallo de generación y el Run puede abortar por límite.
- Los backlogs por sprint se derivarán de forma determinista tras Gate 3 aceptado y vivirán en las carpetas propias de cada sprint (`04_sprint_1`, '05_sprint_2`, '06_sprint_3`), para alinearse con la tabla de artefactos del spec.
- El perfil 'developer' usará modelo cloud por continuidad metodológica con PM y Arquitecto, evitando que la limitación local de hardware sea el factor dominante en la fase de generación de código.
- La derivación valida defensivamente que todas las historias del plan existan en el backlog, que no haya historias duplicadas entre sprints y que no queden
  historias sin asignar.
- El artefacto nuevo 'BacklogSprint' se mantiene como contrato Pydantic para que la fase de desarrollo reciba un subconjunto claro del backlog aceptado.
- Se añade renderer Markdown para que cada backlog de sprint sea inspeccionable por la operadora y reutilizable por el Desarrollador.
- Actualizacion del 'verify_pipeline.py' se amplía con el paso 14. La ejecución completa desde el runtime empaquetado vuelve a quedar limitada por la ausencia de 'yaml' en ese entorno externo, igual que en verificaciones anteriores; debe ejecutarse en el entorno del proyecto para validar todos los pasos.


## 2026-05-11 — Subpaso 1c: DesarrolloCrew aislada
- El Desarrollador usa perfil cloud 'developer`, con el mismo modelo que PM y Arquitecto (`anthropic/claude-haiku-4-5`) y temperatura documentada 0.0 para
  reducir variabilidad en la ejecución medida.
- La salida del agente no escribe directamente en disco. Devuelve una 'EntregaSprint' Pydantic con 'ArchivoCodigo { path, contenido }`.
- Los paths de 'ArchivoCodigo' son relativos a la carpeta 'codigo/` del sprint activo. Se rechazan rutas absolutas, rutas vacías y rutas con `..`.
- El desarrollo se mantiene incremental: sprint 1 debe entregar la base Django ejecutable (`manage.py`, 'settings.py`, 'urls.py`); sprints 2 y 3 podrán
  devolver solo archivos nuevos o sobrescritos, porque partirán de la copia del código del sprint anterior cuando se integre el Flow.
- No se añaden gates humanos entre sprints.


## 2026-05-11 — Subpaso 1d: validación de arranque y review automático
- El objetivo principal del review es comprobar si cada historia de usuario pedida deja señales en el código entregado; si no aparecen señales, la historia se marca como 'ausente`.
- La validación de arranque ejecuta 'python manage.py check' dentro de la carpeta 'codigo/` del sprint activo y registra 'ok`, 'returncode' 'stdout_resumen`, 'stderr_resumen`, 'timeout_s' y si hubo timeout.
- Un fallo de arranque no aborta el Run por sí mismo. Se registra en el review para que el siguiente sprint pueda leer la incidencia.
- El review automático es heurístico y factual: clasifica cada historia como 'ok`, 'parcial' o 'ausente' según coincidencias de título, descripción y criterios de aceptación en paths y contenidos de archivos.
- La heurística no pretende certificar calidad funcional completa; solo deja evidencia repetible de cobertura detectable por historia.


## 2026-05-11 — Subpaso 1e: integración estática de los tres sprints al Flow
- Integrada la secuencia de desarrollo por sprints en 'pipelineFlow`, todavía sin añadir Closer ni validación final. El grafo queda extendido como: fase 01 → fase 02 → fase 03 → sprint 1 → sprint 2 → sprint 3 → cierre.
- Se mantienen tres listeners separados: 'ejecutar_sprint_1`, 'ejecutar_sprint_2' y 'ejecutar_sprint_3`, para preservar trazabilidad por fase y reflejar cada sprint en 'fases_status`.
- No hay gates humanos entre sprints. La decisión humana sigue limitada a gates 1, 2 y 3.
- El código es incremental: sprint 1 crea su 'codigo/`; sprint 2 copia el 'codigo/` de sprint 1 antes de aplicar su entrega; sprint 3 copia el 'codigo/` de sprint 2 antes de aplicar su entrega.
- El Desarrollador devuelve 'EntregaSprint`; el Flow escribe 'entrega_sprint_N.json' y aplica los archivos en 'codigo/` validando rutas relativas. Se bloquean rutas absolutas, rutas con `..` y rutas tipo 'C:/...`.
- Si la generación de una 'EntregaSprint' válida agota reintentos, el Run aborta por límite. Si 'manage.py check' falla, no aborta: queda registrado en 'review_sprint_N.json/md`.
- El cierre del Run pasa a escuchar al sprint 3.


## 2026-05-11 — Verificación de 1e y decisión sobre pruebas sprint-only
- Los sprints quedan integrados en el Flow oficial, pero un Run metodológico completo no debe saltar gates 1, 2 y 3 porque forman parte del protocolo
  congelado.
- Se mantiene la decisión de no copiar automáticamente a 'product/` durante el Run. El producto final evaluable del Run vive en 'runs/run_X/06_sprint_3/codigo/`; 'product/` solo se actualizaría después por decisión manual de la operadora.

---

## 2026-05-12 - Ejecución completa hasta fase de desarrollo
**Run 13 'run_2026-05-12_13-29'** 
- La ejecución avanzó correctamente por fase 01 → Gate 1 → fase 02 → Gate 2 → fase 03 → Gate 3. Los tres gates humanos fueron aceptados sin regeneraciones. Tras Gate 3, el Flow derivó correctamente los backlogs deterministas de los tres sprints. El fallo apareció al iniciar '04_sprint_1`, durante la llamada a 'DesarrolloCrew`. Los tres intentos automáticos del Sprint 1 fallaron con error de validación Pydantic sobre 'EntregaSprint`: *`Invalid JSON: EOF while parsing a string`*
- El error aparece cuando el modelo estaba generando contenido de archivos Django dentro del JSON y la salida quedó truncada. No se llegó a producir una 'EntregaSprint' válida, por lo que el Flow no escribió 'entrega_sprint_1.json`, no aplicó archivos en 'codigo/` y no generó review del sprint.
- El contrato actual de desarrollo exige devolver archivos completos dentro de un único JSON 'EntregaSprint`. Para un Sprint 1 con 11 historias y una base Django completa, la salida supera el tamaño práctico configurado para el perfil 'developer' (`max_tokens: 8192`). El fallo se debe a la combinación de contrato de salida grande + structured output + límite de generación.
- 'abortado_por_limite' en '04_sprint_1`, con 3 reintentos automáticos consumidos. El Run queda registrado como fallo técnico del pipeline.

Se evaluaron varias soluciones: aumentar 'max_tokens' del perfil 'developer`, cambiar a un modelo mas capaz, dividir 'EntregaSprint' por partes o por archivo, permitir escritura directa con herramientas, o introducir un Sprint 0 de scaffold. Finalmente se decide aplicar una solucion acotada: aumentar 'developer.max_tokens' de 8192 a 32768 y anadir un paso '03b_scaffold' generado por LLM antes de Sprint 1. El scaffold crea solo la base Django ejecutable; Sprint 1 parte de ese codigo y se concentra en funcionalidades del backlog. La decision se justifica porque reduce el tamano del JSON del Sprint 1, conserva la trazabilidad del pipeline y se parece a la practica seguida en el proyecto humano, donde se partio de una plantilla por restricciones de tiempo.

**Run 14 'run_2026-05-12_15-34`**
- Tras introducir '03b_scaffold' y aumentar 'developer.max_tokens' a 32768. El flujo avanzó correctamente por Fase 01 → Gate 1 → fase 02 → Gate 2 → fase 03 → Gate 3. 
- El fallo apareció en '03b_scaffold`. A diferencia del Run anterior, no se produjo truncamiento de JSON. Los tres attempts contienen una 'EntregaSprint' estructuralmente válida con código Django generado. Sin embargo, la validación determinista rechazó la entrega porque varios archivos tenían 'contenido=""`.
- Los archivos vacíos detectados eran principalmente '__init__.py' y `.gitkeep`, que son archivos válidos y habituales en proyectos Python/Django. Por tanto, el bloqueo no se debe a ausencia de generación de código, sino a una regla de validación demasiado estricta: 'validate_entrega_sprint_contenido' no distingue entre archivos vacíos inválidos y archivos marcador legítimamente vacíos.
- 'abortado_por_limite' en '03b_scaffold`, con 3 reintentos automáticos consumidos. No se escribió 'entrega_scaffold.json' ni se aplicaron archivos a '03b_scaffold/codigo/`, porque el Flow solo escribe la entrega después de superar validación.

Ajustar la validación para permitir contenido vacío en archivos marcador seguros (`__init__.py`, `.gitkeep`) y mantener la exigencia de contenido no vacío para archivos funcionales como `.py`, `.html`, `.txt`, `.yml`, etc.

**Run 15 `run_2026-05-12_16-48`**
- Tras ajustar `validate_entrega_sprint_contenido` para permitir archivos marcados vacíos, el flujo avanzó correctamente por hasta la fase `03b_scaffold` que generó una `EntregaSprint` válida, fue aceptada por la validación estructural y el Flow escribió `03b_scaffold/entrega_scaffold.json` y aplicó los archivos en `03b_scaffold/codigo/`. Sin embargo termino como Run abortado, saltandose por intentos agotados sprint 1-3. 
Resultado de `manage.py check` sobre el scaffold:
- `ok: false`
- `returncode: 1`
- Error principal: `ModuleNotFoundError: No module named 'django'`

-El fallo no demuestra todavía que el scaffold generado sea incorrecto. La comprobación de arranque usa el intérprete Python que ejecuta el pipeline (`sys.executable`) y ese entorno no tiene Django instalado. El propio scaffold sí incluye `requirements.txt` con `Django==3.2`, `Pillow==9.0.0` y `django-filter==21.1`, pero el Flow no instala esas dependencias antes de ejecutar `manage.py check`.
- Ademas el **Sprint 0 generó 81 archivos, incluyendo modelos, vistas, templates, servicios PayPal, login, administración y reservas**. Esto excede la intención metodológica del Sprint 0, que debía limitarse a una base Django mínima y ejecutable para reducir el tamaño de Sprint 1. No es embellecimiento manual ni escritura directa del LLM, pero sí indica que el prompt de scaffold necesita restringirse más.
- Run abortado en `03b_scaffold` antes del Sprint 1 por fallo de entorno de validación, no por fallo probado del código Django generado. Queda pendiente probar el scaffold en un entorno con dependencias instaladas y decidir si se ajusta el runner de Django, el prompt de Sprint 0 o ambos.

--

## 2026-05-13 - Decision de entorno fijo para validacion Django
Tras analizar el Run 15 (`run_2026-05-12_16-48`) y probar manualmente el codigo generado, se decide separar de forma explicita dos entornos:
- `.venv`: entorno de ejecucion del pipeline IA (CrewAI, Pydantic, proveedores LLM, orquestacion del Flow).
- `.venv_Test`: entorno fijo de validacion del producto Django generado por el pipeline.
La decision evita mezclar dependencias del pipeline con dependencias del producto generado. El fallo observado con `Pillow==9.0.0` bajo Python 3.11 en Windows se clasifica como problema de compatibilidad de entorno/dependencias, no como fallo probado del codigo Django generado. Para el TFG, el objetivo experimental no es medir la capacidad del pipeline para resolver instalacion de wheels nativos en Windows, sino comparar la generacion de un producto Django bajo un banco de pruebas estable y repetible.
Se decide que `django_runner.py` use un Python de validacion fijo:
- Primero, si existe, la variable `DJANGO_CHECK_PYTHON`.
- Si no se define, el interprete local `.venv_Test/Scripts/python.exe`.
- Si no existe un interprete de validacion, `manage.py check` devuelve `ok=False` con error claro. No se usara silenciosamente el Python del pipeline como fallback, para evitar falsos fallos como `ModuleNotFoundError: No module named 'django'`.
Tambien se mantiene la decision de que Sprint 0 (`03b_scaffold`) aborte antes de Sprint 1 si su `manage.py check` no arranca. Esta es una excepcion metodologica respecto a los sprints funcionales: en Sprint 1-3 un fallo de arranque queda registrado en el review y el Run continua, pero Sprint 0 es la plantilla base sobre la que se construyen todos los sprints posteriores.
Finalmente, se decide mantener Sprint 0 como scaffold minimo ejecutable. Se ajusta solo el prompt de Desarrollo para reforzar que Sprint 0 no debe implementar modelos, vistas, formularios, templates, login/registro, checkout, PayPal, panel admin custom, seed data ni servicios de negocio. No se anade todavia una validacion determinista de exceso de funcionalidad; si el modelo vuelve a generar demasiado codigo en Sprint 0, se reconsiderara un validador especifico.


## 2026-05-13 - Ejecución y comprobación manual del producto generado en Run 16 ('run_2026-05-13_06-57')
- Tras analizar Run 16, se decide conservarlo como run valido de construccion y maduracion del pipeline, pero no como run final medida para contrastar las hipotesis de la memoria. El flujo completo ya es viable:
- Fase 01 -> Gate 1 -> Fase 02 -> Gate 2 -> Fase 03 -> Gate 3 -> Sprint 0 -> Sprint 1 -> Sprint 2 -> Sprint 3 -> cierre.
- Sin embargo, el analisis manual posterior muestra que `resultado_final = completo` significa actualmente que el Flow llego al cierre, no que el producto generado cumpla automaticamente los criterios minimos de ejecucion y funcionalidad definidos en el brief.
- Inicialmente, la aplicación arrancaba con `python manage.py runserver 127.0.0.1:8000` y mostraba la home, pero varias rutas fallaban con errores `OperationalError` por tablas inexistentes (`catalog_barco`, `cart_cesta`, `accounts_clienteprofile`, etc.).
- Se comprueba que `python manage.py migrate` solo aplica migraciones internas de Django (`admin`, `auth`, `contenttypes`, `sessions`) y no crea tablas para las apps propias generadas (`accounts`, `catalog`, `cart`, `reservations`). El producto contiene modelos en `models.py`, pero no entrega migraciones propias para esas apps. Se ha ejecutado manualmente, para inspeccionar:
Preparación manual realizada:
python manage.py migrate --run-syncdb
python manage.py seed_data
python manage.py runserver 127.0.0.1:8000

Ruta / acción                        Resultado observado
/                                    OK. Carga la home.
/accounts/registro/ GET              OK. Muestra formulario de registro.
/accounts/registro/ POST             OK. Permite registrar usuario tras --run-syncdb.
/accounts/login/                     OK. Formulario accesible.
/barcos/                             OK. Muestra catálogo tras seed_data.
/barcos/<id>/                        OK  Parcial. Permite ver detalle y añadir barco a cesta.
/cesta/                              OK. Muestra cesta.
/cesta/ actualizar cantidad          OK. Recalcula subtotal automáticamente.
/cesta/ vaciar cesta                 OK. Vacía la cesta.
/reserva/paso1/                      OK. Permite escoger fechas.
/reserva/paso1/ validación fecha     OK. Rechaza fecha de inicio anterior a hoy.
/reserva/paso2/                      OK. Muestra datos de contacto.
/reserva/paso2/ validación email     OK. Valida correo electrónico.
/reserva/paso2/ validación teléfono  Incorrecta.
/reserva/paso3/                      ERROR. ValueError: Need 2 values to unpack in for loop; got 1.
/admin/                              No probado. No queda claro cómo acceder con usuario admin.
/admin-panel/                        No probado / pendiente.

- `migrate --run-syncdb` permite crear tablas para apps sin migraciones, y `seed_data` carga datos iniciales del catálogo. Esta preparación permite ver el comportamiento real de la aplicación más allá de la home.
- El warning `urls.W005` sigue presente por namespace `admin` duplicado.
- La validacion de telefono en paso 2 no cumple correctamente: el formulario contiene el campo, pero no valida formato.
- El acceso a `/admin/` y `/admin-panel/` queda pendiente de verificacion automatica completa.
- El producto contiene un usuario administrador de prueba creado por `seed_data`.


## 2026-05-13 - Discusion sobre decision sobre calidad, verificacion y sobreingenieria
La preocupacion inicial era si introducir un agente de calidad podia ayudar a comprobar si el producto cumplia lo minimo. Tras revisar las hipotesis de la memoria, se reformula el problema: no se busca un agente que juzgue calidad de forma subjetiva, sino un componente que verifique factual y repetiblemente si los minimos definidos se cumplen o no.
La alternativa adoptada es preparar una validacion final determinista, porque:
- produce evidencia repetible;
- no introduce variabilidad adicional de modelo;
- no altera el producto generado;
- encaja con la hipotesis H3 sobre contratos y validacion estructural;
- ayuda a operacionalizar H2 con criterios observables;
- evita convertir el cierre del pipeline en una fase abierta de correccion continua.
Se introduce una frontera metodologica clara:
- Todo ajuste realizado antes de la run final pertenece a la construccion/calibracion del instrumento experimental.
- Una vez congelado el protocolo final, no se modificaran prompts, codigo del pipeline ni producto generado hasta completar la run medida.
- Los fallos de la run final se registraran como resultados del experimento, no se corregiran durante la medicion.
- Cualquier modificacion posterior implicaria una nueva version del protocolo y una nueva run, no una correccion de la run final.


## 2026-05-13 - Actualizacion documental aplicada
Se actualiza `pipeline_specs.md` a version 1.2 en estado `en_revision`, no congelado. La spec pasa a distinguir explicitamente entre run de maduracion, run completo de Flow y run final medida. Tambien deja documentado que `validacion_final.json`, Closer y manifest completo siguen pendientes de implementar o reclasificar antes de congelar el protocolo final.


## 2026-05-13 - Implementacion inicial de validacion final
Se implementa una primera version determinista de la validacion final:
- nuevos modelos Pydantic para `ValidacionFinal`, `ReviewFinal`,
  resultados de comandos, rutas, migraciones y templates;
- nuevo modulo `utils/final_validator.py`;
- renderer `review_final.md` derivado del JSON;
- nueva fase `ejecutar_validacion_final` entre Sprint 3 y `cerrar_run`;
- escritura de `99_cierre/validacion_final.json` y `99_cierre/review_final.md`.
La validacion final trabaja sobre una copia temporal del codigo final para no modificar el entregable generado. El JSON incluye checks planificados, ejecutados y no ejecutados, de modo que en runs oficiales posteriores se pueda contar cuantas veces se ejecuto cada comprobacion y distinguir fallos del producto, del entorno o de bloqueo previo.


## 2026-05-13 - Implementacion y ajuste de prompt del Desarrollador: contrato de producto ejecutable
Se incorpora en `src/pipeline/crews/desarrollo_crew/config/tasks.yaml` el "Contrato de producto ejecutable Hundidos".
La decision es formularlo como regla general del entregable, no como parche especifico al fallo de Run 16. El contrato exige:
- preparacion estandar con `migrate`, `seed_data` y `runserver`;
- migraciones iniciales cuando se generen modelos propios;
- seed reproducible con datos minimos y usuarios de prueba;
- validaciones generales de formularios, con ejemplos minimos;
- rutas declaradas sin error 500;
- flujo de reserva robusto de paso 1 a paso 3;
- rutas principales inspeccionables.
Se mantiene un contrato propio, acotado al experimento y verificable por el validador determinista.
Se añade al ejemplo de `expected_output` una migracion inicial (`catalog/migrations/0001_initial.py`) para hacer visible al modelo que las migraciones forman parte del entregable, no de una preparacion manual posterior.

## 2026-05-13 - Analisis de Run 17 (`run_2026-05-13_15-33`)
Se analiza el nuevo run ejecutado tras incorporar la validacion final determinista y el contrato de producto ejecutable Hundidos en el prompt del Desarrollador.

Resultado operativo:
- El Flow termina correctamente con `resultado_final = completo`.
- El recorrido ejecutado es: Fase 01 -> Gate 1 -> Fase 02 -> Gate 2 -> Fase 03 -> Gate 3 -> Sprint 0 -> Sprint 1 -> Sprint 2 -> Sprint 3 -> Validacion final -> Cierre.
- Los tres gates humanos aparecen aceptados en `run_summary.json`, sin regeneraciones humanas y sin reintentos automaticos.
- Sprint 0 supera `manage.py check` con `ok=true`.
- Los sprints 1, 2 y 3 generan entregas validas, pasan `manage.py check` y el review automatico marca todas las historias pedidas como `ok`.
- La validacion final se ejecuta completa: 16 checks planificados, 16 ejecutados, 0 no ejecutados.

Resultado del producto:
- `validacion_final.json` marca `ok_global=false`.
- La clasificacion del validador es `parcial_con_incidencias`.
- Incidencias detectadas:
  - `/accounts/registro/` devuelve 404.
  - `/accounts/login/` devuelve 404.
- `manage.py check`, deteccion de migraciones propias, `manage.py migrate --noinput`, `manage.py seed_data`, `runserver`, `/reserva/paso3/`, `/admin/` y `/admin-panel/` superan los smoke tests definidos.

Interpretacion:
- El contrato de producto ejecutable mejora claramente los problemas detectados en Run 16: el producto ya entrega migraciones propias, `migrate` estandar funciona, `seed_data` existe y se ejecuta, el servidor arranca y la ruta de reserva paso 3 ya no falla en el smoke test.
- Las incidencias restantes parecen proceder de una desalineacion entre contrato/validador y producto generado: el validador exige `/accounts/registro/` y `/accounts/login/`, mientras el producto expone registro y login en raiz mediante `accounts.urls`.
- Los artefactos `gate_humano.md` presentan una incidencia de trazabilidad: los tres muestran `gate: 1` y timestamps inconsistentes con el cierre del run. `run_summary.json` conserva la evidencia operativa de aceptacion, pero esta incoherencia debe corregirse antes de congelar el protocolo.
- Este run demuestra que el instrumento experimental es mas solido, pero no debe clasificarse como run final medida porque `pipeline_specs.md` sigue en revision, `manifest.json` y Closer siguen pendientes, y `ok_global=false`.

Clasificacion:
- Run de maduracion avanzada / candidata tecnica descartada.
- No se usa como run final medida.

Decisiones antes de congelar:
- Alinear rutas minimas del contrato y del validador: decidir si las rutas oficiales son `/accounts/registro/` y `/accounts/login/` o `/registro/` y `/login/`.
- Corregir la trazabilidad de gates antes de ejecutar una run medida.
- Implementar o reclasificar formalmente `manifest.json`.
- Implementar o reclasificar formalmente el Closer documental.
- Decidir si se amplian los checks funcionales finales o si se mantienen como smoke tests minimos para evitar sobreingenieria.


## 2026-05-13 - Cierre de decisiones pre-Run 18
Tras revisar Run 17 y el capitulo 3 de la memoria, se cierran las siguientes decisiones antes de lanzar una run candidata formal:

- Se mantienen como rutas oficiales de autenticacion `/accounts/registro/` y `/accounts/login/`, porque ya forman parte del contrato ejecutable y del validador final. La correccion se aplica como aclaracion del contrato en el prompt del Desarrollador, no como cambio del validador para acomodar el resultado de Run 17.
- El gate humano pasa a generar una plantilla de `gate_humano.md` si no existe. La plantilla deja `decision` vacia para obligar a una decision formal de la operadora.
- Los campos `gate`, `fase` y `decision` del acta de gate pasan a validarse estrictamente. Los timestamps documentales (`timestamp_revision_inicio` y `timestamp_revision_fin`) se permiten para auditoria, pero no son fuente oficial de tiempo.
- La fuente oficial de tiempo humano de gate sigue siendo `duracion_s_gate_humano`, medido por el Flow desde la apertura del gate hasta el handshake `ok`.
- `manifest.json` se implementa como artefacto determinista en `99_cierre/manifest.json`. Su funcion es trazabilidad estructurada del run: hashes, modelos, versiones, fases, gates, artefactos y resumen de validacion final.
- El Closer se implementa como cierre documental determinista, sin LLM y sin corregir producto generado. Escribe `99_cierre/readme.md` y `99_cierre/lecciones_aprendidas.md`.
- La carpeta `99_cierre` se mantiene. No se renombra para evitar ruido metodologico y preservar la estructura ya documentada.
- Las metricas externas del estudio (M6 implementation rate, M7 pass-rate de suite comun y log estructurado de incidencias para M12-M16) no se implementan dentro del pipeline. Se definiran y ejecutaran fuera, aplicadas de forma comun al baseline y al producto IA.

La version 1.2 de `pipeline_specs.md` sigue en revision hasta probar el cierre completo en una run candidata. Si el cierre completo funciona y no aparecen fallos de pipeline, se podra congelar antes de la run final medida.

## 2026-05-13 - Ajuste de prompts pre-Run 18: rutas canonicas
Se revisa la instruccion de rutas tras detectar que una redaccion centrada en `/accounts/registro/` y `/accounts/login/` podia leerse como parche directo al fallo de Run 17.

- La regla se reformula como contrato general de rutas canonicas minimas del protocolo de validacion.
- Se permite que el producto incluya alias adicionales si mejoran la experiencia, pero no que sustituyan las rutas canonicas.
- La aclaracion se aplica tanto al Arquitecto como al Desarrollador, porque el DisenoTecnico condiciona las rutas que despues implementa el sprint.
- No se cambia el validador final ni se ajusta el criterio para acomodar el producto de Run 17.
- Requisitos y Planificacion se mantienen sin cambios: sus prompts siguen actuando sobre cobertura del brief y particion exacta de historias en tres sprints, no sobre rutas concretas de implementacion.

## 2026-05-14 - Analisis de Run 18 y decision de migrar fase 01 a cloud
Se ejecuta Run 18 (`run_2026-05-13_23-50`) con la configuracion previa: fase 01 en modelo local `ollama/hundidos-analista:latest` y fases posteriores en cloud. La ejecucion se detiene en el gate humano de requisitos tras consumir las regeneraciones disponibles sin obtener un RegistroRequisitos aceptable.

Patron observado en fase 01:
- Intento 1: cobertura funcional amplia, pero inversion semantica bloqueante en la tasa de combustible. El artefacto indicaba que la tasa de 50 EUR/dia se aplicaba a barcos de categoria `velero`, cuando el brief dice lo contrario: 50 EUR/dia salvo `velero`, donde la tasa es 0 EUR.
- Intento 2: corrige la tasa de combustible y mejora los RNF, pero pierde cobertura funcional relevante: inicio de sesion durante reserva con recuperacion de cesta, catalogo/busqueda, modificacion de cesta, recordatorio por correo y otros criterios obligatorios.
- Intento 3: reduce el registro al minimo cuantitativo de 15 RF y omite areas completas del brief, especialmente catalogo, busqueda, ficha de barco y reglas de dominio.
- Intento 4: recupera cobertura, pero desplaza RNF a RF y mantiene errores bloqueantes: atribuye al cliente el cambio de estado de reservas, omite la declaracion explicita de los cuatro estados y deja incompletas reglas de cancelacion, filtros y ficha de barco.

Interpretacion metodologica:
El feedback humano correctamente formulado mejora partes concretas del artefacto, pero el modelo local no mantiene simultaneamente cobertura global, fidelidad semantica y clasificacion RF/RNF bajo un brief largo. Cada regeneracion corrige algunos defectos y desplaza otros. El problema ya no se interpreta como una carencia puntual de prompt, sino como una limitacion del modelo local para sostener el contrato completo de fase 01.

Riesgo metodologico:
Seguir endureciendo el prompt del Analista con instrucciones cada vez mas especificas aumentaria el riesgo de convertir el instrumento en una coleccion de parches ad hoc derivados de runs anteriores. En particular, podria corregir sintomas concretos sin mejorar la capacidad general de extraer requisitos desde el brief.

Decision:
Migrar tambien la fase 01 al modelo cloud usado por el resto de fases (`anthropic/claude-haiku-4-5`) antes de congelar el protocolo final. La decision se toma durante la maduracion del pipeline, no durante una run final medida. No se modifica el brief, no se relajan gates, no se cambia el validador para acomodar el resultado de Run 18 y no se edita manualmente ningun artefacto producido por el LLM.

Justificacion:
El objetivo del TFG no es evaluar el modelo local como variable independiente, sino evaluar un pipeline humano-LLM con contratos, gates humanos, trazabilidad y validacion determinista. Mantener un modelo local que no produce de forma estable el artefacto base amenaza la validez del instrumento experimental. La migracion completa a cloud reduce esa amenaza y evita seguir anadiendo reglas hiperlocales al prompt.

Cambios asociados antes de la siguiente run candidata:
- Actualizar `pipeline_config.yaml` para que el perfil `default` del Analista use Anthropic.
- Actualizar comentarios/documentacion interna que todavia describen `default` como Ollama local.
- Ajustar redacciones de prompts previamente identificadas para evitar lenguaje de "validador" dentro del rol generativo: hablar de contrato publico, ejecucion reproducible y schema, no de trucos para pasar validacion.
- Corregir la contradiccion de Planificacion: el PM no debe referirse a subsecciones del brief original como fuente propia; debe cubrir las areas funcionales reflejadas en el registro aceptado.

## 2026-05-14 - Analisis de Run 19 (`run_2026-05-14_02-35`)
Tras migrar fase 01 a cloud y aplicar los ajustes de redaccion previos, se ejecuta Run 19 como run tecnico de verificacion pre-congelacion, no como run final medida.

Resultado operativo:
- El Flow completa el recorrido completo: Fase 01 -> Gate 1 -> Fase 02 -> Gate 2 -> Fase 03 -> Gate 3 -> Sprint 0 -> Sprint 1 -> Sprint 2 -> Sprint 3 -> validacion final -> cierre.
- Fase 01 usa `anthropic/claude-haiku-4-5` y genera un RegistroRequisitos aceptable en el primer intento. Esto contrasta con Run 18, donde el modelo local no logro mantener cobertura/fidelidad bajo regeneraciones.
- `run_summary.json` marca `resultado_final = completo`, con gates humanos aceptados y sin regeneraciones humanas.
- Los sprints tardan mas de lo esperado respecto a runs previos, especialmente Sprint 1, que consume 1 reintento automatico. Se registra como observacion operativa, no como fallo funcional.

Resultado de validacion final:
- `99_cierre/validacion_final.json` y `99_cierre/review_final.md` se generan correctamente.
- `ok_global = false`.
- Clasificacion: `parcial_con_incidencias`.
- Checks tecnicos basicos correctos: `manage.py check`, migraciones propias, `migrate --noinput`, `seed_data` y `runserver`.
- Incidencias automaticas detectadas:
  - `/cesta/` no supera smoke test. El validador lo reporta como `TimeoutError`.
  - `reservations/checkout_step3.html` no renderiza por `ImportError`: el validador intenta importar `CheckoutStep3Form`, pero el producto generado define `ReservationStep3Form`.

Comprobacion manual del producto:
- Preparacion manual estandar funciona: `python manage.py migrate --noinput`, `python manage.py seed_data`, `python manage.py runserver`.
- `seed_data` documenta credenciales por stdout:
  - administrador: `admin@hundidos.com / admin123`
  - cliente: `cliente@hundidos.com / cliente123`
- Home, catalogo, filtros basicos, detalle de barco, registro, login, perfil, seguimiento y varias rutas principales responden.
- `/cesta/` falla con error 500. La causa real observada manualmente es `TemplateSyntaxError: Invalid filter: 'mul'` en `templates/cart/view.html`, no un timeout funcional puro. Esto bloquea la cesta y por arrastre el flujo normal de reserva desde catalogo.
- El enlace superior de logout usa GET hacia `/accounts/logout/` y devuelve 405. El logout desde perfil si funciona porque usa POST. Por tanto, cierre de sesion queda parcial: existe, pero no funciona desde toda la navegacion visible.
- `/admin-panel/` redirige a `/` cuando no hay usuario admin autenticado. Queda pendiente comprobar panel propio tras login con credenciales admin.
- El flujo de reserva no queda validado de extremo a extremo porque la cesta falla antes de avanzar por el recorrido normal.

Observaciones sobre pago:
- El producto generado contiene dos metodos de pago (`paypal` y `contra_reembolso`) en formulario/modelo.
- PayPal no llama a la API real/Sandbox. El flujo simula el pago redirigiendo a `PayPalCallbackView`, que marca la reserva como `PAGADO`, genera historial, envia confirmacion y limpia cesta/sesion. Esto puede considerarse una simulacion funcional de Sandbox, pero no una integracion real con credenciales/API de PayPal.
- Contra-reembolso crea la reserva, la deja en `PENDIENTE_DE_PAGO`, envia confirmacion y limpia cesta/sesion. No requiere pasarela externa; es coherente como flujo local, siempre que el recorrido hasta paso 3 funcione.

Incidencias del cierre documental:
- En `99_cierre` no aparecen `manifest.json`, `readme.md` ni `lecciones_aprendidas.md`, aunque estaban previstos como Closer determinista.
- El codigo actual contiene `_escribir_cierre_documental()`, pero Run 19 no produjo esos artefactos. Debe investigarse antes de congelar: posible ejecucion con version no actualizada, fallo silencioso, o ruta de cierre no ejecutada como se esperaba.
- La carpeta `logs/` existe pero queda vacia. La evidencia util del run esta actualmente en consola, `_attempts/`, `run_summary.json`, reviews de sprint y `validacion_final.json`.

Cambios propuestos antes de congelar, sin tocar prompts todavia:
- Registrar Run 19 como run tecnico pre-congelacion descartado como run final medida.
- No corregir manualmente el producto generado de Run 19.
- Revisar el cierre documental para garantizar que siempre se escriban `99_cierre/manifest.json`, `99_cierre/readme.md` y `99_cierre/lecciones_aprendidas.md`, o que cualquier fallo quede registrado explicitamente.
- Ampliar `run_summary.json` con totales: duracion de ejecucion, duracion de gates humanos, total contabilizado, `ok_global` y clasificacion de la validacion final.
- Mejorar la validacion final de forma general, no como parche de producto:
  - capturar y reportar errores 500 con causa real cuando una ruta falla;
  - verificar logout observable desde la UI si existe un enlace visible;
  - revisar el check de `CheckoutStep3Form`, porque esta acoplado a un nombre interno no exigido por el contrato;
  - valorar un smoke test de flujo minimo de reserva solo si puede formularse como criterio comun y no como sobreingenieria.
- No anadir instrucciones especificas al prompt del Desarrollador del tipo "no uses filtro mul". Eso seria parche ad hoc al resultado de Run 19.
- Decidir si la integracion PayPal exigida para la run final debe ser simulacion local documentada o llamada real al Sandbox. Esta decision debe cerrarse en protocolo antes de la run final, no deducirse del producto generado.

## 2026-05-14 - Decision pre-congelacion: review automatico incremental mejorado
Tras analizar Run 19 se plantea si anadir una fase/agente de correccion final para mejorar el producto generado. La preocupacion metodologica es legitima: en un desarrollo humano tradicional existe revision tecnica continua, integracion y correccion durante el proyecto, no solo una validacion final al terminar. Sin embargo, introducir ahora un agente corrector final con capacidad de modificar todo el codigo podria abrir una fase nueva dificil de acotar, reducir la comparabilidad con runs previos y acercarse a una correccion oportunista del producto.

Decision:
No se incorpora por ahora un agente LLM corrector ni una fase final abierta de "arreglar todo". En su lugar, se decide reforzar el `review_sprint_N` determinista e incremental, de forma que detecte errores ejecutables relevantes al final de cada sprint y los entregue como `review_anterior_json` al Desarrollador del sprint siguiente.

Justificacion metodologica:
- Simula una practica habitual de desarrollo: revision tecnica e integracion continua entre incrementos.
- Mantiene separacion de responsabilidades: el LLM Desarrollador genera/corrige codigo; el review determinista observa y registra incidencias; el Flow aplica archivos; el gate humano sigue limitado a fases 1-3.
- Evita introducir variabilidad adicional de un Revisor LLM antes de congelar.
- Refuerza H3: contratos y validacion estructural ayudan a coordinar un pipeline multiagente.
- Reduce el riesgo de descubrir fallos basicos solo al final, como ocurrio en Run 19 con `/cesta/` y el filtro de template `mul`.

Alcance del review automatico mejorado:
- Debe seguir siendo pragmatico y no excesivamente estricto. No debe bloquear por preferencias de estilo, nombres internos o detalles no exigidos por el contrato.
- Debe capturar fallos ejecutables que impiden usar el producto o romperian un flujo principal.
- Debe registrar incidencias claras, accionables y trazables en `review_sprint_N.json` y `review_sprint_N.md`.
- Debe permitir que el siguiente sprint corrija incidencias relevantes antes de implementar nuevas historias, sin modificar directamente el codigo generado.

Checks candidatos, formulados como criterios generales:
- Mantener `python manage.py check`.
- Si hay migraciones/modelos, comprobar que las migraciones propias existen y que `migrate --noinput` puede ejecutarse en una copia temporal.
- Ejecutar `seed_data` cuando exista y registrar credenciales emitidas por stdout si aparecen.
- Probar rutas relevantes disponibles hasta el sprint activo, no toda la aplicacion futura. Registrar status, redirecciones y excepciones reales.
- Renderizar templates criticas o modificadas en el sprint cuando sea posible, capturando errores de sintaxis de Django templates.
- Detectar errores 500 y reportar la excepcion raiz cuando sea posible, no solo timeout.
- Revisar navegacion visible basica cuando el HTML expone enlaces a rutas canonicas. Ejemplo general: si se muestra un enlace GET a una accion que la vista solo acepta POST, registrarlo como incidencia de navegacion/metodo.
- No acoplar el review a nombres internos de clases salvo que formen parte del contrato tecnico aceptado. El caso `CheckoutStep3Form` de Run 19 se considera demasiado acoplado si el contrato solo exige que el paso 3 sea funcional.

Limites explicitos:
- El review automatico mejorado no corrige codigo.
- No se anaden prompts especificos derivados de fallos concretos como "no uses filtro mul".
- No se convierte en una suite funcional exhaustiva ni sustituye la evaluacion final/manual.
- Si tras reforzar este review las incidencias siguen siendo dificiles de diagnosticar o corregir por el Desarrollador en el sprint siguiente, se valorara como segunda opcion un Revisor Tecnico LLM sin permisos de escritura, limitado a producir diagnostico estructurado.

Decisiones asociadas:
- PayPal: queda pendiente cerrar en protocolo si se exige integracion real con API Sandbox o simulacion funcional reproducible. Por coste, tiempo y estabilidad experimental, la opcion preferida es simulacion local documentada como flujo Sandbox.
- Credenciales seed: el producto puede emitirlas por stdout de `seed_data`, pero antes de congelar conviene que el cierre/manifest o README de cierre registren donde consultarlas.
- Run 19 no se usa como run final medida. Sirve como evidencia de que el pipeline cloud completa el Flow y de que el review incremental actual es insuficiente para detectar fallos ejecutables tempranos.



## 2026-05-14 - Desicion sobre paypal pagos 
PayPal Sandbox se evalúa como flujo simulado que produce reserva pagada, no como llamada real a API externa

## 2026-05-14 - Implementacion de controles pre-congelacion
Se implementan los cambios derivados del analisis de Run 19 sin modificar prompts ni codigo generado por el LLM.

Cambios aplicados:
- `review_sprint_N` se amplia con comprobaciones ejecutables incrementales en una copia temporal del codigo: `migrate --noinput`, `seed_data` si existe, compilacion de templates Django y smoke tests HTTP de rutas canonicas ya presentes.
- El review incremental registra incidencias accionables en JSON y Markdown mediante nuevos campos `rutas`, `templates` e `incidencias`.
- Se anade deteccion estatica general de navegacion GET hacia logout cuando la vista visible solo define POST.
- La validacion final deja de depender del nombre interno `CheckoutStep3Form`; ahora comprueba que la template critica cargue como template Django. Esto evita convertir una implementacion concreta en criterio metodologico.
- Cuando una ruta devuelve error 500 durante validacion final, se conserva el resumen de stderr/stdout del runserver para diagnosticar causa raiz.
- `run_summary.json` incorpora totales: `duracion_s_ejec_total`, `duracion_s_gate_humano_total`, `duracion_s_total_contabilizada` y resumen de `validacion_final`.
- El cierre documental queda endurecido: si falla la generacion normal de `manifest.json`, `readme.md` o `lecciones_aprendidas.md`, se escriben artefactos fallback con error explicito y se registra `logs/cierre_documental_error.json`.

Decision sobre `logs/`:
Se mantiene la carpeta. No se usa como duplicado de todos los artefactos, sino como sumidero de incidencias operativas del pipeline que no pertenecen al producto ni a una fase concreta. Por ahora el caso definido es el fallo del cierre documental. Si en futuras ejecuciones se decide capturar consola completa, debera hacerse como decision experimental separada para no inflar evidencia irrelevante.

## 2026-05-14 - Incidencia Run 20 en scaffold base
Run 20 (run_2026-05-14_11-32) llega correctamente hasta arquitectura y acepta los gates humanos de fases 01, 02 y 03. El aborto ocurre en `03b_scaffold`: el scaffold propuesto contiene `hundidos/urls.py` con includes a `accounts.urls`, `catalog.urls`, `cart.urls`, `reservations.urls`, `payments.urls`, `tracking.urls` y `admin_panel.urls`, pero no entrega los archivos `urls.py` minimos de esas apps. Django falla al importar la configuracion de URLs durante `manage.py check`, por lo que el Flow aborta antes del Sprint 1.

Clasificacion metodologica:
- No es un fallo de requisitos, planificacion ni arquitectura aceptada.
- No es consecuencia de haber cambiado el texto "manage.py check" en el prompt: el prompt puede hablar de base Django valida, pero el control determinista de arranque sigue siendo necesario.
- Es una inconsistencia Django general: no deben existir includes hacia modulos inexistentes.

Cambios aplicados:
- Se anade al prompt de sprint 0 una regla general: si el urls.py del proyecto usa `include('nombre_app.urls')`, debe entregarse un `urls.py` minimo en esa app con `urlpatterns = []`, o evitar el include hasta que exista la ruta real.
- Se refuerza `validate_entrega_sprint_contenido` para detectar includes a modulos `urls.py` inexistentes como contenido insuficiente. Asi el fallo consume reintento automatico de la crew, en vez de abortar despues por `manage.py check`.
- Se corrige el manifest normal para convertir fechas/datetimes cargados desde YAML a valores JSON serializables. El fallback `manifest_error_v1` funciono correctamente y dejo trazabilidad del error.

## 2026-05-14 - Analisis de Run 21 (`run_2026-05-14_16-05`)
Run 21 completo de Flow tras los cambios de Sprint 0 y cierre documental. No se considera valido como entrega funcional para la memoria, aunque si es valido como evidencia de fallo trazable del pipeline.

Resultado operativo:
- El Flow completa todas las fases: requisitos, planificacion, arquitectura, scaffold, Sprint 1, Sprint 2, Sprint 3 y cierre.
- Los tres gates humanos iniciales quedan aceptados.
- `run_summary.json` marca `resultado_final = completo`.
- La validacion final se ejecuta, pero `ok_global = false`.
- Clasificacion final: `bloqueado_arranque`.
- Checks planificados: 16. Checks ejecutados: 6. Checks no ejecutados: 10.
- Incidencias totales: 15. Factores bloqueantes: 2.

Resultado de validacion final:
- `manage.py check` falla.
- `manage.py migrate --noinput` falla porque Django ejecuta previamente los system checks y estos ya fallan.
- `seed_data` falla por la misma razon: no llega a ejecutar el comando de negocio porque el proyecto no supera los checks de arranque.
- `runserver` no arranca, por lo que no se ejecutan los smoke tests de rutas (`/`, `/barcos/`, `/cesta/`, `/accounts/registro/`, `/accounts/login/`, `/reserva/paso1/`, `/reserva/paso2/`, `/reserva/paso3/`, `/admin/`, `/admin-panel/`).
- La template critica `reservations/checkout_step3.html` no existe; el producto generado usa `templates/reservations/step3.html`.

Comparacion con errores ya resueltos:
- En Run 19 (`run_2026-05-14_02-35`) los checks tecnicos basicos ya estaban resueltos: `manage.py check`, migraciones propias, `migrate --noinput`, `seed_data` y `runserver`.
- Por tanto, Run 21 representa una regresion respecto a Run 19 en los checks de arranque.
- La decision metodologica previa sigue siendo correcta: el prompt no debe decir "optimiza para pasar `manage.py check`"; debe pedir una base/producto Django valido y arrancable. El pipeline, en cambio, debe seguir ejecutando `manage.py check` como control determinista minimo.

Diagnostico tecnico probable:
- La arquitectura de Run 21 pide `reservations/services/paypal.py`.
- El codigo generado importa `requests` en `reservations/services/paypal.py`.
- El entorno fijo de validacion `.venv_Test` no contiene `requests`, y el producto final no entrega un `requirements.txt` que el validador instale o controle.
- Al importar `reservations.urls`, Django importa `reservations.views`; este importa `PayPalService`; y `PayPalService` importa `requests`. Si `requests` no existe, `manage.py check` falla antes de cualquier smoke test.
- El problema de `migrate`, `seed_data` y `runserver` es consecuencia en cascada del fallo de importacion durante `manage.py check`, no cuatro fallos independientes.

Regresion de validacion pendiente:
- La bitacora previa dice que la validacion final dejo de depender del nombre interno `CheckoutStep3Form`, pero `final_validator.py` todavia mantiene `TEMPLATES_CRITICAS = ["reservations/checkout_step3.html"]`.
- Esto ya no importa una clase interna, pero sigue acoplando la validacion a un nombre de template que no aparece en el contrato tecnico aceptado de Run 21, donde la arquitectura lista `templates/reservations/step3.html`.
- Debe corregirse como criterio general: validar la template asociada a la ruta canonica `/reserva/paso3/` o aceptar nombres canonicos equivalentes (`step3.html` / `checkout_step3.html`) derivados de las rutas del producto, no exigir un nombre historico unico.

Cambios necesarios antes de producir pruebas validas:
- Alinear la decision de PayPal simulado con arquitectura y desarrollo: no pedir ni generar un servicio que dependa de `requests` si la politica experimental es simulacion local sin llamada real a API externa.
- Si se permite una dependencia externa en el producto generado, definir contrato y validador para `requirements.txt`; si no, bloquear imports externos no presentes en `.venv_Test`.
- Cambiar `final_validator.py` para no fijar `reservations/checkout_step3.html` como unica template critica.
- Reforzar el review incremental para que un `ModuleNotFoundError` por dependencia externa aparezca como incidencia accionable en el sprint que introduce el import, antes de llegar al cierre.
- Mantener `manage.py check`, `migrate --noinput`, `seed_data` y `runserver` como checks deterministas obligatorios. No quitarlos del pipeline.

## 2026-05-14 - Analisis de Run 22 (`run_2026-05-14_16-53`)
Run 22 completo de Flow tras la correccion de la regresion de arranque observada en Run 21. No se considera todavia valido como run final medida, pero representa una mejora importante: el producto vuelve a ser arrancable y ejecuta todos los checks planificados.

Resultado operativo:
- El Flow completa todas las fases: requisitos, planificacion, arquitectura, scaffold, Sprint 1, Sprint 2, Sprint 3, validacion final y cierre.
- Los tres gates humanos iniciales quedan aceptados.
- `run_summary.json` marca `resultado_final = completo`.
- La validacion final se ejecuta completa: 16 checks planificados, 16 ejecutados, 0 no ejecutados.
- `ok_global = false`.
- Clasificacion final: `parcial_con_incidencias`.
- Factores bloqueantes: 0.

Resultado tecnico positivo:
- `03b_scaffold/scaffold_check.json` pasa con `ok=true`.
- `manage.py check` final pasa sin incidencias.
- Las migraciones propias existen para las apps con modelos (`accounts`, `catalog`, `reservations`).
- `manage.py migrate --noinput` final pasa.
- `runserver` arranca y permite ejecutar smoke tests HTTP.
- PayPal queda implementado como servicio local simulado, sin import externo `requests`, coherente con la decision metodologica de evaluar Sandbox como flujo simulado reproducible.
- `manifest.json`, `readme.md` y `lecciones_aprendidas.md` se generan correctamente en `99_cierre`.

Incidencias finales detectadas:
- `seed_data` falla con `Unknown command: 'seed_data'`, aunque existe `core/management/commands/seed_data.py`.
- Causa probable: la app `core` no esta incluida en `INSTALLED_APPS`, por lo que Django no descubre el comando de gestion.
- La ruta canonica `/cesta/` devuelve 404.
- Causa probable: `hundidos/urls.py` monta `reservations.urls` bajo `path('reserva/', include('reservations.urls'))`, y `reservations/urls.py` define `path('cesta/', ...)`; por tanto la cesta real queda en `/reserva/cesta/`, no en `/cesta/`.
- La validacion final falla en `reservations/checkout_step3.html` por `TemplateDoesNotExist`. El producto entrega y compila `templates/reservations/step3.html`; por tanto esta incidencia mezcla una decision discutible del validador con un posible problema de contrato de nombres.

Incidencias adicionales observadas en reviews incrementales:
- Desde Sprint 1 el review incremental ya detecta `seed_data` no ejecutable y `/cesta/` con 404.
- Sprint 1 y 2 tambien detectan `/admin-panel/` con 404; Sprint 3 lo corrige y final queda como redireccion controlada al login.
- El review incremental detecta templates con filtro inexistente `mul`: `tracking/detail.html` desde Sprint 1 y `admin_panel/reservation_detail.html` en Sprint 3. Estas templates no forman parte del check final minimo, pero son errores reales de producto si esas pantallas se usan.

Valoracion metodologica:
- Run 22 no debe descartarse como "fallo de arranque"; ya no lo es. Debe clasificarse como producto parcialmente funcional con incidencias concretas.
- Las incidencias de `seed_data` y `/cesta/` son fallos legitimos de contrato publico: el brief/protocolo exige datos seed y cesta accesible desde ruta canonica.
- La incidencia `checkout_step3.html` no deberia usarse sola como criterio duro de invalidez si la ruta canonica `/reserva/paso3/` existe y la template real `reservations/step3.html` compila. Mantener ese nombre historico como unica template critica es un acoplamiento del validador.
- Los errores por `mul` son fallos reales, pero no conviene responder con un parche de prompt del tipo "no uses mul". La regla general correcta es: no usar filtros/tags de template no estandar salvo que se entreguen y se carguen correctamente, o hacer los calculos en vistas/modelos/servicios antes de renderizar.

Hasta donde se puede modificar sin sobreingenieria:
- Aceptable: corregir reglas generales del instrumento para exigir comandos de gestion descubribles por Django cuando se entregue `core/management/commands/*`.
- Aceptable: mantener rutas canonicas como contrato publico minimo. Si el producto usa prefijos internos, debe exponer alias canonicos o montar la app de forma compatible.
- Aceptable: corregir el validador final para validar la template asociada a la ruta `/reserva/paso3/` o aceptar nombres equivalentes derivados de la arquitectura, no un unico nombre historico.
- Aceptable: mejorar la calidad del diagnostico del review para conservar la ultima linea de tracebacks, porque ahi aparece la causa real (`Invalid filter: 'mul'`, `TemplateDoesNotExist`, etc.).
- Riesgoso: anadir instrucciones hiperconcretas al prompt basadas en esta run, como "incluye core en INSTALLED_APPS", "no montes reservations bajo /reserva/" o "no uses mul". Esas instrucciones solo son defendibles si se reformulan como reglas generales de Django y contrato publico.
- Riesgoso: corregir manualmente el producto generado de Run 22 y presentarlo como salida del pipeline. Para la memoria, si se modifica producto generado, debe registrarse como intervencion posterior y no como run automatica valida.

Decision provisional:
Run 22 queda como run de maduracion pre-congelacion, no como run final medida. El siguiente trabajo debe centrarse en reglas generales y controles deterministas, no en parches a este producto concreto.


## 2026-05-14 - Cambios pre-run-candidata derivados de Run 22

Se aplican los cambios minimos metodologicamente defendibles para preparar la siguiente run candidata. No se modifica ningon producto generado dentro de runs/, no se cambia el brief, no se relajan criterios y no se anaden agentes nuevos.

Archivos modificados:

1. `src/pipeline/utils/django_runner.py`
   - `_resumir_salida`: ahora conserva tanto el inicio como el final del texto cuando supera `max_chars`. Antes truncaba solo por delante, perdiendo la ultima linea del traceback donde Django reporta la causa real (p.ej. `TemplateDoesNotExist`, `Invalid filter`). El cambio es general: mejora el diagnostico de cualquier error cuyo traceback supere 4000 chars.
   - Funciones nuevas compartidas: `_buscar_settings_py`, `_extraer_installed_apps_estatico`, `_detectar_commands_apps_no_instaladas`. Estas funciones hacen analisis estatico de archivos (sin ejecutar Django) y son usadas por `final_validator.py` y `review_builder.py`. `_detectar_commands_apps_no_instaladas` busca apps con `management/commands/*.py` cuya app no aparece en `INSTALLED_APPS` del settings.py detectado.
   - Cubre incidencias: `seed_data` no descubrible (Run 22), tracebacks truncados (Run 22).

2. `src/pipeline/utils/final_validator.py`
   - `TEMPLATES_CRITICAS` cambia de `["reservations/checkout_step3.html"]` a `["reservations/step3.html"]` (nombre canonico estandar).
   - Nueva funcion `_resolver_templates_criticas(codigo_dir)`: detecta dinamicamente que nombre de template del paso 3 entrego el producto (`step3.html` o `checkout_step3.html`) y valida el que existe. Si ninguno existe, reporta la ausencia sobre el nombre estandar. Elimina el acoplamiento del validador a un nombre historico que no pertenece al contrato tecnico aceptado.
   - Se integra `_detectar_commands_apps_no_instaladas(copia_dir)` como check adicional al finalizar `_construir_incidencias`. El check es estatico y se ejecuta independientemente del resultado de `manage.py check`.
   - Cubre incidencias: `checkout_step3.html` vs `step3.html` (Run 21, Run 22), `seed_data` no descubrible (Run 22).

3. `src/pipeline/utils/review_builder.py`
   - Se anade `_detectar_commands_apps_no_instaladas(codigo_dir)` al final de `_review_ejecutable_incremental`, junto a `_incidencias_navegacion_estatica`. Permite detectar la incidencia en el sprint que la introduce, no solo en la validacion final.
   - Cubre incidencias: `seed_data` no descubrible (Run 22), deteccion temprana de commands en apps no instaladas.

4. `src/pipeline/crews/desarrollo_crew/config/tasks.yaml`
   - Se anaden dos reglas generales de Django al bloque "CONTRATO DE PRODUCTO EJECUTABLE HUNDIDOS":
     a) Regla de management commands: si se entrega un comando en `management/commands/`, la app que lo contiene debe estar en `INSTALLED_APPS`. Es una regla general de Django, no un parche a `core` ni a `seed_data` concretamente.
     b) Regla de template tags: no usar filtros/tags no estandar sin definirlos como templatetags propios, cargados con `{% load %}`. Para calculos de negocio, realizarlos en vista/modelo/servicio. Esta regla cubre el problema del filtro `mul` sin mencionarlo.
   - La regla de rutas canonicas se amplia con la aclaracion de que usar `include()` bajo un prefijo no expone las sub-rutas en la raiz del proyecto; para respetar el contrato publico de rutas, deben montarse en la raiz o proveer alias. Esta es una regla general de Django URL routing, no un parche a `reservations.urls`.
   - Cubre incidencias: `seed_data` no descubrible (Run 22), `/cesta/` con 404 (Run 22), errores de template por filtros no estandar (Run 22).

Lo que NO se modifico deliberadamente:
- No se corrigio el producto de Run 22 (prohibido por protocolo).
- No se cambio el brief.
- No se modificaron los gates humanos.
- No se eliminaron `manage.py check`, `migrate --noinput`, `seed_data` ni `runserver` del pipeline.
- No se anado un agente nuevo ni un corrector LLM.
- No se convirtio ningun fallo concreto en instruccion hiperlocal (no aparece "core", "mul", "reserva/" en los prompts).
- No se modificaron prompts del Arquitecto ni del PM.
- No se modifico `pipeline_specs.md` ni `pipeline_config.yaml`.
- No se modifico `validators.py` (los checks de nivel 2 son independientes de estas incidencias).

Verificacion:
- Smoke tests de importacion y logica nuevas: 9/9 OK.
- Linter: sin errores en los 4 archivos modificados.
- Los checks planificados de la validacion final siguen siendo 16 (la lista de templates planificadas usa el nombre estandar `step3.html`; el check ejecutado refleja el nombre real del producto).

Estado del pipeline: listo para lanzar run candidata.

## 2026-05-14 - Incidencia Run 23 (`run_2026-05-14_19-50`) y control de rate limit

Se revisa el aborto temprano del Sprint 1 en `run_2026-05-14_19-50`. La causa documentada en `_attempts/fase04_regen0_intento1.txt`, `_attempts/fase04_regen0_intento2.txt` y `_attempts/fase04_regen0_intento3.txt` no es un fallo de Django ni una regresion de `manage.py check`: los tres intentos fallan antes de producir `entrega_sprint_1.json` por `RateLimitError 429` del proveedor LLM (`output tokens per minute`).

Diagnostico:
- El scaffold de Sprint 0 si se genera y `scaffold_check.json` queda con `ok=true`.
- Sprint 1 no llega a generar entrega; por tanto no existen `entrega_sprint_1.json`, `review_sprint_1.json` ni errores funcionales atribuibles al producto.
- La API informa limite de 10,000 output tokens/minute para el modelo usado. El pipeline consumia los tres reintentos automaticamente sin esperar una ventana de recuperacion, por lo que repetia la misma condicion de fallo.
- La incidencia se clasifica como fallo operativo de proveedor/configuracion temporal de ejecucion, no como evidencia de invalidez funcional del producto generado.

Cambio aplicado:
- `src/pipeline/main.py` incorpora deteccion general de errores 429/rate limit en llamadas LLM.
- Si el SDK expone `retry-after`, se respeta ese valor; si no, se espera una ventana conservadora de 90 segundos antes de consumir el siguiente reintento.
- El cambio se aplica a fase 01, fase 02, fase 03, scaffold y sprints de desarrollo.

Justificacion metodologica:
- No se relajan validadores.
- No se eliminan `manage.py check`, `migrate --noinput`, `seed_data` ni `runserver`.
- No se modifica el producto generado ni los artefactos dentro de `runs/`.
- No se cambia el contrato de rutas ni el brief.
- La correccion solo evita que un limite temporal del proveedor se confunda con tres fallos independientes del pipeline.

Verificacion:
- `src/pipeline/main.py` compila correctamente con el Python bundled de Codex.

Actualizacion tras revisar la consola de Anthropic:
- La consola muestra solicitudes recientes del perfil developer con 26k tokens de entrada y `32768` tokens de salida solicitados.
- Aunque el backoff evita reintentos inmediatos, mantener `developer.max_tokens=32768` no es operativo con el limite observado de 10,000 output tokens/minute.
- Se reduce `developer.max_tokens` y `generation.developer.max_tokens_documentados` de `32768` a `8192` en `src/pipeline/config/pipeline_config.yaml`.
- Esta reduccion no relaja criterios tecnicos; solo adapta el presupuesto maximo de salida a la cuota real disponible para poder ejecutar pruebas hoy.
- Riesgo conocido: si una entrega de sprint necesita mas de 8192 tokens de salida, puede aparecer salida truncada o schema invalido. En ese caso la solucion metodologicamente limpia no seria subir otra vez a 32768 bajo esta cuota, sino dividir la entrega de desarrollo en unidades menores o usar un perfil con mayor OTPM.

## 2026-05-15 - Actualizacion de cuota Anthropic a Nivel 2

Tras comprar credito adicional, la consola de Anthropic muestra la organizacion en Nivel 2. Para `Claude Haiku Active` los limites visibles pasan a:
- Solicitudes por minuto: 1K.
- Tokens de entrada por minuto: 450K.
- Tokens de salida por minuto: 90K.

Decision operativa:
- Se actualiza `developer.max_tokens` de `8192` a `24000` en `src/pipeline/config/pipeline_config.yaml`.
- Se actualiza tambien `generation.developer.max_tokens_documentados` a `24000` para mantener coherencia del manifiesto.

Justificacion:
- El Run 24 (run_2026-05-15_09-52) demostro que `8192` no basta para Sprint 1: las tres respuestas quedaron truncadas y Pydantic reporto `Invalid JSON: EOF while parsing a string`.
- No se vuelve directamente a `32768`, porque el objetivo es usar el nuevo margen de Nivel 2 de forma prudente y reducir la probabilidad de picos innecesarios.
- Con 90K tokens de salida/minuto, `24000` deja margen para una entrega de Sprint 1 grande y mantiene espacio operativo para reintentos si el proveedor aplica ventanas estrictas.

Nota metodologica:
- La division de Sprint 1 en subentregas sigue siendo la solucion estructural mas robusta si el contrato monolitico de `EntregaSprint` vuelve a fallar. No se aplica ahora para no introducir un cambio mayor de protocolo justo antes de cerrar pruebas, salvo que el siguiente run confirme que el limite sigue siendo el cuello de botella.

## 2026-05-15 - Run 25 de confirmacion y congelacion del pipeline (run_2026-05-15_11-00)

Se ejecuta `run_2026-05-15_11-00` tras actualizar la cuota de Anthropic a Nivel 2 y configurar `developer.max_tokens=24000`. La ejecucion completa el flujo end-to-end sin reintentos automaticos ni regeneraciones humanas.

Resultado operativo:
- `resultado_final = completo`.
- Fases 01, 02 y 03 aceptadas por gate humano.
- Scaffold ejecutado correctamente.
- Sprint 1, Sprint 2 y Sprint 3 completados.
- Cierre ejecutado y manifiesto generado.
- `validacion_final.ejecutada = true`.
- `ok_global = true`.
- Clasificacion final: `apto_para_revision_funcional`.
- Checks planificados: 16.
- Checks ejecutados: 16.
- Checks no ejecutados: 0.
- Incidencias finales: 0.
- Factores bloqueantes: 0.

Checks deterministas superados:
- `manage.py check` correcto (`returncode=0`).
- Migraciones propias correctas para apps con modelos.
- `manage.py migrate --noinput` correcto.
- `manage.py seed_data` correcto.
- `runserver` arranca correctamente.
- Rutas minimas inspeccionables sin 404 ni 500: `/`, `/barcos/`, `/cesta/`, `/accounts/registro/`, `/accounts/login/`, `/reserva/paso1/`, `/reserva/paso2/`, `/reserva/paso3/`, `/admin/`, `/admin-panel/`.
- Template critica `reservations/step3.html` compila correctamente.

Observacion sobre gates:
- Los gates humanos de esta ejecucion se usaron como control de avance del flujo y fueron aceptados, pero no deben presentarse como una revision funcional profunda del producto.
- La evaluacion fuerte para considerar el Run 25 apto es la validacion final determinista y trazable.
- En la memoria se debe explicar que el gate humano valida continuidad y aceptacion de artefactos intermedios, mientras que la aptitud tecnica final se apoya en los checks reproducibles del cierre.

Decision de congelacion:
- El Run 25 se toma como run de confirmacion de que el pipeline esta terminado y operativo.
- A partir de este punto el pipeline queda congelado para las pruebas de memoria.
- No se haran nuevas correcciones del pipeline para acomodar resultados de las pruebas, salvo errores materiales de ejecucion del entorno que impidan lanzar el instrumento.
- Si las siguientes ejecuciones producen incidencias, estas se reportaran como resultados experimentales, no como motivos para seguir ajustando prompts, validadores o contratos.

Paso siguiente:
- La bitacora de maduracion del pipeline queda cerrada en este punto.
- Las ejecuciones de prueba para la memoria deben documentarse en un artefacto separado de resultados experimentales, referenciando sus carpetas `runs/`, manifiestos, validaciones finales y metricas.
- `run_2026-05-15_11-00` puede utilizarse en la memoria como evidencia de confirmacion/cierre del instrumento y como punto de congelacion del protocolo.

## 2026-05-17 - Preflight de entorno de validacion tras congelacion y Ajuste pre-oficial del prompt de planificacion

Durante la preparacion de la primera ejecucion oficial para documentacion se lanzo `run_2026-05-17_18-49`. La ejecucion completo el flujo, pero la validacion final quedo bloqueada por un problema del entorno de validacion, no por una ausencia de artefactos del producto:
- `validacion_final.ok_global = false`.
- Clasificacion: `bloqueado_arranque`.
- Causa inmediata: `ModuleNotFoundError: No module named 'requests'` al importar `reservations/services/paypal.py`.
- La entrega generada si declaraba `requests==2.31.0` en `requirements.txt`.

Tambien se observo un intento fallido de Sprint 1 con salida JSON incompleta del LLM (`Invalid JSON: EOF while parsing a string` para `EntregaSprint`). Ese fallo fue gestionado por el mecanismo de reintento automatico y no fue el bloqueo final del run.

Decision metodologica:
- `run_2026-05-17_18-49` se conserva como evidencia de preflight/incidencia de preparacion, pero no se considera primera run oficial de resultados.
- No se modifican `runs/`, el brief, los validadores ni el producto generado.
- Se reconstruye `.venv_Test` porque el entorno fijo de validacion habia quedado desalineado tras movimientos y pruebas locales.
- Se instala el conjunto fijo de dependencias necesarias para validar los productos Django generados: `Django==3.2`, `Pillow==9.5.0`, `django-filter==23.1` y `requests==2.31.0`.

Preflight verificado:
- Interprete: `D:\University\TFG\PRUEBAS\multiagentes\pipeline\.venv_Test\Scripts\python.exe`.
- `django 3.2`.
- `PIL 9.5.0`.
- `django-filter 23.1`.
- `requests 2.31.0`.
- Resultado: `PREFLIGHT_OK`.

Se revisa el valor metodologico del artefacto `plan_sprints`. La version previa
repartia correctamente el backlog en tres sprints, pero aportaba poca
informacion adicional para justificar la secuencia, evaluar dependencias o
comparar runs. Se decide enriquecer el prompt de planificacion sin cambiar el
esquema Pydantic ni la logica del pipeline.

Cambio aplicado:
- `src/pipeline/crews/planificacion_crew/config/tasks.yaml`
  - En la tarea `planificar_sprints`, el campo `objetivo` debe incluir ahora
    justificacion de secuencia: por que esas historias van juntas y que
    dependencias preparan para los sprints posteriores.
  - El campo `entregable_verificable` debe incluir funcionalidad operativa al
    cierre, dependencias desbloqueadas, checks minimos observables y riesgo
    principal del sprint.
  - Para mejorar la legibilidad sin cambiar el contrato JSON, el campo
    `entregable_verificable` debe usar etiquetas Markdown internas dentro de un
    unico string: `**Funcionalidad operativa:**`,
    `**Dependencias desbloqueadas:**`, `**Checks minimos:**` y
    `**Riesgo principal:**`.
  - Se mantiene la restriccion de no anadir campos nuevos al JSON. La
    informacion se integra dentro de los campos existentes.
- `src/pipeline/crews/planificacion_crew/config/tasks.yaml`
  - En la tarea `analizar_riesgos`, cada riesgo debe ubicarse con un marcador
    inicial: `[Sprint 1]`, `[Sprint 2]`, `[Sprint 3]` o `[Proyecto]`.
  - Los riesgos de sprint deben conectarse con dependencias entre historias,
    criterios de salida o checks minimos del sprint.
  - Los riesgos transversales o no asociados a un sprint concreto se marcan
    como `[Proyecto]`.
- `src/pipeline/crews/planificacion_crew/config/agents.yaml`
  - Se refuerza el backstory del PM para que el plan no sea una particion
    mecanica del backlog, sino un artefacto con criterio de direccion del
    proyecto.
  - Se anade la misma regla de ubicacion de riesgos por sprint o proyecto.
  - Se anade la regla de etiquetas Markdown internas para
    `entregable_verificable`.

Justificacion:
- El cambio mejora la utilidad documental del plan de sprints para la memoria:
  permite explicar por que se desarrolla en ese orden, que dependencias se
  desbloquean y que checks minimos se esperan por incremento.
- Tambien mejora la trazabilidad de riesgos, separando riesgos de sprint de
  riesgos globales del proyecto.
- No se modifica el brief.
- No se modifica ningun producto generado dentro de `runs/`.
- No se modifican schemas, renderers, validators ni el Flow.
- No se anaden campos nuevos al contrato JSON, por lo que el cambio se limita a
  contenido generado dentro de campos ya existentes.

Implicacion metodologica:
- Las pruebas oficiales de memoria deben lanzarse despues de este ajuste, o bien documentar explicitamente que la run previa pertenece a una version anterior del prompt de planificacion.
- Antes de lanzar las tres runs oficiales, este ajuste debe considerarse parte de la nueva congelacion oficial del instrumento.
- La siguiente ejecucion, lanzada con `.venv_Test` verificado inmediatamente antes y los ajustes agregados, sera la candidata a primera run oficial de resultados.
