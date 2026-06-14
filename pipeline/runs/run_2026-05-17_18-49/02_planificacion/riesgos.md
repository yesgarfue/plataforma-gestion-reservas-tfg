---
run_id: run_2026-05-17_18-49
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-17T19:09:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-17_18-49`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 euros en lugar de 50 euros/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar la historia HU-12, y añadir un comentario en el código indicando la excepción. |
| R-03 | SQLite tiene concurrencia limitada para múltiples reservas simultáneas, lo que puede causar bloqueos o errores si varios clientes intentan reservar al mismo tiempo. | media | alto | Implementar un mecanismo de transacciones explícitas con aislamiento SERIALIZABLE en el modelo de reserva, y ejecutar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el sprint 2. |
| R-04 | El proceso de reserva en tres pasos sin registro previo tiene múltiples casos borde: cliente inicia sesión durante el proceso, cesta se modifica entre pasos, datos heredados incompletos. | alta | medio | Documentar explícitamente todos los casos borde en la historia HU-09, crear un test de integración para cada caso (login durante reserva, modificación de cesta, herencia de datos), y ejecutarlos antes de cerrar el sprint 2. |
| R-05 | Los filtros combinables de catálogo (puerto, fabricante, precio, categoría, capacidad, fechas) son complejos de implementar correctamente y pueden tener intersecciones vacías o comportamientos inesperados. | media | medio | Crear una matriz de pruebas con al menos 15 combinaciones de filtros (incluyendo casos límite como rango de precio vacío, fechas sin disponibilidad) y ejecutarlas antes de cerrar la historia HU-06 en el sprint 1. |
| R-06 | El envío de correos de confirmación y recordatorio depende de un servidor SMTP configurado correctamente, que puede no estar disponible en el entorno de desarrollo o demo. | media | medio | Configurar un backend de correo en memoria (console backend) para desarrollo y pruebas, y crear un script de validación que verifique la configuración SMTP antes de cada despliegue en producción. |
| R-07 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden fallar si hay conflictos de claves primarias o cambios en el esquema. | media | medio | Implementar un comando de management personalizado que verifique la integridad de los datos seed, elimine datos duplicados y reinserte si es necesario, ejecutándolo en el entrypoint del Dockerfile. |
| R-08 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas o incompatibilidades con dependencias. | baja | alto | Ejecutar 'pip check' y 'safety check' antes de cada commit para detectar vulnerabilidades conocidas, y documentar en el README las versiones mínimas de dependencias compatibles. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, etc.) que pueden no estar disponibles o tener cambios incompatibles. | baja | medio | Especificar versiones exactas de imágenes base en el Dockerfile (p.ej. python:3.9.18-slim), y crear un script de validación que intente construir la imagen antes de cada release. |
| R-10 | El reparto de funcionalidades entre tres sprints puede dejar dependencias cruzadas: el sprint 2 necesita el modelo de reserva del sprint 1, y el sprint 3 necesita la lógica de pago del sprint 2. | alta | medio | Establecer un orden de desarrollo estricto: sprint 1 cierra con modelo de reserva básico, sprint 2 cierra con lógica de pago funcional, sprint 3 solo añade gestión administrativa. Ejecutar pruebas de integración entre sprints antes de cerrar cada uno. |
