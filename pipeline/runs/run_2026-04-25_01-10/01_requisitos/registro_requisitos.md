---
run_id: run_2026-04-25_01-10
fase: 01_requisitos
agente: Analista
modelo: ollama/qwen2.5-coder:7b
timestamp: 2026-04-25T01:14:21+02:00
hash_brief: sha256:e62bcd5b2a4f5684...
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-04-25_01-10`

## Requisitos funcionales

Total: **15**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El cliente puede navegar por el catálogo de barcos organizado por categorías. | Alta |
| RF-05 | El cliente puede buscar barcos por nombre o título del barco. | Alta |
| RF-06 | El cliente puede aplicar filtros combinables (puertos, fabricantes, precio, categoría, capacidad, rango de fechas) durante la búsqueda. | Alta |
| RF-07 | El cliente puede agregar un barco a la cesta desde la ficha del barco. | Alta |
| RF-08 | El cliente puede ampliar o reducir la cantidad de unidades de cada barco en la cesta. | Alta |
| RF-09 | El cliente puede revisar el estado de su cesta desde el catálogo. | Alta |
| RF-10 | El cliente puede finalizar la compra (proceso de reserva) desde la cesta. | Alta |
| RF-11 | El sistema aplica una tasa de combustible de 50 € por día, salvo que el barco sea de categoría 'velero', en cuyo caso la tasa es 0 €. | Alta |
| RF-12 | El sistema envía un correo electrónico al cliente con los datos del barco reservado, el rango de fechas, el importe total y un código de seguimiento del alquiler. | Alta |
| RF-13 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email, incluso si no está registrado. | Alta |
| RF-14 | El administrador puede gestionar barcos (alta, edición, baja) desde su panel de administración. | Alta |
| RF-15 | El administrador puede gestionar clientes (consulta, eliminación) desde su panel de administración. | Alta |

## Requisitos no funcionales

Total: **3**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Idioma | La interfaz de usuario está íntegramente en español. | Alta |
| RNF-02 | Seguridad | Contraseñas no almacenadas en texto plano (se usa el mecanismo estándar de Django); CSRF activo; validación de formularios. | Alta |
| RNF-03 | Restricciones técnicas | El lenguaje es Python. | Alta |
