import pytest
from airport.models import Pasajero, Tripulante, Incidente


@pytest.mark.django_db
class TestPasajero:

    def test_listar_pasajeros(self, admin_client, pasajero):
        response = admin_client.get("/api/pasajeros/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_crear_pasajero(self, admin_client):
        data = {
            "nombre": "María",
            "apellido": "López",
            "num_pasaporte": "NUEVO123",
            "nacionalidad": "Colombiana",
            "fecha_nacimiento": "1995-06-15",
            "email": "maria.lopez@test.com",
            "telefono": "0999999999",
        }
        response = admin_client.post("/api/pasajeros/", data, format="json")
        assert response.status_code == 201
        assert response.data["nombre"] == "María"

    def test_pasaporte_duplicado_falla(self, admin_client, pasajero):
        data = {
            "nombre": "Otro",
            "apellido": "Pasajero",
            "num_pasaporte": "TEST123",
            "nacionalidad": "Ecuatoriano",
            "fecha_nacimiento": "1990-01-01",
            "email": "otro@test.com",
        }
        response = admin_client.post("/api/pasajeros/", data, format="json")
        assert response.status_code == 400

    def test_pasajero_incluye_nombre_completo(self, admin_client, pasajero):
        response = admin_client.get(f"/api/pasajeros/{pasajero.id}/")
        assert response.status_code == 200
        assert "nombre_completo" in response.data
        assert response.data["nombre_completo"] == "Juan Pérez"

    def test_buscar_pasajero_por_pasaporte(self, admin_client, pasajero):
        response = admin_client.get("/api/pasajeros/?search=TEST123")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_usuario_no_puede_eliminar_pasajero(self, usuario_client, pasajero):
        response = usuario_client.delete(f"/api/pasajeros/{pasajero.id}/")
        assert response.status_code == 403


@pytest.mark.django_db
class TestTripulante:

    def test_listar_tripulantes(self, admin_client, tripulante):
        response = admin_client.get("/api/tripulantes/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_crear_tripulante(self, admin_client, aerolinea):
        data = {
            "aerolinea": str(aerolinea.id),
            "nombre": "Ana",
            "apellido": "Torres",
            "rol": "copiloto",
            "num_licencia": "CO-TEST-999",
            "disponible": True,
        }
        response = admin_client.post("/api/tripulantes/", data, format="json")
        assert response.status_code == 201

    def test_licencia_duplicada_falla(self, admin_client, aerolinea, tripulante):
        data = {
            "aerolinea": str(aerolinea.id),
            "nombre": "Otro",
            "apellido": "Piloto",
            "rol": "piloto",
            "num_licencia": "PL-TEST-001",
            "disponible": True,
        }
        response = admin_client.post("/api/tripulantes/", data, format="json")
        assert response.status_code == 400

    def test_filtrar_por_disponible(self, admin_client, tripulante):
        response = admin_client.get("/api/tripulantes/?disponible=true")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_filtrar_por_rol(self, admin_client, tripulante):
        response = admin_client.get("/api/tripulantes/?rol=piloto")
        assert response.status_code == 200
        assert response.data["total"] >= 1


@pytest.mark.django_db
class TestIncidente:

    def test_crear_incidente(self, admin_client, vuelo):
        data = {
            "vuelo": str(vuelo.id),
            "tipo": "tecnico",
            "descripcion": "Falla menor en sistema hidráulico.",
            "severidad": "media",
            "estado_resolucion": "abierto",
        }
        response = admin_client.post("/api/incidentes/", data, format="json")
        assert response.status_code == 201
        assert response.data["tipo"] == "tecnico"

    def test_listar_incidentes(self, admin_client, vuelo):
        # Crear un incidente primero
        Incidente.objects.create(
            vuelo=vuelo, tipo="medico",
            descripcion="Pasajero con malestar.",
            severidad="baja", estado_resolucion="resuelto",
        )
        response = admin_client.get("/api/incidentes/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_filtrar_por_severidad(self, admin_client, vuelo):
        Incidente.objects.create(
            vuelo=vuelo, tipo="seguridad",
            descripcion="Alerta de seguridad.",
            severidad="alta", estado_resolucion="en_proceso",
        )
        response = admin_client.get("/api/incidentes/?severidad=alta")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_operador_no_puede_eliminar_incidente(self, operador_client, vuelo):
        incidente = Incidente.objects.create(
            vuelo=vuelo, tipo="otro",
            descripcion="Test.",
            severidad="baja", estado_resolucion="abierto",
        )
        response = operador_client.delete(f"/api/incidentes/{incidente.id}/")
        assert response.status_code == 403