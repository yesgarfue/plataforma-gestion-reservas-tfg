---
run_id: run_2026-05-10_10-50
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-10T10:59:24+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-10_10-50`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Crear un test unitario explícito que valide el cálculo de tasa de combustible para barcos de categoría 'velero' antes de cerrar la historia HU-13, y ejecutarlo en cada commit. |
| R-03 | SQLite tiene limitaciones de concurrencia para múltiples reservas simultáneas, lo que puede causar bloqueos o errores si varios clientes reservan al mismo tiempo. | media | alto | Implementar un mecanismo de transacciones explícitas con aislamiento SERIALIZABLE en el modelo de reserva, y realizar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el Sprint 2. |
| R-04 | El envío de correos de confirmación con código de seguimiento depende de un servidor SMTP configurado, que puede no estar disponible en el entorno de desarrollo o demo. | media | medio | Configurar un backend de correo en memoria (console backend) para desarrollo y un servicio SMTP mock (como MailHog) en Docker, permitiendo verificar el contenido del correo sin dependencia externa. |
| R-05 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker sin crear duplicados, lo que puede fallar si la lógica de carga no es idempotente. | alta | medio | Implementar un comando manage.py personalizado que verifique la existencia de datos seed antes de insertarlos, usando get_or_create en lugar de create, y ejecutarlo en el punto de entrada del Dockerfile. |
| R-06 | Los filtros combinables (puerto, fabricante, precio, categoría, capacidad) son más complejos de lo que aparentan, con casos borde como rangos de precio vacíos o combinaciones sin resultados. | alta | medio | Crear tests de integración para cada combinación de filtros (al menos 8 escenarios) incluyendo casos sin resultados, y documentar el comportamiento esperado en la historia HU-06 antes de implementar. |
| R-07 | El proceso de reserva en tres pasos sin registro previo tiene casos borde como pérdida de sesión entre pasos, cambios de cesta durante el proceso, o recuperación de cesta al iniciar sesión durante la reserva. | media | alto | Implementar tests de flujo end-to-end que cubran: abandono y retorno al carrito, inicio de sesión en paso 2, recuperación de cesta anterior, y cambios de cantidad durante el proceso, antes de cerrar el Sprint 2. |
| R-08 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024), lo que puede dificultar la obtención de parches de seguridad o compatibilidad con dependencias nuevas. | baja | medio | Documentar explícitamente la versión de Django 3.2 en el Dockerfile y requirements.txt, y realizar un análisis de vulnerabilidades conocidas antes del despliegue usando safety check. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, etc.) que pueden no estar disponibles o cambiar de forma inesperada. | baja | medio | Especificar versiones exactas de imágenes base en el Dockerfile (p.ej. python:3.9-slim-bullseye) y usar un registro privado o caché local si es posible, para garantizar reproducibilidad. |
| R-10 | Tres sprints son ajustados para el alcance comprometido (26 historias), y el reparto entre sprints puede dejar dependencias cruzadas que bloqueen el desarrollo (p.ej. Sprint 2 necesita el modelo de reserva de Sprint 1). | media | alto | Ejecutar una reunión de refinamiento al cierre de Sprint 1 para validar que el modelo de reserva está completamente funcional antes de que Sprint 2 comience, y mantener un backlog de bloqueos visible en el tablero. |
