# ✈️ SkyOps API

Sistema de Control de Vuelos — API REST construida con Django y PostgreSQL, desplegada en Digital Ocean con CI/CD automático.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Django](https://img.shields.io/badge/Django-6.0+-green)
![DRF](https://img.shields.io/badge/DRF-3.15+-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue)
![Tests](https://img.shields.io/badge/Tests-passed-brightgreen)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black)
![Deploy](https://img.shields.io/badge/Deploy-Digital%20Ocean-0080FF)

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
- [Tablas de la base de datos](#tablas-de-la-base-de-datos)
- [Despliegue en Digital Ocean](#despliegue-en-digital-ocean)
- [CI/CD con GitHub Actions](#cicd-con-github-actions)

---

## Descripción

SkyOps es una API REST para la gestión y control operativo de un aeropuerto. Permite administrar vuelos, pasajeros, reservas, tripulación, aeronaves e incidentes con autenticación JWT y control de acceso por roles.

El proyecto fue desarrollado de manera grupal con 25 tablas distribuidas entre 3 integrantes.

🌐 **API en producción:** `https://alba-vuelos.uaeftt-ute.site/api/`
📖 **Documentación Swagger:** `https://alba-vuelos.uaeftt-ute.site/api/docs/`
❤️ **Health check:** `https://alba-vuelos.uaeftt-ute.site/api/health/`

---

## Tecnologías

- **Python 3.12**
- **Django 6.0** — framework web
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
- **Digital Ocean Droplet** — infraestructura cloud

---

## Estructura del proyecto

```
skyops/
├── .github/
│   └── workflows/
│       └── deploy.yml
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
│   │   ├── incidente.py
│   │   ├── terminal.py
│   │   ├── pista_aterrizaje.py
│   │   ├── asignacion_pista.py
│   │   ├── horario_vuelo.py
│   │   ├── escala_vuelo.py
│   │   ├── tipo_aeronave.py
│   │   ├── equipaje.py
│   │   ├── tarjeta_embarque.py
│   │   ├── categoria_pasajero.py
│   │   ├── notificacion.py
│   │   ├── perfil_usuario.py
│   │   ├── sesion_usuario.py
│   │   ├── audit_log.py
│   │   ├── mantenimiento_aeronave.py
│   │   └── certificacion_tripulante.py
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

### Recursos principales (10 tablas base)

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
| Asignaciones Tripulación | `/api/asignaciones/` |
| Incidentes | `/api/incidentes/` |

### Módulo Operaciones — Mateo Alba (5 tablas)

| Recurso | Endpoint base |
|---------|--------------|
| Terminales | `/api/terminales/` |
| Pistas de Aterrizaje | `/api/pistas/` |
| Asignaciones de Pista | `/api/asignaciones-pista/` |
| Horarios de Vuelo | `/api/horarios/` |
| Escalas de Vuelo | `/api/escalas/` |

### Módulo Pasajeros y Flota (5 tablas)

| Recurso | Endpoint base |
|---------|--------------|
| Tipos de Aeronave | `/api/tipos-aeronave/` |
| Equipajes | `/api/equipajes/` |
| Tarjetas de Embarque | `/api/tarjetas-embarque/` |
| Categorías de Pasajero | `/api/categorias-pasajero/` |
| Notificaciones | `/api/notificaciones/` |

### Módulo Usuarios y Mantenimiento (5 tablas)

| Recurso | Endpoint base |
|---------|--------------|
| Perfiles de Usuario | `/api/perfiles-usuario/` |
| Sesiones de Usuario | `/api/sesiones-usuario/` |
| Audit Log | `/api/audit-log/` |
| Mantenimiento Aeronave | `/api/mantenimientos/` |
| Certificaciones Tripulante | `/api/certificaciones/` |

Cada recurso soporta: `GET` (listar), `POST` (crear), `GET /{id}/` (detalle), `PUT /{id}/` (editar completo), `PATCH /{id}/` (editar parcial), `DELETE /{id}/` (eliminar).

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

### Vuelos

```
GET /api/vuelos/?estado=programado
GET /api/vuelos/?origen_codigo=UIO&destino_codigo=GYE
GET /api/vuelos/?fecha=2026-05-27
GET /api/vuelos/?aerolinea_codigo=LA
```

### Pistas de Aterrizaje

```
GET /api/pistas/?estado=operativa
GET /api/pistas/?superficie=asfalto
GET /api/pistas/?aeropuerto=UUID
```

### Terminales

```
GET /api/terminales/?estado=activa
GET /api/terminales/?aeropuerto=UUID
```

### Horarios de Vuelo

```
GET /api/horarios/?activo=true
GET /api/horarios/?aerolinea=UUID
GET /api/horarios/?origen=UUID&destino=UUID
```

### Escalas de Vuelo

```
GET /api/escalas/?vuelo=UUID
GET /api/escalas/?aeropuerto_escala=UUID
```

Todos los endpoints también soportan:
- **Búsqueda:** `?search=texto`
- **Ordenamiento:** `?ordering=campo` o `?ordering=-campo`
- **Paginación:** `?page=2&limite=10`

---

## Tests

```bash
uv run pytest -v
```

Los tests cubren todas las tablas implementadas:
- Autenticación JWT
- CRUD completo de los 25 recursos
- Control de permisos por rol
- Validaciones de modelos
- Filtros y búsquedas

---

## Roles y permisos

| Rol | Descripción | GET | POST | PUT/PATCH | DELETE |
|-----|-------------|-----|------|-----------|--------|
| **Admin** | `is_staff=True` | ✅ | ✅ | ✅ | ✅ |
| **Operador** | Grupo `Operadores` | ✅ | ✅ | ✅ | ❌ |
| **Usuario** | Autenticado | ✅ vuelos | ❌ | ❌ | ❌ |

### Usuarios de prueba

| Usuario | Password | Rol |
|---------|----------|-----|
| `mateo` | `dinosaurio12` | Admin |
| `operador1` | `Operador123!` | Operador |
| `usuario1` | `Usuario123!` | Usuario |

---

## Tablas de la base de datos

### Tablas base (10)

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

### Módulo Operaciones — Mateo Alba (5)

| Tabla | Descripción |
|-------|-------------|
| `Terminal` | Terminales del aeropuerto (T1, T2...) |
| `PistaAterrizaje` | Pistas con longitud y estado |
| `AsignacionPista` | Qué vuelo usa qué pista y cuándo |
| `HorarioVuelo` | Horarios recurrentes por ruta |
| `EscalaVuelo` | Aeropuerto intermedio de un vuelo |

### Módulo Pasajeros y Flota (5)

| Tabla | Descripción |
|-------|-------------|
| `TipoAeronave` | Catálogo de tipos de aeronave |
| `Equipaje` | Maletas por reserva con peso y estado |
| `TarjetaEmbarque` | Boarding pass por reserva |
| `CategoriaPasajero` | VIP, Frequent Flyer, etc. |
| `Notificacion` | Alertas al pasajero sobre su vuelo |

### Módulo Usuarios y Mantenimiento (5)

| Tabla | Descripción |
|-------|-------------|
| `PerfilUsuario` | Extensión del User de Django |
| `SesionUsuario` | Historial de logins con IP |
| `AuditLog` | Quién hizo qué sobre qué objeto |
| `MantenimientoAeronave` | Mantenimientos programados |
| `CertificacionTripulante` | Licencias y habilitaciones |

---

## Despliegue en Digital Ocean

La API está desplegada en un **Digital Ocean Droplet** con Ubuntu usando Gunicorn + Nginx.

### Infraestructura

| Componente | Detalle |
|------------|---------|
| **Servidor** | Digital Ocean Droplet |
| **OS** | Ubuntu 24.04 LTS |
| **IP pública** | `147.182.179.6` |
| **Dominio** | `alba-vuelos.uaeftt-ute.site` |
| **Base de datos** | PostgreSQL 16 (local en Droplet) |
| **Servidor WSGI** | Gunicorn |
| **Reverse proxy** | Nginx |
| **Ruta del proyecto** | `/opt/skyops/` |

### Servicios del sistema

```bash
# Ver estado
sudo systemctl status gunicorn-skyops
sudo systemctl status nginx
sudo systemctl status postgresql

# Reiniciar
sudo systemctl restart gunicorn-skyops

# Ver logs
sudo tail -f /var/log/gunicorn-skyops-access.log
sudo journalctl -u gunicorn-skyops -f
```

### Variables de entorno en producción

```env
SECRET_KEY=<clave-segura>
DEBUG=False
ALLOWED_HOSTS=147.182.179.6,alba-vuelos.uaeftt-ute.site
DB_NAME=skyops_db
DB_USER=skyops_user
DB_PASSWORD=<password-seguro>
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOW_ALL_ORIGINS=True
```

---

## CI/CD con GitHub Actions

🔗 **Repositorio:** `https://github.com/mateoalba/skyops`

### Flujo del pipeline

```
push a main
     │
     ▼
[Job 1: Tests] ── instala uv ── uv sync ── pytest
     │
     │ (solo si todos los tests pasan ✅)
     ▼
[Job 2: Deploy] ── SSH a Droplet ── git pull ── uv sync ── migrate ── restart
```

### GitHub Secrets configurados

| Secret | Descripción |
|--------|-------------|
| `VPS_SSH_KEY` | Clave privada SSH |
| `VPS_HOST` | IP del servidor (`147.182.179.6`) |
| `VPS_USERNAME` | Usuario SSH |
| `DEPLOY_PATH` | Ruta del proyecto (`/opt/skyops`) |

### Historial de deploys

`https://github.com/mateoalba/skyops/actions`

---

## Licencia

MIT