import pytest
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from airport.models import (
    Aerolinea, Aeropuerto, Aeronave, Puerta,
    Vuelo, Pasajero, Reserva, Tripulante,
    AsignacionTripulacion, Incidente,
)
from django.utils import timezone
from datetime import timedelta


# ------------------------------------------------------------------
# Clientes autenticados
# ------------------------------------------------------------------
@pytest.fixture
def api_client():
    return APIClient()


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin_test",
        email="admin@test.com",
        password="Admin123!",
    )


@pytest.fixture
def operador_user(db):
    grupo, _ = Group.objects.get_or_create(name="Operadores")
    user = User.objects.create_user(
        username="operador_test",
        email="operador@test.com",
        password="Operador123!",
    )
    user.groups.add(grupo)
    return user


@pytest.fixture
def usuario_user(db):
    return User.objects.create_user(
        username="usuario_test",
        email="usuario@test.com",
        password="Usuario123!",
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(admin_user)}")
    return api_client


@pytest.fixture
def operador_client(api_client, operador_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(operador_user)}")
    return api_client


@pytest.fixture
def usuario_client(api_client, usuario_user):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(usuario_user)}")
    return api_client


# ------------------------------------------------------------------
# Fixtures de modelos
# ------------------------------------------------------------------
@pytest.fixture
def aerolinea(db):
    return Aerolinea.objects.create(
        nombre="LATAM Airlines",
        codigo_iata="LA",
        pais="Chile",
        activa=True,
    )


@pytest.fixture
def aeropuerto_origen(db):
    return Aeropuerto.objects.create(
        nombre="Aeropuerto Mariscal Sucre",
        codigo_iata="UIO",
        ciudad="Quito",
        pais="Ecuador",
        latitud=-0.1292,
        longitud=-78.3575,
        zona_horaria="America/Guayaquil",
    )


@pytest.fixture
def aeropuerto_destino(db):
    return Aeropuerto.objects.create(
        nombre="Aeropuerto José J. de Olmedo",
        codigo_iata="GYE",
        ciudad="Guayaquil",
        pais="Ecuador",
        latitud=-2.1574,
        longitud=-79.8836,
        zona_horaria="America/Guayaquil",
    )


@pytest.fixture
def aeronave(db, aerolinea):
    return Aeronave.objects.create(
        aerolinea=aerolinea,
        matricula="HC-TEST",
        modelo="Airbus A320",
        fabricante="Airbus",
        capacidad=180,
        estado="activa",
    )


@pytest.fixture
def puerta(db, aeropuerto_origen):
    return Puerta.objects.create(
        aeropuerto=aeropuerto_origen,
        codigo="A1",
        terminal="Terminal A",
        estado="disponible",
    )


@pytest.fixture
def vuelo(db, aerolinea, aeronave, aeropuerto_origen, aeropuerto_destino, puerta):
    ahora = timezone.now()
    return Vuelo.objects.create(
        aerolinea=aerolinea,
        aeronave=aeronave,
        origen=aeropuerto_origen,
        destino=aeropuerto_destino,
        puerta=puerta,
        numero_vuelo="LA101",
        salida_programada=ahora + timedelta(hours=2),
        llegada_programada=ahora + timedelta(hours=3),
        estado="programado",
        duracion_min=60,
    )


@pytest.fixture
def pasajero(db):
    return Pasajero.objects.create(
        nombre="Juan",
        apellido="Pérez",
        num_pasaporte="TEST123",
        nacionalidad="Ecuatoriano",
        fecha_nacimiento="1990-01-01",
        email="juan.perez@test.com",
        telefono="0991234567",
    )


@pytest.fixture
def reserva(db, vuelo, pasajero):
    return Reserva.objects.create(
        vuelo=vuelo,
        pasajero=pasajero,
        numero_asiento="12A",
        clase="economica",
        estado="confirmada",
    )


@pytest.fixture
def tripulante(db, aerolinea):
    return Tripulante.objects.create(
        aerolinea=aerolinea,
        nombre="Carlos",
        apellido="Mendoza",
        rol="piloto",
        num_licencia="PL-TEST-001",
        disponible=True,
    )