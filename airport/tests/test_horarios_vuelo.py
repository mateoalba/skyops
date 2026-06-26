import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from airport.models import HorarioVuelo, Aeropuerto, Aerolinea

User = get_user_model()


@pytest.fixture
def admin_client():
    client = APIClient()
    user = User.objects.create_superuser(
        username="admin_horario", password="admin123", email="admin_h@test.com"
    )
    response = client.post("/api/auth/login/", {"username": "admin_horario", "password": "admin123"})
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


@pytest.fixture
def aerolinea():
    return Aerolinea.objects.create(
        nombre="Horario Air", codigo_iata="HA", pais="Ecuador"
    )


@pytest.fixture
def aeropuerto_origen():
    return Aeropuerto.objects.create(
        nombre="Aeropuerto Origen", codigo_iata="ORG",
        ciudad="Quito", pais="Ecuador",
        zona_horaria="America/Guayaquil", latitud=0.0, longitud=0.0
    )


@pytest.fixture
def aeropuerto_destino():
    return Aeropuerto.objects.create(
        nombre="Aeropuerto Destino", codigo_iata="DST",
        ciudad="Guayaquil", pais="Ecuador",
        zona_horaria="America/Guayaquil", latitud=0.0, longitud=0.0
    )


@pytest.mark.django_db
def test_listar_horarios(admin_client, aerolinea, aeropuerto_origen, aeropuerto_destino):
    HorarioVuelo.objects.create(
        aerolinea=aerolinea, origen=aeropuerto_origen,
        destino=aeropuerto_destino, numero_vuelo_base="HA101",
        hora_salida="08:00:00", dias_operacion=["lunes", "miercoles"]
    )
    response = admin_client.get("/api/horarios/")
    assert response.status_code == 200
    assert response.data["total"] >= 1


@pytest.mark.django_db
def test_crear_horario(admin_client, aerolinea, aeropuerto_origen, aeropuerto_destino):
    data = {
        "aerolinea": str(aerolinea.id),
        "origen": str(aeropuerto_origen.id),
        "destino": str(aeropuerto_destino.id),
        "numero_vuelo_base": "HA202",
        "hora_salida": "10:00:00",
        "dias_operacion": ["lunes", "viernes"],
        "activo": True
    }
    response = admin_client.post("/api/horarios/", data, format="json")
    assert response.status_code == 201
    assert response.data["numero_vuelo_base"] == "HA202"


@pytest.mark.django_db
def test_editar_horario(admin_client, aerolinea, aeropuerto_origen, aeropuerto_destino):
    horario = HorarioVuelo.objects.create(
        aerolinea=aerolinea, origen=aeropuerto_origen,
        destino=aeropuerto_destino, numero_vuelo_base="HA303",
        hora_salida="12:00:00", dias_operacion=["martes"]
    )
    response = admin_client.patch(
        f"/api/horarios/{horario.id}/",
        {"activo": False}, format="json"
    )
    assert response.status_code == 200
    assert response.data["activo"] == False


@pytest.mark.django_db
def test_eliminar_horario(admin_client, aerolinea, aeropuerto_origen, aeropuerto_destino):
    horario = HorarioVuelo.objects.create(
        aerolinea=aerolinea, origen=aeropuerto_origen,
        destino=aeropuerto_destino, numero_vuelo_base="HA404",
        hora_salida="14:00:00", dias_operacion=["sabado"]
    )
    response = admin_client.delete(f"/api/horarios/{horario.id}/")
    assert response.status_code == 204