# Práctica: Desarrollo Backend con Django, DRF, Swagger y JWT (`portal_universitario`)

Este proyecto corresponde al seguimiento del **Manual de Desarrollo Full Stack con Django y ReactJS (Páginas 5 a 12)**, aplicando todas las adaptaciones solicitadas y corrigiendo las vulnerabilidades de seguridad presentes en el código original del manual.

---

## 1. Cambios Implementados

1. **Nombre y tema propio del proyecto**:
   - El proyecto se nombró **`portal_universitario`** (en lugar de `restaurante`).
   - En `portal_universitario/urls.py`, la documentación de **Swagger (`drf-yasg`)** lleva el título **`"Portal Universitario API"`** y descripción personalizada.
2. **Campos extra en el modelo `User`**:
   - En `users/models.py`, se agregaron los campos **`matricula`** (`CharField`) y **`carrera`** (`CharField`) al modelo `User` que hereda de `AbstractUser`, manteniendo el login por `email` (`USERNAME_FIELD = 'email'`).
   - **Admin de Django (`users/admin.py`)**: Se configuró `UserAdmin` heredando de `BaseUserAdmin` para que `matricula` y `carrera` aparezcan tanto en la tabla principal (`list_display`) como en los formularios de edición (`fieldsets`) y creación (`add_fieldsets`).
   - **Serializer y Swagger (`users/serializers.py`)**: Se incluyeron `'matricula'` y `'carrera'` dentro de `fields` en `UserSerializer`, por lo que se visualizan y documentan automáticamente en **Swagger** (`/swagger/`) y **ReDoc** (`/redoc/`).
3. **Configuración de `ACCESS_TOKEN_LIFETIME`**:
   - En `portal_universitario/settings.py`, se importó `timedelta` y se añadió el diccionario `SIMPLE_JWT` configurando explícitamente `'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60)` (1 hora) y `'REFRESH_TOKEN_LIFETIME': timedelta(days=7)`.

---

## 2. Errores de Seguridad Encontrados y Corregidos

### Falla 1: Exposición del hash de la contraseña en las respuestas de la API
- **Causa en el manual**: En `UserSerializer` (`users/serializers.py`), el campo `'password'` se incluyó en `fields` sin ninguna restricción de lectura. Como consecuencia, al listar usuarios (`GET /api/v1/users/`), consultar un usuario o llamar al endpoint de datos personales (`GET /api/v1/auth/me/`), la API devolvía el hash PBKDF2 de la contraseña en el JSON de respuesta.
- **Solución aplicada**: Se agregó `extra_kwargs = {'password': {'write_only': True, 'required': False}}` dentro de la clase `Meta` de `UserSerializer`. De esta manera, la contraseña se puede recibir al crear o actualizar un usuario, pero **jamás** es incluida en ninguna respuesta de la API (incluido `/api/v1/auth/me/`).

### Falla 2: Sobrescritura de la contraseña con la del usuario que hace la petición al actualizar sin enviar contraseña
- **Causa en el manual**: En `UserApiViewSet.partial_update` (`users/views.py`), el manual tenía el siguiente bloque:
  ```python
  if "password" in request.data:
      request.data["password"] = make_password(request.data["password"])
  else:
      request.data["password"] = request.user.password
  ```
  Cuando un administrador actualizaba los datos de otro usuario sin enviar el campo `password`, entraba al `else` y le asignaba `request.user.password` (¡la contraseña del administrador que estaba haciendo la petición!).
- **Solución aplicada**: Se eliminó el bloque `else` dañino y se validó que solo cuando `password` venga en la petición con contenido (`if password:`) se aplique `make_password(password)`. Si no se envía o viene vacía, se elimina del diccionario de entrada (`request.data.pop('password')`) para que Django conserve intacta la contraseña original del usuario modificado.

---

## 3. Instrucciones de Ejecución

```bash
cd backend
python -m venv venv
# En Windows:
./venv/Scripts/activate
# En Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Rutas principales:
- **Panel Admin**: `http://127.0.0.1:8000/admin/`
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`
- **CRUD Usuarios**: `http://127.0.0.1:8000/api/v1/users/`
- **Datos Personales (Me)**: `http://127.0.0.1:8000/api/v1/auth/me/`
- **Login JWT (Access & Refresh)**: `http://127.0.0.1:8000/api/v1/auth/token/`
