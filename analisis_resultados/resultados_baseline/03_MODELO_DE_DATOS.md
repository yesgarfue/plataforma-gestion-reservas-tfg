# 03 — Modelo de Datos

[← Volver al índice](00_INDICE.md)

---

## App: `category`

### `Category` — `category/models.py`

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `category_name` | CharField(20) | unique=True |
| `description` | CharField(255) | blank=True |
| `slug` | CharField(100) | unique=True |
| `cat_image` | ImageField | upload_to='photos/categories', blank=True |

**Métodos:**
- `get_url()` → devuelve la URL de categoría usando el slug
- `__str__()` → devuelve `category_name`

**Tabla generada:** `category_category`

---

## App: `accounts`

### `Account` — `accounts/models.py`

Extiende `AbstractBaseUser` (modelo de usuario personalizado). Configurado como `AUTH_USER_MODEL = 'accounts.Account'` en `settings.py:96`.

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `first_name` | CharField(30) | — |
| `last_name` | CharField(55) | — |
| `username` | CharField(50) | unique=True |
| `email` | CharField(50) | unique=True |
| `phone_number` | CharField(50) | — |
| `date_joinded` | DateTimeField | auto_now_add=True — **typo**: debería ser `date_joined` |
| `last_login` | DateTimeField | auto_now_add=True — **bug**: este campo debería usar `auto_now` o actualizarse al hacer login, no `auto_now_add` |
| `is_admin` | BooleanField | default=False |
| `is_staff` | BooleanField | default=False |
| `is_active` | BooleanField | **default=False** — los usuarios se crean inactivos; deben verificar email |
| `is_superadmin` | BooleanField | default=False |

**USERNAME_FIELD:** `email` (login por email, no por username)

**REQUIRED_FIELDS:** `username`, `first_name`, `last_name`

**Métodos:**
- `full_name()` → `"{first_name} {last_name}"`
- `has_perm(perm, obj)` → devuelve `is_admin`
- `has_module_perms(add_label)` → siempre `True`
- `get_user_by_email(email)` → método estático (sin `@staticmethod`, accede como `Account.get_user_by_email(email)`)

**Tabla generada:** `accounts_account`

---

### `UserProfile` — `accounts/models.py`

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `user` | OneToOneField(Account) | on_delete=CASCADE |
| `address_line_1` | CharField(100) | blank=True |
| `address_line_2` | CharField(100) | blank=True |
| `profile_picture` | ImageField | upload_to='userprofile', blank=True |
| `city` | CharField(20) | blank=True |
| `state` | CharField(5) | blank=True |
| `country` | CharField(20) | blank=True |

**Métodos:**
- `full_address()` → `"{address_line_1} {address_line_2}"`
- `__str__()` → devuelve `user.first_name`

**Tabla generada:** `accounts_userprofile`

---

## App: `store`

> ⚠️ **Bug crítico:** Los modelos `Puerto` y `Fabricante` están definidos **dos veces** en `store/models.py`. Las líneas 8-26 contienen una primera definición completa de ambos modelos, y las líneas 30-43 los redefinen idénticamente. Python simplemente sobreescribe la primera clase con la segunda; funciona pero es un error grave de limpieza.

### `Puerto` — `store/models.py` (líneas 30-36)

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `nombre` | CharField(100) | unique=True |

**Tabla generada:** `store_puerto`

### `Fabricante` — `store/models.py` (líneas 37-43)

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `nombre` | CharField(100) | unique=True |

**Tabla generada:** `store_fabricante`

### `Product` — `store/models.py` (líneas 44-83)

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `product_name` | CharField(200) | unique=True |
| `slug` | CharField(200) | unique=True |
| `description` | TextField(500) | blank=True |
| `price` | IntegerField | default=1 — precio **por día** de alquiler |
| `images` | ImageField | upload_to='photos/products' |
| `stock` | IntegerField | default=1 — número de unidades disponibles |
| `is_available` | BooleanField | default=True |
| `category` | ForeignKey(Category) | on_delete=CASCADE |
| `created_date` | DateTimeField | auto_now_add=True |
| `modified_date` | DateTimeField | auto_now=True |
| `fabricante` | ForeignKey(Fabricante) | on_delete=CASCADE |
| `puerto` | ForeignKey(Puerto) | on_delete=CASCADE |
| `capacidad` | IntegerField | default=4 — número de personas |

**Métodos:**
- `save()` → genera el slug automáticamente desde `product_name`
- `get_url()` → URL de detalle del producto
- `averageReview()` → media de valoraciones activas
- `countReview()` → número de reseñas activas

**Tabla generada:** `store_product`

---

### `Variation` — `store/models.py` (líneas 86-110)

⚠️ **Residuo de la plantilla e-commerce original.** El modelo usa categorías `color` y `talla` (`variation_category_choice`), conceptos propios de una tienda de ropa. Para alquiler de barcos este modelo no tiene sentido funcional real, aunque se mantiene en código (el carrito y pedidos tienen relaciones M2M con él por herencia de la plantilla).

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `product` | ForeignKey(Product) | on_delete=CASCADE |
| `variation_category` | CharField(100) | choices: `color`, `talla` |
| `variation_value` | CharField(100) | — |
| `is_active` | BooleanField | default=True |
| `created_date` | DateTimeField | auto_now=True |

**Manager personalizado:** `VariationManager`
- `colors()` → filtra variaciones de categoría `color`
- `tallas()` → filtra variaciones de categoría `talla`

**Tabla generada:** `store_variation`

---

### `ReviewRating` — `store/models.py` (líneas 113-127)

Modelo de reseñas de usuario sobre un barco. Adaptado parcialmente del e-commerce original.

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `product` | ForeignKey(Product) | on_delete=CASCADE |
| `user` | ForeignKey(Account) | on_delete=CASCADE |
| `subject` | CharField(100) | blank=True |
| `review` | CharField(500) | blank=True |
| `rating` | FloatField | — (sin validators de rango) |
| `ip` | CharField(20) | blank=True |
| `status` | BooleanField | default=True |
| `created_at` | DateTimeField | auto_now_add=True |
| `updated_at` | DateTimeField | auto_now=True |

**Tabla generada:** `store_reviewrating`

---

## App: `carts`

### `Cart` — `carts/models.py`

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `cart_id` | CharField(250) | blank=True — se usa el session_key como identificador |
| `date_added` | DateField | auto_now_add=True |

**Tabla generada:** `carts_cart`

### `CartItem` — `carts/models.py`

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `user` | ForeignKey(Account) | on_delete=CASCADE, null=True — null para usuarios anónimos |
| `product` | ForeignKey(Product) | on_delete=CASCADE |
| `variation` | ManyToManyField(Variation) | blank=True — ⚠️ herencia de la plantilla, no usado funcionalmente |
| `cart` | ForeignKey(Cart) | on_delete=CASCADE, null=True |
| `quantity` | IntegerField | — |
| `fecha_inicio` | DateField | default=hoy+1 |
| `fecha_fin` | DateField | default=hoy+2 |
| `is_active` | BooleanField | default=True |

**Métodos:**
- `duracion()` → días entre `fecha_fin` y `fecha_inicio`
- `sub_total()` → `price × (fecha_fin - fecha_inicio).days`
- `__unicode__()` → devuelve `self.product` (el objeto, no el string — bug menor)

**Tabla generada:** `carts_cartitem`

---

## App: `orders`

### `Payment` — `orders/models.py`

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `user` | ForeignKey(Account) | on_delete=CASCADE |
| `payment_id` | CharField(100) | — (ID de transacción PayPal) |
| `payment_method` | CharField(100) | — |
| `amount_id` | CharField(100) | — (guarda el total como string) |
| `status` | CharField(100) | — |
| `created_at` | DateTimeField | auto_now_add=True |

**Tabla generada:** `orders_payment`

### `Order` — `orders/models.py`

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `user` | ForeignKey(Account) | on_delete=SET_NULL, null=True |
| `payment` | ForeignKey(Payment) | on_delete=SET_NULL, blank=True, null=True |
| `order_number` | CharField(20) | — (formato: `YYYYMMDD` + id) |
| `first_name` | CharField(50) | — |
| `last_name` | CharField(50) | — |
| `phone` | CharField(50) | — |
| `email` | CharField(50) | — |
| `address_line_1` | CharField(100) | — |
| `address_line_2` | CharField(100) | — |
| `country` | CharField(50) | — |
| `city` | CharField(50) | — |
| `state` | CharField(5) | — comentario en código: "QUE ES CODIGO POSTAL EN CHECKOUT.HTML" |
| `order_note` | CharField(100) | blank=True — **contiene el código de seguimiento** (`RES-XXXX`) |
| `order_total` | FloatField | — |
| `tax` | FloatField | — |
| `extra_combustible` | FloatField | — surcharge de 50€ por barcos no-veleros |
| `status` | CharField(50) | choices: Pagado / Pendiente de pago / En uso / Devuelto — **⚠️ `default='New'` no está en las choices; pedidos nuevos nacen con estado inválido** |
| `ip` | CharField(20) | blank=True |
| `is_ordered` | BooleanField | default=False |
| `created_at` | DateTimeField | auto_now_add=True |
| `updated_at` | DateTimeField | auto_now=True |

**Nota semántica:** el campo `order_note` se ha reaprovechado para almacenar el código de seguimiento de la reserva (generado como `RES-<random20>`). Es confuso y mezcla responsabilidades.

**Tabla generada:** `orders_order`

### `OrderProduct` — `orders/models.py`

| Campo | Tipo Django | Restricciones |
|---|---|---|
| `order` | ForeignKey(Order) | on_delete=CASCADE |
| `payment` | ForeignKey(Payment) | on_delete=CASCADE, blank=True, null=True |
| `user` | ForeignKey(Account) | on_delete=CASCADE, null=True, blank=True |
| `product` | ForeignKey(Product) | on_delete=CASCADE |
| `variation` | ManyToManyField(Variation) | blank=True — ⚠️ herencia de plantilla |
| `quantity` | IntegerField | — |
| `product_price` | FloatField | — precio por día en el momento de la reserva |
| `ordered` | BooleanField | default=False |
| `created_at` | DateTimeField | auto_now_add=True |
| `updated_at` | DateTimeField | auto_now=True |
| `fecha_inicio` | DateField | default=hoy+1 |
| `fecha_fin` | DateField | default=hoy+2 |

**Métodos:**
- `clean()` → valida solapamiento de fechas para el mismo producto; lanza `ValidationError`
- `duracion()` → días de la reserva

**Tabla generada:** `orders_orderproduct`

---

## Resumen de tablas generadas

| Tabla | App |
|---|---|
| `category_category` | category |
| `accounts_account` | accounts |
| `accounts_userprofile` | accounts |
| `store_puerto` | store |
| `store_fabricante` | store |
| `store_product` | store |
| `store_variation` | store |
| `store_reviewrating` | store |
| `carts_cart` | carts |
| `carts_cartitem` | carts |
| `carts_cartitem_variation` | carts (M2M automática) |
| `orders_payment` | orders |
| `orders_order` | orders |
| `orders_orderproduct` | orders |
| `orders_orderproduct_variation` | orders (M2M automática) |
| Tablas de Django contrib | django.contrib.* |

---

[← Volver al índice](00_INDICE.md)
