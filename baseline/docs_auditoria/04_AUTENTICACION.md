# 04 — Autenticación y Autorización

[← Volver al índice](00_INDICE.md)

---

## Modelo de usuario personalizado

El proyecto usa un modelo de usuario propio configurado en `settings.py:96`:

```python
AUTH_USER_MODEL = 'accounts.Account'
```

Definido en `accounts/models.py`, extiende `AbstractBaseUser` con `MyAccountManager` como manager.

### Campos del modelo `Account`

| Campo | Tipo | Notas |
|---|---|---|
| `first_name` | CharField(30) | — |
| `last_name` | CharField(55) | — |
| `username` | CharField(50) | unique; se genera automáticamente como la parte local del email (`email.split("@")[0]`) |
| `email` | CharField(50) | unique; es el campo de login (`USERNAME_FIELD`) |
| `phone_number` | CharField(50) | — |
| `date_joinded` | DateTimeField | auto_now_add — **typo** (debería ser `date_joined`) |
| `last_login` | DateTimeField | auto_now_add — **bug**: nunca se actualiza tras iniciar sesión |
| `is_admin` | BooleanField | default=False; controla acceso a vistas de administración custom |
| `is_staff` | BooleanField | default=False; acceso al `/securelogin/` (admin Django) |
| `is_active` | BooleanField | **default=False**; los nuevos usuarios deben verificar su email para activarse |
| `is_superadmin` | BooleanField | default=False; se setea al crear superusuario |

---

## Flujo de registro

Vistas: `accounts/views.py:23–65` | Template: `templates/accounts/register.html`

1. El usuario rellena `RegistrationForm` (nombre, apellidos, teléfono, email, contraseña).
2. Se valida la contraseña con `CustomPasswordValidator` (ver sección validadores).
3. Se crea el usuario con `is_active=False`.
4. Se genera un `username` como `email.split("@")[0]`.
5. Se crea un `UserProfile` asociado con `profile_picture = 'default/default-user.png'` — **⚠️ esta imagen no existe** en el repositorio (el directorio `media/default/` no está presente).
6. Se envía un email de activación con un token firmado (`default_token_generator`) usando la plantilla `accounts/account_verification_email.html`.
7. Se redirige a `/accounts/login/?command=verification&email=<email>`.

---

## Flujo de login

Vistas: `accounts/views.py:67–148` | Template: `templates/accounts/login.html`

1. Se autentica con `auth.authenticate(email=email, password=password)`.
2. Si la autenticación es exitosa, se migra el carrito anónimo al usuario (merge de cart items).
3. Se hace `auth.login(request, user)` y se redirige a `next` o a `home`.
4. Si falla:
   - Si el email no existe → mensaje genérico de error.
   - Si el usuario existe pero no está activo → se reenvía el email de activación automáticamente.
   - Si el usuario existe y está activo pero la contraseña es incorrecta → mensaje genérico de error (no distingue para evitar enumeración de usuarios).

---

## Flujo de recuperación de contraseña

Vistas: `accounts/views.py:192–262`

| Paso | Vista | URL | Template |
|---|---|---|---|
| 1. Formulario de email | `forgotPassword` | `/accounts/forgotPassword/` | `accounts/forgotPassword.html` |
| 2. Email con enlace | — (send via `EmailMessage`) | — | `accounts/reset_password_email.html` |
| 3. Validación del token | `resetpassword_validate` | `/accounts/resetpassword_validate/<uidb64>/<token>/` | — (redirect) |
| 4. Nueva contraseña | `resetPassword` | `/accounts/resetPassword/` | `accounts/resetPassword.html` |

El enlace de recuperación usa `urlsafe_base64_encode(force_bytes(user.pk))` + `default_token_generator.make_token(user)`. El token se verifica en paso 3 y el UID se guarda en sesión (`request.session['uid']`) para recuperarlo en el paso 4.

---

## Activación de cuenta

Vista: `accounts/views.py:158–172` | URL: `/accounts/activate/<uidb64>/<token>/`

Decodifica el UID, verifica el token con `default_token_generator.check_token(user, token)`, y si es válido setea `is_active = True`.

---

## Validadores de contraseña

Definido en `accounts/validators.py`. Configurado en `settings.py:113-117`:

```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'accounts.validators.CustomPasswordValidator'},
]
```

**Reglas:**
- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos una letra minúscula
- Al menos un dígito
- Al menos un carácter especial de: `!@#$%^&*(),.?:{}|<>_-`

El validador se aplica tanto en registro (`RegistrationForm.clean()`) como en cambio y reset de contraseña (via `validate_password()`).

---

## Permisos y roles

No hay grupos de Django ni sistema de permisos granular. El control de acceso se basa en dos flags booleanos del modelo `Account`:

| Flag | Uso |
|---|---|
| `is_admin` | Controla acceso a vistas custom de gestión (CRUD usuarios, barcos, reservas). Verificado con `@user_passes_test(lambda u: u.is_admin)`. |
| `is_staff` | Permite acceso al panel Django admin (`/securelogin/`). |

**Vistas protegidas con `@login_required`:**
- `logout`, `dashboard`, `edit_profile`, `change_password`
- CRUD de barcos: `product_list`, `edit_ship`, `delete_ship`, `create_ship`
- CRUD de reservas: `order_list`, `edit_order`, `delete_order`
- CRUD de usuarios: `list_users`, `create_users`, `edit_user`

**⚠️ Vista sin protección:** `delete_user` (`accounts/views.py:431`) NO tiene ni `@login_required` ni `@user_passes_test`. Cualquier usuario anónimo puede enviar una petición GET a `/accounts/delete_user/<id>/` y eliminar una cuenta.

---

## Middleware de sesiones

`django_session_timeout.middleware.SessionTimeoutMiddleware` configurado en `settings.py:66`.

| Parámetro | Valor |
|---|---|
| `SESSION_EXPIRE_SECONDS` | 1800 (30 minutos) |
| `SESSION_EXPIRE_AFTER_LAST_ACTIVITY` | True — reinicia el timer con cada petición |
| `SESSION_TIMEOUT_REDIRECT` | `'accounts/login'` — sin barra inicial, puede causar redirección relativa incorrecta |

---

## Configuración SMTP

Definida directamente en `settings.py:27-33` (ver [07_CONFIGURACION.md](07_CONFIGURACION.md) para el problema de seguridad):

| Parámetro | Valor |
|---|---|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | 587 (TLS) |
| `EMAIL_USE_TLS` | True |
| `EMAIL_HOST_USER` | `hundidosgestion@gmail.com` |
| `EMAIL_HOST_PASSWORD` | **credencial retirada del repositorio; debe configurarse de forma segura** |
| `DEFAULT_FROM_EMAIL` | `hundidosgestion@gmail.com` |

Se usa para:
- Enviar email de verificación de cuenta al registrarse
- Reenviar email de verificación al intentar login con cuenta inactiva
- Enviar email de recuperación de contraseña
- Enviar confirmación de reserva al pagar (PayPal o contra-reembolso)

---

[← Volver al índice](00_INDICE.md)
