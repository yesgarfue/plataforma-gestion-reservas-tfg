# Informe de Auditoría Técnica — Proyecto "Hundidos"

> Auditoría generada el 2026-04-20

---

## Resumen ejecutivo

**Hundidos** es una aplicación web de alquiler de barcos desarrollada como Trabajo de Fin de Grado (TFG). Partió de una plantilla de e-commerce genérica en Django y fue adaptada al dominio de reservas náuticas. El sistema permite a los usuarios buscar barcos por categoría, puerto, fabricante, capacidad y fechas de disponibilidad; añadirlos a un carrito con fechas de inicio/fin; completar el pago vía PayPal o contra-reembolso; y recibir un email de confirmación con código de seguimiento. Incluye un panel de administración propio (independiente del admin de Django) para gestionar barcos, usuarios y reservas.

### Estado general del proyecto

El proyecto **funciona para su propósito demo/académico** pero presenta deuda técnica significativa heredada de la plantilla original y varios problemas de seguridad que lo hacen **no apto para producción real** en su estado actual.

### Valoración de la calidad del código

| Dimensión | Valoración | Observación principal |
|---|---|---|
| Funcionalidad core | ⭐⭐⭐⭐ (4/5) | El flujo de reserva funciona; hay bugs puntuales |
| Seguridad | ⭐ (1/5) | 3 vulnerabilidades críticas; secretos hardcodeados |
| Calidad del código | ⭐⭐ (2/5) | Duplicados, imports muertos, código comentado |
| Arquitectura | ⭐⭐⭐ (3/5) | Estructura Django correcta pero sin limpieza post-adaptación |
| Testing | ⭐ (1/5) | Cero tests implementados |
| Preparación para producción | ⭐ (1/5) | DEBUG=True, SQLite, sin gestión de secretos |

### Los 5 problemas más urgentes

1. **`SECRET_KEY = 1234`** — La clave criptográfica de Django es un entero hardcodeado. Todo el sistema de firmas (sesiones, CSRF, tokens) está comprometido.
2. **`delete_user` sin autenticación** — Cualquier visitante anónimo puede eliminar cualquier usuario enviando una petición GET a `/accounts/delete_user/<id>/`.
3. **Contraseña Gmail real hardcodeada** — La credencial original fue retirada del repositorio y debe rotarse.
4. **`DEBUG=True` en producción** — El sitio está desplegado en Render con debug activo; los errores exponen trazas completas.
5. **`order_list` crashea** — La vista de administración de reservas lanza `TypeError` en tiempo de ejecución por un bug en la línea 309 de `orders/views.py`.

---

## Índice de archivos

| Archivo | Contenido |
|---|---|
| [01_STACK_TECNOLOGICO.md](01_STACK_TECNOLOGICO.md) | Versiones de Python/Django, librerías, frontend (Bootstrap, jQuery, FullCalendar, PayPal), Docker, Render |
| [02_ARQUITECTURA.md](02_ARQUITECTURA.md) | Árbol de carpetas comentado, las 5 apps Django y sus responsabilidades, diagrama de dependencias |
| [03_MODELO_DE_DATOS.md](03_MODELO_DE_DATOS.md) | Todos los modelos con campos, tipos, relaciones y métodos; marcados residuos de e-commerce |
| [04_AUTENTICACION.md](04_AUTENTICACION.md) | Modelo `Account`, flujos de registro/login/recuperación, validador de contraseña, roles, SMTP |
| [05_URLS_Y_VISTAS.md](05_URLS_Y_VISTAS.md) | Tabla completa de URLs por app con vista, protección de login y descripción; bugs funcionales |
| [06_TEMPLATES_Y_ESTATICOS.md](06_TEMPLATES_Y_ESTATICOS.md) | Jerarquía de templates, bloques de `base.html`, formularios, estáticos y archivos de media |
| [07_CONFIGURACION.md](07_CONFIGURACION.md) | DEBUG, ALLOWED_HOSTS, INSTALLED_APPS, MIDDLEWARE, email, cookies — y todos los secretos hardcodeados |
| [08_BASE_DE_DATOS.md](08_BASE_DE_DATOS.md) | SQLite, ubicación, número de migraciones por app, tablas generadas, recomendaciones de producción |
| [09_DEUDA_TECNICA.md](09_DEUDA_TECNICA.md) | Imports muertos, duplicados, dependencias sin uso, residuos de plantilla, bugs funcionales identificados |
| [10_SEGURIDAD.md](10_SEGURIDAD.md) | 17 hallazgos priorizados (3 críticos, 4 altos, 5 medios, 5 bajos) con ubicación exacta y corrección sugerida |
| [11_ARRANQUE_Y_CREDENCIALES.md](11_ARRANQUE_Y_CREDENCIALES.md) | Pasos reproducibles para levantar el proyecto, credenciales encontradas, cómo crear superusuario |

---

## Mapa de archivos de código fuente clave

```
ecommerce/settings.py     ← Configuración global (secretos hardcodeados aquí)
ecommerce/urls.py         ← Enrutador raíz
accounts/models.py        ← Modelo de usuario Account + UserProfile
accounts/views.py         ← Registro, login, gestión de usuarios
store/models.py           ← Product, Puerto, Fabricante, Variation, ReviewRating
store/views.py            ← Catálogo, búsqueda, CRUD admin barcos
carts/views.py            ← Lógica de carrito, disponibilidad
orders/views.py           ← Checkout, pagos PayPal, contra-reembolso
orders/models.py          ← Order, OrderProduct, Payment
templates/base.html       ← Plantilla base (PayPal client-id expuesto aquí)
requirements.txt          ← Dependencias (algunas sin uso)
```

---

*Informe generado mediante auditoría estática del código fuente del repositorio.*
