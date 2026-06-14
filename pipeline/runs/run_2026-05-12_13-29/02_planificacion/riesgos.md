---
run_id: run_2026-05-12_13-29
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T13:52:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-12_13-29`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total de la reserva. | alta | medio | Crear un test unitario explícito que valide el cálculo de tasa de combustible para barcos de categoría 'velero' antes de cerrar la historia HU-11, y ejecutarlo en cada commit. |
| R-03 | SQLite tiene limitaciones de concurrencia para múltiples reservas simultáneas, lo que puede causar bloqueos o pérdida de datos si varios clientes reservan al mismo tiempo. | media | alto | Implementar transacciones explícitas con nivel de aislamiento SERIALIZABLE en el modelo de reserva, y ejecutar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el sprint 2. |
| R-04 | El servidor SMTP para envío de correos puede no estar configurado en el entorno de desarrollo o pruebas, impidiendo que los clientes reciban confirmaciones y códigos de seguimiento. | alta | medio | Configurar un backend de correo en memoria (console backend) para desarrollo y un servicio SMTP mock (como MailHog) para pruebas, con instrucciones en el README. Implementar logs de correos enviados para verificar contenido sin depender de SMTP real. |
| R-05 | Los filtros combinables (puerto, fabricante, categoría, capacidad, precio, fechas) pueden generar queries SQL complejas que degraden el rendimiento con muchos barcos en el catálogo. | media | medio | Implementar índices en las columnas de filtrado (puerto, fabricante, categoría) en la base de datos, y ejecutar pruebas de rendimiento con 100+ barcos antes de cerrar la historia HU-05. Documentar el plan de optimización en caso de necesidad futura. |
| R-06 | El proceso de reserva en tres pasos sin registro previo tiene casos borde complejos: mantener la cesta entre pasos, validar datos incompletos, manejar timeouts de sesión sin perder datos. | alta | medio | Crear un conjunto de tests de integración que cubra los tres pasos completos, incluyendo casos de error (datos inválidos, sesión expirada, volver atrás). Ejecutar estos tests antes de cerrar la historia HU-09. |
| R-07 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024), lo que puede dejar la aplicación vulnerable a problemas de seguridad no parcheados. | baja | alto | Documentar explícitamente en el README que Django 3.2 es la versión requerida por el proyecto. Ejecutar manage.py check antes de cada commit y bloquear merge si hay advertencias de seguridad. Planificar una migración a versión LTS más reciente como tarea post-proyecto. |
| R-08 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden fallar si hay conflictos de claves primarias o cambios en el esquema. | media | medio | Crear un script de seed idempotente que verifique si los datos ya existen antes de insertarlos. Ejecutar migrations y seed en el entrypoint del Dockerfile, con logs detallados. Incluir instrucciones en el README para resetear la base de datos si es necesario. |
| R-09 | La construcción del contenedor Docker depende de descargar imágenes base externas (python:3.x) que pueden no estar disponibles o cambiar de forma incompatible. | baja | medio | Especificar una versión exacta de la imagen base en el Dockerfile (p.ej. python:3.9-slim-bullseye en lugar de python:3.9). Documentar las versiones de dependencias en requirements.txt con pins exactos. Probar la construcción del contenedor en un entorno limpio antes de cada release. |
| R-10 | El reparto de funcionalidades entre tres sprints es ajustado: el sprint 2 depende del modelo de reserva del sprint 1, y el sprint 3 depende de la lógica de pago del sprint 2, creando riesgo de bloqueos en cascada. | media | alto | Establecer un modelo de reserva básico (sin cálculo de tasa) al final del sprint 1 para que el sprint 2 pueda comenzar en paralelo. Usar feature flags para activar/desactivar funcionalidades incompletas. Realizar una reunión de sincronización entre sprints para identificar dependencias cruzadas. |
