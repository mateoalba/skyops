# ✈️ SkyOps API

Sistema de Control de Vuelos — API REST construida con Django y PostgreSQL, desplegada en Azure con CI/CD automático.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Django](https://img.shields.io/badge/Django-5.0+-green)
![DRF](https://img.shields.io/badge/DRF-3.15+-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue)
![Tests](https://img.shields.io/badge/Tests-86%20passed-brightgreen)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black)
![Deploy](https://img.shields.io/badge/Deploy-Azure%20VM-0078D4)

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Base de datos](#base-de-datos)
- [Uso](#uso)
- [Endpoints](#endpoints)
- [Autenticación](#autenticación)
- [Filtros](#filtros)
- [Tests](#tests)
- [Roles y permisos](#roles-y-permisos)
- [Despliegue en Azure](#despliegue-en-azure)
- [CI/CD con GitHub Actions](#cicd-con-github-actions)

---

## Descripción

SkyOps es una API REST para la gestión y control operativo de un aeropuerto. Permite administrar vuelos, pasajeros, reservas, tripulación, aeronaves e incidentes con autenticación JWT y control de acceso por roles.

🌐 **API en producción:** `https://alba-vuelos.uaeftt-ute.site/api/`
📖 **Documentación Swagger:** `https://alba-vuelos.uaeftt-ute.site/api/docs/`
❤️ **Health check:** `https://alba-vuelos.uaeftt-ute.site/api/health/`

---

## Tecnologías

- **Python 3.12**
- **Django 5.0** — framework web
- **Django REST Framework** — API REST
- **PostgreSQL** — base de datos
- **SimpleJWT** — autenticación con tokens JWT
- **drf-spectacular** — documentación OpenAPI / Swagger
- **django-filter** — filtros avanzados
- **pytest-django** — tests automatizados
- **uv** — gestor de paquetes
- **Gunicorn** — servidor WSGI para producción
- **Nginx** — reverse proxy
- **GitHub Actions** — CI/CD automático
- **Azure VM** — infraestructura cloud

---

## Estructura del proyecto

```
skyops/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Pipeline CI/CD
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── airport/
│   ├── models/
│   │   ├── aerolinea.py
│   │   ├── aeropuerto.py
│   │   ├── aeronave.py
│   │   ├── puerta.py
│   │   ├── vuelo.py
│   │   ├── pasajero.py
│   │   ├── reserva.py
│   │   ├── tripulante.py
│   │   ├── asignacion_tripulacion.py
│   │   └── incidente.py
│   ├── serializers/
│   ├── views/
│   ├── tests/
│   ├── admin.py
│   ├── filters.py
│   ├── pagination.py
│   ├── permissions.py
│   └── urls.py
├── .env.example
├── .gitignore
├── manage.py
├── pytest.ini
├── pyproject.toml
└── seed_data.py
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/mateoalba/skyops.git
cd skyops
```

### 2. Crear entorno virtual e instalar dependencias

```bash
uv venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

uv sync
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus datos.

---

## Configuración

Crea el archivo `.env` en la raíz del proyecto:

```env
# Django
SECRET_KEY=django-insecure-cambia-esto-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=skyops_db
DB_USER=skyops_user
DB_PASSWORD=skyops_pass
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOW_ALL_ORIGINS=True

# Test database
TEST_DB_NAME=skyops_test_db
```

---

## Base de datos

### Crear usuario y base de datos en PostgreSQL

```sql
CREATE USER skyops_user WITH PASSWORD 'skyops_pass';
CREATE DATABASE skyops_db OWNER skyops_user;
GRANT ALL PRIVILEGES ON DATABASE skyops_db TO skyops_user;
ALTER USER skyops_user CREATEDB;
```

### Aplicar migraciones

```bash
uv run python manage.py migrate
```

### Crear superusuario

```bash
uv run python manage.py createsuperuser
```

### Cargar datos de prueba

```bash
# Windows
Get-Content seed_data.py | uv run python manage.py shell

# Mac/Linux
uv run python manage.py shell < seed_data.py
```

### Crear grupos de usuarios

```bash
# Windows
Get-Content crear_grupos.py | uv run python manage.py shell

# Mac/Linux
uv run python manage.py shell < crear_grupos.py
```

---

## Uso

```bash
uv run python manage.py runserver
```

| URL | Descripción |
|-----|-------------|
| `http://127.0.0.1:8000/api/` | Listado de endpoints |
| `http://127.0.0.1:8000/api/docs/` | Documentación Swagger |
| `http://127.0.0.1:8000/api/redoc/` | Documentación ReDoc |
| `http://127.0.0.1:8000/admin/` | Panel de administración |
| `http://127.0.0.1:8000/api/health/` | Health check |

---

## Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Obtener tokens JWT |
| POST | `/api/auth/refresh/` | Renovar access token |
| POST | `/api/auth/registro/` | Crear cuenta |
| POST | `/api/auth/logout/` | Cerrar sesión |
| GET/PUT | `/api/auth/perfil/` | Ver y editar perfil |
| POST | `/api/auth/cambiar-password/` | Cambiar contraseña |

### Recursos principales

| Recurso | Endpoint base |
|---------|--------------|
| Aerolíneas | `/api/aerolineas/` |
| Aeropuertos | `/api/aeropuertos/` |
| Aeronaves | `/api/aeronaves/` |
| Puertas | `/api/puertas/` |
| Vuelos | `/api/vuelos/` |
| Pasajeros | `/api/pasajeros/` |
| Reservas | `/api/reservas/` |
| Tripulantes | `/api/tripulantes/` |
| Asignaciones | `/api/asignaciones/` |
| Incidentes | `/api/incidentes/` |

Cada recurso soporta: `GET` (listar), `POST` (crear), `GET /{id}/` (detalle), `PUT /{id}/` (editar), `PATCH /{id}/` (editar parcial), `DELETE /{id}/` (eliminar).

### Endpoints especiales

```
PATCH /api/vuelos/{id}/cambiar-estado/
GET   /api/vuelos/por-ruta/?origen=UIO&destino=GYE
```

---

## Autenticación

La API usa **JWT (JSON Web Tokens)**. Para acceder a los endpoints protegidos incluye el token en el header:

```
Authorization: Bearer <access_token>
```

### Ejemplo de login

```bash
curl -X POST https://alba-vuelos.uaeftt-ute.site/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu_password"}'
```

Respuesta:
```json
{
  "refresh": "eyJ...",
  "access": "eyJ...",
  "usuario": {
    "id": 1,
    "username": "admin",
    "email": "admin@skyops.com",
    "es_staff": true
  }
}
```

---

## Filtros

Todos los endpoints soportan filtros avanzados por query params:

### Vuelos

```
GET /api/vuelos/?estado=programado
GET /api/vuelos/?origen_codigo=UIO&destino_codigo=GYE
GET /api/vuelos/?fecha=2026-05-27
GET /api/vuelos/?fecha_desde=2026-05-27T00:00:00&fecha_hasta=2026-05-28T00:00:00
GET /api/vuelos/?duracion_max=120
GET /api/vuelos/?aerolinea_codigo=LA
```

### Reservas

```
GET /api/reservas/?estado=confirmada&clase=ejecutiva
GET /api/reservas/?numero_vuelo=LA101
GET /api/reservas/?origen_codigo=UIO
```

### Aeronaves

```
GET /api/aeronaves/?estado=activa
GET /api/aeronaves/?capacidad_min=150&capacidad_max=200
GET /api/aeronaves/?fabricante=Airbus
```

### Tripulantes

```
GET /api/tripulantes/?rol=piloto&disponible=true
GET /api/tripulantes/?aerolinea_codigo=LA
```

### Incidentes

```
GET /api/incidentes/?severidad=critica&estado_resolucion=abierto
GET /api/incidentes/?tipo=tecnico
```

Todos los endpoints también soportan:
- **Búsqueda:** `?search=texto`
- **Ordenamiento:** `?ordering=campo` o `?ordering=-campo` (descendente)
- **Paginación:** `?page=2&limite=10`

---

## Tests

```bash
pytest
```

```
86 passed in 34.49s
```

Los tests cubren:
- Autenticación JWT (login, registro, perfil, logout)
- CRUD completo de todos los recursos
- Control de permisos por rol
- Validaciones de modelos
- Filtros y búsquedas
- Endpoints especiales (cambiar estado, buscar por ruta)

---

## Roles y permisos

| Rol | Descripción | GET | POST | PUT/PATCH | DELETE |
|-----|-------------|-----|------|-----------|--------|
| **Admin** | `is_staff=True` | ✅ | ✅ | ✅ | ✅ |
| **Operador** | Grupo `Operadores` | ✅ | ✅ | ✅ | ❌ |
| **Usuario** | Autenticado | ✅ vuelos | ❌ | ❌ | ❌ |
| **Usuario** | Sus reservas | ✅ | ❌ | ✅ | ❌ |

### Usuarios de prueba

| Usuario | Password | Rol |
|---------|----------|-----|
| `mateo` | (el que creaste) | Admin |
| `operador1` | `Operador123!` | Operador |
| `usuario1` | `Usuario123!` | Usuario |

---

## Tablas de la base de datos

| Tabla | Descripción |
|-------|-------------|
| `Aerolinea` | Empresas de aviación |
| `Aeropuerto` | Aeropuertos con coordenadas |
| `Aeronave` | Aviones asignados a aerolíneas |
| `Puerta` | Gates de embarque |
| `Vuelo` | Tabla central del sistema |
| `Pasajero` | Viajeros registrados |
| `Reserva` | Relación vuelo ↔ pasajero |
| `Tripulante` | Pilotos y auxiliares |
| `AsignacionTripulacion` | Tripulantes por vuelo |
| `Incidente` | Eventos reportados en vuelos |

---

## Despliegue en Azure

La API está desplegada en una **Azure Virtual Machine** con Ubuntu 24.04 usando Gunicorn + Nginx.

### Infraestructura

| Componente | Detalle |
|------------|---------|
| **Servidor** | Azure VM — Standard B2ats v2 |
| **OS** | Ubuntu 24.04 LTS |
| **IP pública** | `68.211.88.144` |
| **Dominio** | `alba-vuelos.uaeftt-ute.site` |
| **Base de datos** | PostgreSQL 16 (local en VM) |
| **Servidor WSGI** | Gunicorn — 3 workers |
| **Reverse proxy** | Nginx 1.24 |
| **Ruta del proyecto** | `/opt/skyops/` |

### Servicios del sistema

```bash
# Ver estado de los servicios
sudo systemctl status gunicorn-skyops
sudo systemctl status nginx
sudo systemctl status postgresql

# Reiniciar Gunicorn después de cambios
sudo systemctl restart gunicorn-skyops

# Ver logs
sudo tail -f /var/log/gunicorn-skyops-access.log
sudo tail -f /var/log/nginx/skyops-access.log
sudo journalctl -u gunicorn-skyops -f
```

### Variables de entorno en producción

```env
SECRET_KEY=<clave-segura>
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,68.211.88.144,alba-vuelos.uaeftt-ute.site
DB_NAME=skyops_db
DB_USER=skyops_user
DB_PASSWORD=<password-seguro>
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOW_ALL_ORIGINS=True
```

---

## CI/CD con GitHub Actions

El proyecto tiene un pipeline completo de **CI/CD automático** con GitHub Actions.

🔗 **Repositorio:** `https://github.com/mateoalba/skyops`

### Flujo del pipeline

```
push a main
     │
     ▼
[Job 1: Tests] ── instala uv ── uv sync ── pytest (86 tests)
     │
     │ (solo si todos los tests pasan ✅)
     ▼
[Job 2: Deploy] ── SSH a VM ── git pull ── uv sync ── migrate ── collectstatic ── restart
```

### Archivo de workflow

`.github/workflows/deploy.yml`

```yaml
name: SkyOps — CI/CD Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: skyops_test_db
          POSTGRES_USER: skyops_user
          POSTGRES_PASSWORD: skyops_pass
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv python install 3.12
      - run: uv sync
      - run: uv run python manage.py test --verbosity=2

  deploy:
    name: Deploy to Azure VM
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy via SSH
        run: |
          ssh root@68.211.88.144 << 'ENDSSH'
            cd /opt/skyops
            git pull origin main
            uv sync --frozen
            uv run python manage.py migrate --noinput
            uv run python manage.py collectstatic --noinput --clear
            sudo systemctl restart gunicorn-skyops
            sudo systemctl restart nginx
          ENDSSH
```

### GitHub Secrets configurados

| Secret | Descripción |
|--------|-------------|
| `VPS_SSH_KEY` | Clave privada SSH para conectarse a la VM |
| `VPS_HOST` | IP pública del servidor (`68.211.88.144`) |
| `VPS_USERNAME` | Usuario SSH (`root`) |
| `DEPLOY_PATH` | Ruta del proyecto (`/opt/skyops`) |

### Historial de deploys

Los deploys se pueden monitorear en:
`https://github.com/mateoalba/skyops/actions`

---

## Licencia

MIT