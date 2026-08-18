# API Cine

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.17-A30000)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)

API REST para un catálogo de películas: gestión de películas, categorías y comentarios de usuarios, con autenticación JWT y documentación interactiva.

**Demo en vivo:** https://cine-api-8uih.onrender.com
**Documentación:** [Swagger](https://cine-api-8uih.onrender.com/docs/) · [ReDoc](https://cine-api-8uih.onrender.com/redocs/)

> Desplegado en el plan gratuito de Render: si el servicio estuvo inactivo, la primera petición puede demorar hasta un minuto en responder.

---

## Stack

| Componente | Tecnología |
|---|---|
| Framework | Django 6.0.6 |
| API | Django REST Framework 3.17 |
| Autenticación | djangorestframework-simplejwt (JWT) |
| Base de datos | PostgreSQL (`psycopg2-binary`, `dj-database-url`) |
| Filtros | django-filter |
| Documentación | drf-yasg (Swagger UI + ReDoc) |
| Imágenes | Pillow |
| Servidor | Gunicorn + WhiteNoise |
| Despliegue | Render (aplicación) + Neon (base de datos) |
| Python | 3.14 |

---

## Estructura del proyecto

```
cine_api/
├── cine/                  # Configuración del proyecto (settings, urls, wsgi/asgi)
├── user/                  # Usuario custom + registro y autenticación JWT
├── categorias/            # Géneros de películas
├── peliculas/             # Catálogo de películas
├── comentarios/           # Comentarios de usuarios sobre películas
├── manage.py
└── requirements.txt
```

Cada app de dominio sigue la misma organización:

```
<app>/
├── models.py
├── admin.py
├── migrations/
└── api/
    ├── serializers.py     # Serializers del modelo
    ├── views.py           # ViewSet / APIView
    ├── permissions.py     # Permisos custom
    └── router.py          # Registro de rutas
```

---

## Modelos

### `User` (app `user`)

Extiende `AbstractUser`. **El login se hace con el email**, no con el username.

| Campo | Tipo | Notas |
|---|---|---|
| `email` | EmailField(50) | único, `USERNAME_FIELD` |
| `username` | CharField(150) | único, requerido al registrarse |
| `first_name` / `last_name` | CharField(150) | opcionales |
| `telefono` | CharField(20) | opcional |
| `instagram` | CharField(30) | opcional |
| `twitter` | CharField(30) | opcional |
| `web_site` | CharField(50) | opcional |

### `Categoria` (app `categorias`)

| Campo | Tipo | Notas |
|---|---|---|
| `genero` | CharField(100) | ej. "Terror", "Comedia" |
| `slug` | SlugField | único, se usa como identificador en la URL |

### `Pelicula` (app `peliculas`)

| Campo | Tipo | Notas |
|---|---|---|
| `nombre` | CharField(100) | único, requerido |
| `categoria` | FK → `Categoria` | opcional · `SET_NULL` si se borra la categoría |
| `anio_creacion` | IntegerField | requerido |
| `descripcion` | TextField | requerido |
| `poster` | ImageField | opcional, se sube a `media/peliculas/imagenes/` |
| `estado` | BooleanField | opcional, `False` por defecto |

### `Comentario` (app `comentarios`)

| Campo | Tipo | Notas |
|---|---|---|
| `mensaje` | TextField | requerido |
| `fecha_mensaje` | DateTimeField | solo lectura, se completa solo |
| `estado` | BooleanField | opcional, `False` por defecto |
| `pelicula` | FK → `Pelicula` | opcional · `SET_NULL` |
| `usuario` | FK → `User` | **requerido**, se envía el `id` en el body |

---

## Endpoints

Base: `/api/`

### Autenticación

| Método | Ruta | Descripción | Permiso |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Registro de usuario | Público |
| `POST` | `/api/auth/login/` | Devuelve `access` y `refresh` | Público |
| `POST` | `/api/auth/token/refresh/` | Renueva el `access` token | Público |
| `GET` | `/api/auth/me/` | Datos del usuario autenticado | Autenticado |
| `PUT` | `/api/auth/me/` | Actualiza el perfil | Autenticado |

### Categorías

| Método | Ruta | Permiso |
|---|---|---|
| `GET` | `/api/categoria/` | Público |
| `GET` | `/api/categoria/{slug}/` | Público |
| `POST` | `/api/categoria/` | Staff |
| `PUT` / `PATCH` | `/api/categoria/{slug}/` | Staff |
| `DELETE` | `/api/categoria/{slug}/` | Staff |

Se identifican por **slug**, no por id. Filtro: `?genero=`

### Películas

| Método | Ruta | Permiso |
|---|---|---|
| `GET` | `/api/pelicula/` | Público |
| `GET` | `/api/pelicula/{id}/` | Público |
| `POST` | `/api/pelicula/` | Staff |
| `PUT` / `PATCH` | `/api/pelicula/{id}/` | Staff |
| `DELETE` | `/api/pelicula/{id}/` | Staff |

Filtros: `?estado=`, `?categoria=`
Orden por defecto: `-anio_creacion` (más recientes primero), modificable con `?ordering=`

### Comentarios

| Método | Ruta | Permiso |
|---|---|---|
| `GET` | `/api/comentario/` | Público |
| `POST` | `/api/comentario/` | Público |
| `PUT` / `PATCH` | `/api/comentario/{id}/` | Solo el autor del comentario |
| `DELETE` | `/api/comentario/{id}/` | Solo el autor del comentario |

Filtros: `?estado=`, `?usuario=`, `?pelicula=`
Orden por defecto: `-fecha_mensaje`

### Otros

| Ruta | Descripción |
|---|---|
| `/admin/` | Panel de administración de Django |
| `/docs/` | Swagger UI |
| `/redocs/` | ReDoc |

### Notas sobre las respuestas de listado

Los endpoints de listado **no están paginados**: devuelven un array JSON plano con todos los resultados, sin envoltorio `count` / `next` / `previous`.

```json
[
  { "id": 1, "nombre": "El Padrino", "...": "..." },
  { "id": 2, "nombre": "Interestelar", "...": "..." }
]
```

Los filtros y el ordenamiento se combinan libremente:

```
GET /api/pelicula/?categoria=3&estado=true&ordering=nombre
```

---

## Autenticación JWT

Los tokens se envían en la cabecera `Authorization` con el prefijo `Bearer`.

**Duración:** `access` 10 minutos · `refresh` 1 día.

### 1. Registro

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "fede@example.com",
    "username": "fede",
    "password": "unaClaveSegura123",
    "first_name": "Federico",
    "last_name": "Di Santo"
  }'
```

Responde `200 OK`. `first_name` y `last_name` son opcionales.

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "fede@example.com", "password": "unaClaveSegura123"}'
```

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}
```

> El campo es `email`, no `username`, porque el modelo define `USERNAME_FIELD = "email"`.

### 3. Petición autenticada

```bash
curl http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

```json
{
  "id": 1,
  "email": "fede@example.com",
  "username": "fede",
  "first_name": "Federico",
  "last_name": "Di Santo"
}
```

### 4. Renovar el token

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

### 5. Actualizar el perfil

Solo acepta `PUT` (no `PATCH`). Los seis campos son opcionales:

```bash
curl -X PUT http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Federico",
    "telefono": "+54 11 5555-5555",
    "instagram": "@fede",
    "web_site": "https://fede.dev"
  }'
```

---

## Ejemplos de uso

Los ejemplos usan `http://localhost:8000`. Para probarlos contra el demo, reemplazá esa base por `https://cine-api-8uih.onrender.com`.

### Crear una categoría (requiere staff)

```bash
curl -X POST http://localhost:8000/api/categoria/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"genero": "Ciencia Ficción", "slug": "ciencia-ficcion"}'
```

### Crear una película sin póster (requiere staff)

```bash
curl -X POST http://localhost:8000/api/pelicula/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Interestelar",
    "categoria": 1,
    "anio_creacion": 2014,
    "descripcion": "Un grupo de exploradores atraviesa un agujero de gusano.",
    "estado": true
  }'
```

`categoria` es el **id** de la categoría, no el slug.

### Crear una película con póster

`poster` es un archivo, así que **no se puede enviar como JSON**: hay que usar `multipart/form-data`.

```bash
curl -X POST http://localhost:8000/api/pelicula/ \
  -H "Authorization: Bearer <access_token>" \
  -F "nombre=Interestelar" \
  -F "categoria=1" \
  -F "anio_creacion=2014" \
  -F "descripcion=Un grupo de exploradores atraviesa un agujero de gusano." \
  -F "estado=true" \
  -F "poster=@/ruta/a/poster.jpg"
```

La respuesta devuelve `poster` como la URL del archivo servido bajo `/media/`.

> **Sobre las imágenes en el demo:** el plan gratuito de Render no incluye disco persistente, así que los archivos subidos no sobreviven a un redespliegue. La carga de imágenes se puede probar localmente.

### Crear un comentario

```bash
curl -X POST http://localhost:8000/api/comentario/ \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "Una obra maestra.",
    "pelicula": 1,
    "usuario": 1
  }'
```

`usuario` es obligatorio y se envía como id en el body.

### Filtrar y ordenar

```bash
# Películas activas de la categoría 2, de la más vieja a la más nueva
curl "http://localhost:8000/api/pelicula/?categoria=2&estado=true&ordering=anio_creacion"

# Comentarios de una película
curl "http://localhost:8000/api/comentario/?pelicula=1"

# Categoría por slug
curl "http://localhost:8000/api/categoria/ciencia-ficcion/"
```

---

## Códigos de estado

| Código | Cuándo |
|---|---|
| `200 OK` | Lecturas, actualizaciones y el registro de usuario |
| `201 Created` | Creación de categorías, películas y comentarios |
| `204 No Content` | Borrado exitoso |
| `400 Bad Request` | Error de validación |
| `401 Unauthorized` | Falta el token, está vencido, o la operación exige autenticación |
| `403 Forbidden` | Autenticado pero sin permisos (ej. usuario común creando una película) |
| `404 Not Found` | El recurso no existe |

### Formato de los errores

**Validación (400)** — un objeto con una lista de mensajes por campo:

```json
{
  "email": ["user with this email already exists."],
  "anio_creacion": ["A valid integer is required."]
}
```

**Credenciales incorrectas en el login (401):**

```json
{ "detail": "No active account found with the given credentials" }
```

**Token vencido o inválido (401):**

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

**Sin permisos (403):**

```json
{ "detail": "You do not have permission to perform this action." }
```

---

## Instalación local

### Requisitos

- Python 3.14
- PostgreSQL corriendo en local

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/FedericoDiSanto/cine_api.git
cd cine_api

# 2. Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear la base de datos
createdb cine_db

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear un superusuario (necesario para las operaciones de staff)
python manage.py createsuperuser

# 7. Levantar el servidor
python manage.py runserver
```

La API queda en `http://localhost:8000/api/` y la documentación en `http://localhost:8000/docs/`.

> Al crear el superusuario, Django pide primero el **email** (es el `USERNAME_FIELD`) y después el username.

### Base de datos

En desarrollo se usa la configuración de PostgreSQL definida en `cine/settings.py`:

```
NAME: cine_db
USER: fede
HOST: localhost
PORT: 5432
```

Si tu usuario de PostgreSQL es distinto, ajustá ese bloque o definí la variable de entorno `DATABASE_URL`, que tiene prioridad sobre la configuración local.

### Datos de ejemplo

El repositorio incluye un fixture con películas de ejemplo:

```bash
python manage.py loaddata peliculas.json
```

---

## Variables de entorno

Toda la configuración que cambia entre desarrollo y producción se lee del entorno. En local no hace falta definir ninguna: cada una tiene un valor por defecto pensado para desarrollo.

| Variable | Descripción | Por defecto |
|---|---|---|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL (`postgres://usuario:clave@host:puerto/base`). Si está definida, se usa en lugar de la configuración local. | — (usa la config local) |
| `SECRET_KEY` | Clave de firma de Django. | clave de desarrollo |
| `DEBUG` | `True` o `False`. | `True` |
| `ALLOWED_HOSTS` | Dominios permitidos, separados por coma. | `*` |
| `CSRF_TRUSTED_ORIGINS` | Orígenes confiables para CSRF, con protocolo, separados por coma. | vacío |
| `PORT` | Puerto en el que escucha Gunicorn. Lo inyecta la plataforma. | — |

---

## Tests

El proyecto todavía no tiene tests escritos. La suite se ejecuta con:

```bash
python manage.py test
```

---

## Despliegue

La aplicación corre en **Render** y la base de datos en **Neon**. Están separadas a propósito: el servidor de aplicación es descartable y se reconstruye en cada deploy, mientras que los datos persisten en un servicio dedicado.

**Build command:**

```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start command:**

```
gunicorn cine.wsgi:application
```

Las migraciones se aplican en cada build y los archivos estáticos los sirve WhiteNoise. Cada push a `main` dispara un nuevo despliegue automático.

La conexión a la base se resuelve por la variable `DATABASE_URL`, así que el mismo código funciona en local y en producción sin cambios.

---

## Panel de administración

Todos los modelos están registrados en el admin de Django (`/admin/`):

- **Usuarios** — con secciones separadas para información personal, permisos y redes sociales
- **Películas** — listado con nombre, categoría, año y estado
- **Categorías** — listado por género
- **Comentarios** — listado con usuario, película, fecha y estado

---

## Autor

**Federico Di Santo** — [GitHub](https://github.com/FedericoDiSanto) · [LinkedIn](https://www.linkedin.com/in/di-santo-federico-javier/)