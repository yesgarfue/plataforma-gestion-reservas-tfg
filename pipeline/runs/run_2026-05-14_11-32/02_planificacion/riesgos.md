---
run_id: run_2026-05-14_11-32
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T11:41:59+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-14_11-32`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | El servidor SMTP para envío de correos puede no estar configurado o disponible en el entorno de desarrollo, impidiendo la validación de confirmaciones y recordatorios de reserva. | media | medio | Configurar un servidor SMTP de prueba (p.ej. MailHog o similar) en el Dockerfile y documentar en README cómo cambiar las credenciales para producción. Implementar logs de correos fallidos en la aplicación. |
| R-03 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Crear un test unitario explícito que valide el cálculo de tasa para barcos de categoría 'velero' y otro para categorías no velero antes de cerrar la historia HU-10. Incluir este test en la suite de CI/CD. |
| R-04 | SQLite tiene concurrencia limitada y puede generar bloqueos si múltiples clientes intentan reservar simultáneamente, causando errores de transacción. | media | alto | Implementar reintentos automáticos con backoff exponencial en las operaciones de reserva. Documentar en README que SQLite es solo para desarrollo y que producción requiere PostgreSQL. Realizar pruebas de carga con al menos 10 reservas simultáneas en Sprint 2. |
| R-05 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden fallar si hay conflictos de claves primarias o cambios en el esquema. | media | medio | Crear un script de inicialización idempotente que verifique si los datos ya existen antes de insertarlos. Usar manage.py loaddata con fixtures en lugar de scripts SQL directos. Documentar el proceso en README. |
| R-06 | El proceso de reserva en 3 pasos sin registro previo tiene casos borde complejos: cliente inicia sesión durante el flujo, recupera cesta, pero datos de pago pueden no sincronizarse correctamente. | alta | medio | Crear casos de prueba explícitos en Sprint 2 que cubran: (1) cliente anónimo inicia reserva, (2) inicia sesión a mitad del flujo, (3) vuelve de login y verifica que la cesta se recupera. Bloquear merge de HU-07 si estos casos no pasan. |
| R-07 | Los filtros combinables (puertos, fabricantes, precio, categoría, capacidad, fechas) son más complejos de lo que aparentan y pueden generar queries SQL ineficientes o resultados incorrectos con combinaciones específicas. | media | medio | Implementar tests de integración en Sprint 1 que validen todas las combinaciones críticas de filtros (p.ej. filtro de fechas + precio + puerto). Usar Django Debug Toolbar para monitorear queries. Documentar la lógica de filtros en docstrings. |
| R-08 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024) y puede tener vulnerabilidades de seguridad no parcheadas. | baja | alto | Ejecutar manage.py check --deploy antes de cada release. Usar herramientas como safety o pip-audit para detectar dependencias vulnerables. Documentar en README que la aplicación es de demostración y requiere actualización a Django LTS más reciente para producción. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas que pueden no estar disponibles o cambiar de forma incompatible. | baja | medio | Fijar versiones específicas de imágenes base en el Dockerfile (p.ej. python:3.9-slim-bullseye en lugar de python:3.9-slim). Usar un registro privado o caché local si es posible. Documentar las versiones esperadas en README. |
| R-10 | Tres sprints son ajustados para el alcance comprometido; el Sprint 2 depende del modelo de reserva del Sprint 1, y el Sprint 3 depende de ambos, creando riesgo de bloqueos en cascada. | alta | alto | Establecer una reunión de sincronización diaria entre sprints. Crear un contrato de interfaz claro para el modelo de Reserva al final del Sprint 1 (estados, campos, métodos). Implementar mocks del modelo en Sprint 2 si es necesario para no bloquear desarrollo de pago. |
