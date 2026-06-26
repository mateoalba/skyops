import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from airport.models import PistaAterrizaje, Aeropuerto

User = get_user_model()


@pytest.fixture
def admin_client():
    client = APIClient()
    user = User.objects.create_superuser(
        username="admin_pista", password="admin123", email="admin_p@test.com"
    )
    response = client.post("/api/auth/login/", {"username": "admin_pista", "password": "admin123"})
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


@pytest.fixture
def aeropuerto():
    return Aeropuerto.objects.create(
        nombre="Aeropuerto Pista Test",
        codigo_iata="PST",
        ciudad="Ciudad Test",
        pais="Ecuador",
        zona_horaria="America/Guayaquil",
        latitud=0.0,
        longitud=0.0
    )


@pytest.mark.django_db
def test_listar_pistas(admin_client, aeropuerto):
    PistaAterrizaje.objects.create(
        aeropuerto=aeropuerto, identificador="09L",
        longitud_metros=3000, superficie="asfalto", estado="operativa"
    )
    response = admin_client.get("/api/pistas/")
    assert response.status_code == 200
    assert response.data["total"] >= 1


@pytest.mark.django_db
def test_crear_pista(admin_client, aeropuerto):
    data = {
        "aeropuerto": str(aeropuerto.id),
        "identificador": "27R",
        "longitud_metros": 2500,
        "superficie": "concreto",
        "estado": "operativa"
    }
    response = admin_client.post("/api/pistas/", data)
    assert response.status_code == 201
    assert response.data["identificador"] == "27R"


@pytest.mark.django_db
def test_editar_pista(admin_client, aeropuerto):
    pista = PistaAterrizaje.objects.create(
        aeropuerto=aeropuerto, identificador="18L",
        longitud_metros=2800, superficie="asfalto", estado="operativa"
    )
    response = admin_client.patch(
        f"/api/pistas/{pista.id}/",
        {"estado": "mantenimiento"}
    )
    assert response.status_code == 200
    assert response.data["estado"] == "mantenimiento"


@pytest.mark.django_db
def test_eliminar_pista(admin_client, aeropuerto):
    pista = PistaAterrizaje.objects.create(
        aeropuerto=aeropuerto, identificador="36R",
        longitud_metros=3200, superficie="concreto", estado="operativa"
    )
    response = admin_client.delete(f"/api/pistas/{pista.id}/")
    assert response.status_code == 204