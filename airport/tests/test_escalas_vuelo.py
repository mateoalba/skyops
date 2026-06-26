import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from airport.models import EscalaVuelo, Aeropuerto, Aerolinea, Vuelo
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@pytest.fixture
def admin_client():
    client = APIClient()
    user = User.objects.create_superuser(
        username="admin_escala", password="admin123", email="admin_e@test.com"
    )
    response = client.post("/api/auth/login/", {"username": "admin_escala", "password": "admin123"})
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


@pytest.fixture
def aeropuerto():
    return Aeropuerto.objects.create(
        nombre="Aeropuerto Escala", codigo_iata="ESC",
        ciudad="Test", pais="Ecuador",
        zona_horaria="America/Guayaquil", latitud=0.0, longitud=0.0
    )


@pytest.fixture
def aeropuerto_escala():
    return Aeropuerto.objects.create(
        nombre="Aeropuerto Intermedio", codigo_iata="INT",
        ciudad="Intermedia", pais="Colombia",
        zona_horaria="America/Bogota", latitud=0.0, longitud=0.0
    )


@pytest.fixture
def vuelo(aeropuerto):
    aerolinea = Aerolinea.objects.create(
        nombre="Escala Air", codigo_iata="EA", pais="Ecuador"
    )
    return Vuelo.objects.create(
        numero_vuelo="EA001", aerolinea=aerolinea,
        origen=aeropuerto, destino=aeropuerto,
        salida_programada=timezone.now() + timedelta(hours=1),
        llegada_programada=timezone.now() + timedelta(hours=5),
        estado="programado"
    )


@pytest.mark.django_db
def test_listar_escalas(admin_client, vuelo, aeropuerto_escala):
    EscalaVuelo.objects.create(
        vuelo=vuelo, aeropuerto_escala=aeropuerto_escala,
        numero_secuencia=1,
        hora_llegada=timezone.now() + timedelta(hours=2),
        hora_salida=timezone.now() + timedelta(hours=3)
    )
    response = admin_client.get("/api/escalas/")
    assert response.status_code == 200
    assert response.data["total"] >= 1


@pytest.mark.django_db
def test_crear_escala(admin_client, vuelo, aeropuerto_escala):
    data = {
        "vuelo": str(vuelo.id),
        "aeropuerto_escala": str(aeropuerto_escala.id),
        "numero_secuencia": 1,
        "hora_llegada": (timezone.now() + timedelta(hours=2)).isoformat(),
        "hora_salida": (timezone.now() + timedelta(hours=3)).isoformat()
    }
    response = admin_client.post("/api/escalas/", data)
    assert response.status_code == 201
    assert response.data["numero_secuencia"] == 1


@pytest.mark.django_db
def test_editar_escala(admin_client, vuelo, aeropuerto_escala):
    escala = EscalaVuelo.objects.create(
        vuelo=vuelo, aeropuerto_escala=aeropuerto_escala,
        numero_secuencia=2,
        hora_llegada=timezone.now() + timedelta(hours=2),
        hora_salida=timezone.now() + timedelta(hours=3)
    )
    nueva_hora = (timezone.now() + timedelta(hours=4)).isoformat()
    response = admin_client.patch(
        f"/api/escalas/{escala.id}/",
        {"hora_salida": nueva_hora}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_eliminar_escala(admin_client, vuelo, aeropuerto_escala):
    escala = EscalaVuelo.objects.create(
        vuelo=vuelo, aeropuerto_escala=aeropuerto_escala,
        numero_secuencia=3,
        hora_llegada=timezone.now() + timedelta(hours=2),
        hora_salida=timezone.now() + timedelta(hours=3)
    )
    response = admin_client.delete(f"/api/escalas/{escala.id}/")
    assert response.status_code == 204