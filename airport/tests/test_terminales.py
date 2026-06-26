import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from airport.models import Terminal, Aeropuerto

User = get_user_model()


@pytest.fixture
def admin_client():
    client = APIClient()
    user = User.objects.create_superuser(
        username="admin_terminal", password="admin123", email="admin_t@test.com"
    )
    response = client.post("/api/auth/login/", {"username": "admin_terminal", "password": "admin123"})
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


@pytest.fixture
def aeropuerto():
    return Aeropuerto.objects.create(
        nombre="Aeropuerto Test",
        codigo_iata="TST",
        ciudad="Ciudad Test",
        pais="Ecuador",
        zona_horaria="America/Guayaquil",
        latitud=0.0,
        longitud=0.0
    )


@pytest.mark.django_db
def test_listar_terminales(admin_client, aeropuerto):
    Terminal.objects.create(
        aeropuerto=aeropuerto, nombre="Terminal Norte",
        codigo="T1", capacidad_puertas=10, estado="activa"
    )
    response = admin_client.get("/api/terminales/")
    assert response.status_code == 200
    assert response.data["total"] >= 1


@pytest.mark.django_db
def test_crear_terminal(admin_client, aeropuerto):
    data = {
        "aeropuerto": str(aeropuerto.id),
        "nombre": "Terminal Sur",
        "codigo": "T2",
        "capacidad_puertas": 5,
        "estado": "activa"
    }
    response = admin_client.post("/api/terminales/", data)
    assert response.status_code == 201
    assert response.data["codigo"] == "T2"


@pytest.mark.django_db
def test_editar_terminal(admin_client, aeropuerto):
    terminal = Terminal.objects.create(
        aeropuerto=aeropuerto, nombre="Terminal Este",
        codigo="T3", capacidad_puertas=8, estado="activa"
    )
    response = admin_client.patch(
        f"/api/terminales/{terminal.id}/",
        {"estado": "mantenimiento"}
    )
    assert response.status_code == 200
    assert response.data["estado"] == "mantenimiento"


@pytest.mark.django_db
def test_eliminar_terminal(admin_client, aeropuerto):
    terminal = Terminal.objects.create(
        aeropuerto=aeropuerto, nombre="Terminal Oeste",
        codigo="T4", capacidad_puertas=6, estado="activa"
    )
    response = admin_client.delete(f"/api/terminales/{terminal.id}/")
    assert response.status_code == 204