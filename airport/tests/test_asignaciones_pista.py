import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from airport.models import AsignacionPista, PistaAterrizaje, Aeropuerto, Vuelo, Aerolinea
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@pytest.fixture
def admin_client():
    client = APIClient()
    user = User.objects.create_superuser(
        username="admin_asig_pista", password="admin123", email="admin_ap@test.com"
    )
    response = client.post("/api/auth/login/", {"username": "admin_asig_pista", "password": "admin123"})
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


@pytest.fixture
def aeropuerto():
    return Aeropuerto.objects.create(
        nombre="Aeropuerto AP Test", codigo_iata="APT",
        ciudad="Test", pais="Ecuador",
        zona_horaria="America/Guayaquil", latitud=0.0, longitud=0.0
    )


@pytest.fixture
def pista(aeropuerto):
    return PistaAterrizaje.objects.create(
        aeropuerto=aeropuerto, identificador="09L",
        longitud_metros=3000, superficie="asfalto", estado="operativa"
    )


@pytest.fixture
def vuelo(aeropuerto):
    aerolinea = Aerolinea.objects.create(
        nombre="Test Air", codigo_iata="TA", pais="Ecuador"
    )
    return Vuelo.objects.create(
        numero_vuelo="TA001", aerolinea=aerolinea,
        origen=aeropuerto, destino=aeropuerto,
        salida_programada=timezone.now() + timedelta(hours=1),
        llegada_programada=timezone.now() + timedelta(hours=3),
        estado="programado"
    )


@pytest.mark.django_db
def test_listar_asignaciones_pista(admin_client, vuelo, pista):
    AsignacionPista.objects.create(
        vuelo=vuelo, pista=pista, tipo_operacion="aterrizaje",
        hora_inicio=timezone.now(), hora_fin=timezone.now() + timedelta(minutes=30)
    )
    response = admin_client.get("/api/asignaciones-pista/")
    assert response.status_code == 200
    assert response.data["total"] >= 1


@pytest.mark.django_db
def test_crear_asignacion_pista(admin_client, vuelo, pista):
    data = {
        "vuelo": str(vuelo.id),
        "pista": str(pista.id),
        "tipo_operacion": "despegue",
        "hora_inicio": (timezone.now() + timedelta(hours=2)).isoformat(),
        "hora_fin": (timezone.now() + timedelta(hours=2, minutes=30)).isoformat()
    }
    response = admin_client.post("/api/asignaciones-pista/", data)
    assert response.status_code == 201
    assert response.data["tipo_operacion"] == "despegue"


@pytest.mark.django_db
def test_editar_asignacion_pista(admin_client, vuelo, pista):
    asignacion = AsignacionPista.objects.create(
        vuelo=vuelo, pista=pista, tipo_operacion="aterrizaje",
        hora_inicio=timezone.now(), hora_fin=timezone.now() + timedelta(minutes=30)
    )
    response = admin_client.patch(
        f"/api/asignaciones-pista/{asignacion.id}/",
        {"tipo_operacion": "prueba"}
    )
    assert response.status_code == 200
    assert response.data["tipo_operacion"] == "prueba"


@pytest.mark.django_db
def test_eliminar_asignacion_pista(admin_client, vuelo, pista):
    asignacion = AsignacionPista.objects.create(
        vuelo=vuelo, pista=pista, tipo_operacion="despegue",
        hora_inicio=timezone.now(), hora_fin=timezone.now() + timedelta(minutes=30)
    )
    response = admin_client.delete(f"/api/asignaciones-pista/{asignacion.id}/")
    assert response.status_code == 204