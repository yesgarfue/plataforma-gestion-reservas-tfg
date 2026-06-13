# 08 — Base de Datos

[← Volver al índice](00_INDICE.md)

---

## Motor y ubicación

| Parámetro | Valor |
|---|---|
| Motor | SQLite3 |
| Archivo | `BASE_DIR/db.sqlite3` → `/hundidos/db.sqlite3` |
| Configuración | `ecommerce/settings.py:102-107` |

El archivo `db.sqlite3` **está incluido en el repositorio**. Esto implica que los datos de prueba (usuarios, barcos, reservas) son accesibles directamente desde el repositorio. Para producción esto supone un riesgo de privacidad y de sincronización de estado.

---

## Herramienta recomendada para inspeccionar la BD

**DB Browser for SQLite** — https://sqlitebrowser.org/

Pasos:
1. Descargar e instalar DB Browser for SQLite.
2. `File → Open Database` → seleccionar `hundidos/db.sqlite3`.
3. Pestaña `Browse Data` → seleccionar tabla.

---

## Número de migraciones por app

| App | Migraciones |
|---|---|
| `accounts` | 6 |
| `store` | 5 |
| `carts` | 6 |
| `orders` | 10 |
| `category` | 3 |
| **Total proyecto** | **30** |

Las migraciones de Django built-in (`auth`, `contenttypes`, `sessions`, `admin`, etc.) añaden ~20 migraciones adicionales del framework.

---

## Tablas generadas por el proyecto

| Tabla | App / módulo | Descripción |
|---|---|---|
| `category_category` | category | Categorías de barcos |
| `accounts_account` | accounts | Usuarios personalizados |
| `accounts_userprofile` | accounts | Perfil extendido del usuario |
| `store_puerto` | store | Puertos de origen de los barcos |
| `store_fabricante` | store | Fabricantes de barcos |
| `store_product` | store | Catálogo de barcos |
| `store_variation` | store | Variaciones de producto (residuo: color/talla) |
| `store_reviewrating` | store | Reseñas y valoraciones |
| `carts_cart` | carts | Sesión de carrito anónimo |
| `carts_cartitem` | carts | Ítems del carrito con fechas de reserva |
| `carts_cartitem_variation` | carts (auto M2M) | Relación carrito-variación |
| `orders_payment` | orders | Registros de pago |
| `orders_order` | orders | Reservas/pedidos |
| `orders_orderproduct` | orders | Líneas de reserva con fechas |
| `orders_orderproduct_variation` | orders (auto M2M) | Relación pedido-variación |

### Tablas Django built-in presentes

| Tabla | Módulo |
|---|---|
| `django_admin_log` | django.contrib.admin |
| `auth_permission` | django.contrib.auth |
| `auth_group` | django.contrib.auth |
| `auth_group_permissions` | django.contrib.auth |
| `auth_user_groups` | django.contrib.auth |
| `django_content_type` | django.contrib.contenttypes |
| `django_session` | django.contrib.sessions |
| `django_migrations` | django (tracking) |

---

## Consideraciones de producción

- **SQLite no es apto para producción** con múltiples usuarios concurrentes. Django tiene soporte nativo para PostgreSQL, MySQL y MariaDB; para Render, PostgreSQL es la opción recomendada.
- El archivo `db.sqlite3` en el repositorio mezcla estado de datos con código. Debería añadirse a `.gitignore`.
- No hay fixtures de datos iniciales (`fixtures/`) que permitan recrear datos base sin el `.sqlite3` del repo.

---

[← Volver al índice](00_INDICE.md)
