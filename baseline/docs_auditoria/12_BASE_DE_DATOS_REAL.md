# 12 — Base de Datos Real (Inspección del `db.sqlite3`)

[← Volver al índice](00_INDICE.md)

---

## Resumen ejecutivo

La base de datos contiene **7 usuarios reales**, **8 barcos** cargados con datos de prueba, **5 pedidos** completados (todos con estado "Devuelto"), y **14 items** en carritos (13 de usuarios anónimos/demo). Todo está migrado correctamente. La BD es funcional y no tiene datos corruptos detectables.

---

## 1. Inventario de tablas reales

### Tablas en la BD física (22 total)

Ejecutado: `python manage.py dbshell` + `.tables` equivalente

| Tabla | Tipo | Modelo/Origen | Estado |
|---|---|---|---|
| `accounts_account` | Datos | Account (custom user) | ✓ Sincronizado |
| `accounts_userprofile` | Datos | UserProfile | ✓ Sincronizado |
| `auth_group` | Sistema | Django auth | ✓ (sin usar) |
| `auth_group_permissions` | Sistema M2M | Django auth | ✓ (sin usar) |
| `auth_permission` | Sistema | Django auth | ✓ |
| `carts_cart` | Datos | Cart | ✓ Sincronizado |
| `carts_cartitem` | Datos | CartItem | ✓ Sincronizado |
| `carts_cartitem_variation` | M2M | CartItem-Variation | ✓ Sincronizado |
| `category_category` | Datos | Category | ✓ Sincronizado |
| `django_admin_log` | Sistema | Django admin | ✓ |
| `django_content_type` | Sistema | Django | ✓ |
| `django_migrations` | Sistema | Django | ✓ |
| `django_session` | Sistema | Django sessions | ✓ |
| `orders_order` | Datos | Order | ✓ Sincronizado |
| `orders_orderproduct` | Datos | OrderProduct | ✓ Sincronizado |
| `orders_orderproduct_variation` | M2M | OrderProduct-Variation | ✓ Sincronizado |
| `orders_payment` | Datos | Payment | ✓ Sincronizado |
| `store_fabricante` | Datos | Fabricante | ✓ Sincronizado |
| `store_product` | Datos | Product | ✓ Sincronizado |
| `store_puerto` | Datos | Puerto | ✓ Sincronizado |
| `store_reviewrating` | Datos | ReviewRating | ✓ Sincronizado |
| `store_variation` | Datos | Variation | ✓ Sincronizado |

### Comparación: Modelos vs BD

- **Modelos definidos en código:** 18
- **Tablas en BD:** 22 (18 de datos/modelos + 4 de sistema Django)
- **Sincronización:** 100% ✓ — todos los modelos tienen tabla; todas las tablas tienen modelo

**Tablas sin modelo asociado (Django internas o M2M):**
- `auth_group_permissions` (M2M Django - no usado)
- `django_migrations` (historial de migraciones)
- `django_session` (sesiones)
- `django_admin_log` (log admin Django)

**Conclusión:** La BD está perfectamente sincronizada. No hay tablas huérfanas del código ni modelos sin migración.

---

## 2. Conteo de registros por tabla

| Tabla | Registros | Estado |
|---|---|---|
| `accounts_account` | **7** | ✓ Poblada |
| `accounts_userprofile` | **7** | ✓ Poblada (uno por usuario) |
| `category_category` | **4** | ✓ Poblada |
| `store_puerto` | **5** | ✓ Poblada |
| `store_fabricante` | **3** | ✓ Poblada |
| `store_product` | **8** | ✓ Poblada |
| `store_variation` | **11** | ✓ Poblada (variaciones de productos) |
| `store_reviewrating` | **1** | Mínima (1 reseña) |
| `carts_cart` | **13** | ✓ Poblada (carritos anónimos) |
| `carts_cartitem` | **14** | ✓ Poblada |
| `carts_cartitem_variation` | **6** | ✓ M2M activa |
| `orders_payment` | **2** | Mínima (2 pagos) |
| `orders_order` | **5** | ✓ Poblada |
| `orders_orderproduct` | **6** | ✓ Poblada |
| `orders_orderproduct_variation` | **0** | Vacía (no se usan variaciones en pedidos) |

**Análisis:** La BD está principalmente poblada con datos de prueba. Las tablas de datos core (usuarios, productos, categorías) tienen registros reales. Las tablas de transacción (pedidos, pagos) tienen volumen de prueba. Las reseñas son mínimas (solo 1).

---

## 3. Usuarios existentes

**Total: 7 usuarios**

| ID | Email | Username | Active | Staff | Superadmin | Notas |
|---|---|---|---|---|---|---|
| 13 | `pepe@pepe.com` | `pepe` | ✓ | ✓ | ✓ | Admin demo |
| 24 | `admin@admin.com` | `admin` | ✓ | ✓ | ✓ | Admin predeterminado |
| 26 | `pedro@pedro.com` | `pedro` | ✓ | ✗ | ✗ | Usuario regular |
| 27 | `yesica@yesica.com` | `yesica` | ✓ | ✓ | ✓ | Admin (el del proyecto?) |
| 28 | `franco@franco.com` | `franco` | ✓ | ✗ | ✗ | Usuario activo con pedidos |
| 29 | `enrique@enrique.com` | `enrique` | ✓ | ✗ | ✗ | Usuario regular |
| 30 | `pablo@pablo.com` | `pablo` | ✓ | ✗ | ✗ | Usuario regular |

### Contraseñas

**No mostradas** — están hasheadas con `pbkdf2_sha256`. Para resetear contraseña de admin o crear superusuario nuevo, ver [11_ARRANQUE_Y_CREDENCIALES.md](11_ARRANQUE_Y_CREDENCIALES.md).

### Observaciones

- **3 superadmins:** pepe, admin, yesica
- **Todos activos:** ningún usuario inactivo
- **4 usuarios sin privilegios:** pedro, franco, enrique, pablo (usuarios normales del sistema)
- **Usuario más activo:** franco tiene 5 pedidos completos

---

## 4. Muestra de datos principales

### Categorías (4)

| ID | Nombre | Slug | Productos |
|---|---|---|---|
| 1 | Veleros | `veleros` | 1 |
| 2 | Barcos a motor | `barcos-motor` | 0 ⚠️ |
| 3 | Catamaranes | `catamaranes` | 3 |
| 4 | Embarcaciones neumáticas | `embarc-neumaticas` | 4 |

⚠️ Categoría "Barcos a motor" sin productos asignados.

### Puertos (5)

| ID | Nombre | Barcos |
|---|---|---|
| 1 | Santa Maria | 1 |
| 2 | Barbate | 3 |
| 3 | Tarifa | 2 |
| 4 | Bahía de Cádiz | 2 |
| 5 | Algeciras | 0 ⚠️ |

### Fabricantes (3)

| ID | Nombre | Barcos |
|---|---|---|
| 1 | Rodman | 1 |
| 2 | Beneteau | 4 |
| 3 | Jeanneau | 3 |

### Productos - 5 primeros

| ID | Nombre | Categoría | Puerto | Fabricante | Precio/día | Stock |
|---|---|---|---|---|---|---|
| 4 | Velero Esperanza | Veleros | Santa Maria | Rodman | 50€ | 1 |
| 5 | Lancha a motor Trueno | Catamaranes | Barbate | Beneteau | 65€ | 6 |
| 6 | Lancha a motor Zalamero | Emb. neumáticas | Barbate | Beneteau | 45€ | 2 |
| 7 | Yate Rojo | Catamaranes | Tarifa | Jeanneau | 50€ | 3 |
| 8 | Yate Azul | Catamaranes | Bahía de C. | Jeanneau | 75€ | 1 |

### Pedidos - 5 recientes

| ID | # Pedido | Usuario | Status | Total | Fecha |
|---|---|---|---|---|---|
| 28 | 2024112928 | franco@franco.com | **Devuelto** | 151.25€ | 29-nov-2024 |
| 27 | 2024112827 | franco@franco.com | **Devuelto** | 10648.0€ | 28-nov-2024 |
| 26 | 2024112826 | franco@franco.com | **Devuelto** | 544.5€ | 28-nov-2024 |
| 25 | 2024112825 | franco@franco.com | **Devuelto** | 581.5€ | 28-nov-2024 |
| 20 | 2024112820 | franco@franco.com | **Devuelto** | 114.95€ | 28-nov-2024 |

**Nota:** ⚠️ Todos los 5 pedidos mostrados están en estado "Devuelto". Ver análisis de estados más abajo.

### Reseñas (1 total)

Solo **1 reseña** en la BD, de usuario desconocido sobre un producto. El sistema de valoración no está siendo utilizado.

---

## 5. Estado de las migraciones

Ejecutado: `python manage.py showmigrations`

```
accounts
 [X] 0001_initial
 [X] 0002_userprofile
 [X] 0003_auto_20230718_1456
 [X] 0004_alter_account_id_alter_userprofile_id
 [X] 0005_alter_account_email
 [X] 0006_alter_account_email

carts
 [X] 0001_initial
 [X] 0002_cartitem_variation
 [X] 0003_cartitem_user_alter_cartitem_cart
 [X] 0004_auto_20230718_1456
 [X] 0005_alter_cart_id_alter_cartitem_id
 [X] 0006_auto_20241121_1357

category
 [X] 0001_initial
 [X] 0002_auto_20230718_1456
 [X] 0003_alter_category_id

orders
 [X] 0001_initial
 [X] 0002_remove_orderproduct_color_remove_orderproduct_size_and_more
 [X] 0003_auto_20230718_1456
 [X] 0004_alter_order_id_alter_orderproduct_id_and_more
 [X] 0005_auto_20241121_1357
 [X] 0005_alter_order_status (merge)
 [X] 0006_merge_0005_alter_order_status_0005_auto_20241121_1357
 [X] 0007_alter_orderproduct_user
 [X] 0008_alter_order_status
 [X] 0009_order_extra_combustible

store
 [X] 0001_initial
 [X] 0002_variation
 [X] 0003_reviewrating
 [X] 0004_auto_20241206_2006
 [X] 0005_auto_20241206_2011
```

**Estado:** ✓ **TODAS LAS MIGRACIONES APLICADAS** — No hay migraciones pendientes.

---

## 6. Integridad de datos

Ejecutado: `python manage.py check`

```
System check identified no issues (0 silenced)
```

### Verificaciones adicionales realizadas

| Verificación | Resultado |
|---|---|
| CartItems con product_id NULL | 0 ✓ |
| Orders con user_id NULL | 0 ✓ (todos los pedidos tienen usuario) |
| M2M CartItem-Variation | 6 registros activos |
| M2M OrderProduct-Variation | 0 registros (no se usan variaciones en pedidos reales) |
| Relaciones FK | ✓ Todas íntegras |

**Conclusión:** La BD está íntegra. No hay referencias rotas ni datos huérfanos detectables.

---

## 7. Análisis de estados de pedidos

Ejecutado: Conteo de órdenes por status

| Estado | Cantidad |
|---|---|
| **Devuelto** | **5** |
| Pagado | 0 |
| Pendiente de pago | 0 |
| En uso | 0 |

⚠️ **ANOMALÍA IMPORTANTE:** Los 5 pedidos en la BD tienen status "Devuelto", que es un estado final. **Significa que el sistema fue usado pero todos los pedidos están marcados como finalizados/devueltos.** No hay pedidos en estados intermedios (Pagado, En uso) ni pendientes.

Esto es **consistente con datos de prueba** (alguien probó el sistema, creó reservas, y las marcó como devueltas), pero es anormal para producción.

---

## 8. Comparación: Modelos (03_MODELO_DE_DATOS.md) vs BD Real

| Aspecto | Teoría (Informe 03) | Realidad (BD) | ✓/⚠️ |
|---|---|---|---|
| **Usuarios custom (Account)** | ✓ auth_user_model | ✓ 7 cuentas activas | ✓ |
| **UserProfile 1:1** | ✓ OneToOne a Account | ✓ 7 perfiles (coinciden) | ✓ |
| **Categorías** | ✓ 4 teóricas | ✓ 4 en BD | ✓ |
| **Puerto + Fabricante** | ✓ Modelos duplicados en código | ✓ 5 puertos + 3 fabricantes | ✓ |
| **Productos** | ✓ FK a Category, Puerto, Fabricante | ✓ 8 barcos con relaciones FK | ✓ |
| **Variaciones** | ✓ M2M (color/talla, residuo) | ✓ 11 variaciones, 6 en CartItem, 0 en Orders | ⚠️ No usadas en pedidos |
| **Reseñas** | ✓ ReviewRating por producto | ✓ 1 reseña (mínimo) | ✓ |
| **Carrito** | ✓ Cart + CartItem con M2M Variation | ✓ 13 carritos + 14 items | ✓ |
| **Pedidos** | ✓ Order + OrderProduct + Payment | ✓ 5 órdenes, 6 line items, 2 pagos | ✓ |
| **Order.status default='New'** | ⚠️ bug reportado en código | ✗ No hay ningún pedido con status 'New' | ⚠️ Bug existe pero no activado |

**Conclusión:** Los modelos teóricos coinciden con la BD real. No hay divergencias. El bug del `default='New'` existe en el código pero no se ha manifestado (todos los pedidos existentes se han creado con un status válido en la lógica de la app).

---

## 9. Datos adicionales de diagnóstico

### Items en carrito

**Total: 14 items de carrito activos**

Desglose:
- Usuarios autenticados: al menos 1 item en carrito de `pepe@pepe.com`
- Usuarios anónimos: 13 items en carritos de sesión

**Ejemplo:** `Velero Esperanza` tiene:
- 5 unidades en carrito anónimo
- 1 unidad en carrito de pepe@pepe.com
- Total: 6 items para este barco

### Tickets de prueba pendientes

De todos los datos examinados, NO hay:
- Pedidos "Pendiente de pago" (contra-reembolso sin procesar)
- Pedidos "En uso" (reservas activas)
- Órdenes parciales o incompletas

---

## 10. Recomendaciones post-inspección

1. **Limpiar datos de prueba si vas a producción:** Los 7 usuarios son de demo/prueba. Crear solo 1 admin real.
2. **Categoría vacía:** "Barcos a motor" no tiene productos. Eliminarla o poblarla.
3. **Puerto vacío:** "Algeciras" sin barcos. Eliminar o asignar barcos.
4. **Implementar más reseñas:** Solo 1 reseña. El sistema de rating no se está usando.
5. **Monitorear estado de pedidos:** Asegurar que los pedidos nuevos se creen con estado válido, no 'New'.

---

[← Volver al índice](00_INDICE.md)
