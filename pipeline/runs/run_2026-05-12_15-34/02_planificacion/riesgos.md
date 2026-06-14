---
run_id: run_2026-05-12_15-34
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T15:55:36+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-12_15-34`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Crear un test unitario explícito que valide el cálculo de tasa de combustible para barcos de categoría 'velero' antes de cerrar la historia HU-13, y ejecutar este test en cada commit. |
| R-03 | Los filtros combinables del catálogo (puertos, fabricantes, precio, cantidad) son más complejos de lo que aparentan, con múltiples combinaciones posibles que pueden generar casos borde no previstos. | alta | medio | Crear una matriz de pruebas exhaustiva en la historia HU-06 que cubra todas las combinaciones de filtros (al menos 16 casos: cada filtro solo, pares de filtros, tríos y todos juntos) antes de marcar la historia como completada. |
| R-04 | SQLite tiene concurrencia limitada para reservas simultáneas, lo que puede causar bloqueos o pérdida de datos si múltiples clientes intentan reservar el mismo barco al mismo tiempo. | media | alto | Implementar transacciones explícitas con nivel de aislamiento SERIALIZABLE en el modelo de Reserva, y ejecutar pruebas de carga con al menos 10 reservas simultáneas del mismo barco antes de cerrar el sprint 2. |
| R-05 | El envío de correos de confirmación y recordatorios depende de un servidor SMTP configurado correctamente, que puede no estar disponible en el entorno de desarrollo o demo. | media | medio | Configurar un backend de email en memoria (console backend) para desarrollo y testing, y documentar en el README las variables de entorno necesarias para SMTP en producción. Crear un test que verifique que el correo se genera correctamente aunque no se envíe. |
| R-06 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden fallar si las migraciones no se ejecutan correctamente o si hay conflictos de integridad referencial. | media | alto | Crear un script de inicialización (manage.py seed) que ejecute las migraciones, cargue los datos seed y valide que los 5 barcos, 2 puertos, 2 fabricantes y 2 categorías existan. Incluir este script en el Dockerfile como parte del CMD de arranque. |
| R-07 | El proceso de reserva en tres pasos sin registro previo tiene casos borde complejos, como la recuperación de cesta al iniciar sesión durante el proceso, que pueden causar inconsistencias en los datos. | alta | medio | Crear un flujo de pruebas manual documentado en la historia HU-10 que cubra al menos 5 escenarios: reserva sin sesión, reserva con sesión, inicio de sesión durante reserva, cambio de cantidad en cesta durante reserva, y cancelación en cada paso. |
| R-08 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril de 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas y incompatibilidades con dependencias nuevas. | baja | alto | Documentar explícitamente en el README que Django 3.2 es la versión requerida y que no se deben actualizar dependencias sin validar compatibilidad. Ejecutar manage.py check antes de cada commit y bloquear merge si hay advertencias de seguridad. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas que pueden no estar disponibles o cambiar de forma incompatible durante el desarrollo. | baja | medio | Especificar versiones exactas de las imágenes base en el Dockerfile (p.ej. python:3.9-slim-bullseye en lugar de python:3.9-slim) y documentar las versiones probadas en el README. |
| R-10 | El reparto de funcionalidades entre tres sprints puede dejar dependencias cruzadas críticas, como que el sprint 2 (pago) depende del modelo de Reserva del sprint 1, causando bloqueos si el sprint 1 se retrasa. | media | alto | Implementar el modelo de Reserva completo (con estados PENDIENTE DE PAGO, CONFIRMADA, CANCELADA) en el sprint 1, aunque no se use hasta el sprint 2. Crear un test de integración que valide que el modelo de Reserva funciona correctamente antes de cerrar el sprint 1. |
