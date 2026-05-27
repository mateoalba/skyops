import pytest
from airport.models import Aerolinea, Aeropuerto, Aeronave


@pytest.mark.django_db
class TestAerolinea:

    def test_listar_aerolineas(self, admin_client, aerolinea):
        response = admin_client.get("/api/aerolineas/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_crear_aerolinea(self, admin_client):
        data = {"nombre": "Avianca", "codigo_iata": "AV", "pais": "Colombia", "activa": True}
        response = admin_client.post("/api/aerolineas/", data, format="json")
        assert response.status_code == 201
        assert response.data["nombre"] == "Avianca"

    def test_codigo_iata_duplicado_falla(self, admin_client, aerolinea):
        data = {"nombre": "Otra Aerolínea", "codigo_iata": "LA", "pais": "Ecuador"}
        response = admin_client.post("/api/aerolineas/", data, format="json")
        assert response.status_code == 400

    def test_obtener_aerolinea(self, admin_client, aerolinea):
        response = admin_client.get(f"/api/aerolineas/{aerolinea.id}/")
        assert response.status_code == 200
        assert response.data["codigo_iata"] == "LA"

    def test_actualizar_aerolinea(self, admin_client, aerolinea):
        data = {"nombre": "LATAM Ecuador", "codigo_iata": "LA",
                "pais": "Ecuador", "activa": True}
        response = admin_client.put(f"/api/aerolineas/{aerolinea.id}/", data, format="json")
        assert response.status_code == 200
        assert response.data["pais"] == "Ecuador"

    def test_eliminar_aerolinea(self, admin_client, aerolinea):
        response = admin_client.delete(f"/api/aerolineas/{aerolinea.id}/")
        assert response.status_code == 204

    def test_operador_no_puede_eliminar(self, operador_client, aerolinea):
        response = operador_client.delete(f"/api/aerolineas/{aerolinea.id}/")
        assert response.status_code == 403

    def test_buscar_por_nombre(self, admin_client, aerolinea):
        response = admin_client.get("/api/aerolineas/?search=LATAM")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_filtrar_por_activa(self, admin_client, aerolinea):
        response = admin_client.get("/api/aerolineas/?activa=true")
        assert response.status_code == 200


@pytest.mark.django_db
class TestAeropuerto:

    def test_listar_aeropuertos(self, admin_client, aeropuerto_origen):
        response = admin_client.get("/api/aeropuertos/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_crear_aeropuerto(self, admin_client):
        data = {
            "nombre": "El Dorado",
            "codigo_iata": "BOG",
            "ciudad": "Bogotá",
            "pais": "Colombia",
            "latitud": 4.7016,
            "longitud": -74.1469,
            "zona_horaria": "America/Bogota",
        }
        response = admin_client.post("/api/aeropuertos/", data, format="json")
        assert response.status_code == 201

    def test_codigo_iata_unico(self, admin_client, aeropuerto_origen):
        data = {
            "nombre": "Otro Aeropuerto",
            "codigo_iata": "UIO",
            "ciudad": "Quito",
            "pais": "Ecuador",
            "latitud": 0.0,
            "longitud": 0.0,
            "zona_horaria": "America/Guayaquil",
        }
        response = admin_client.post("/api/aeropuertos/", data, format="json")
        assert response.status_code == 400

    def test_buscar_aeropuerto(self, admin_client, aeropuerto_origen):
        response = admin_client.get("/api/aeropuertos/?search=Quito")
        assert response.status_code == 200
        assert response.data["total"] >= 1


@pytest.mark.django_db
class TestAeronave:

    def test_listar_aeronaves(self, admin_client, aeronave):
        response = admin_client.get("/api/aeronaves/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_crear_aeronave(self, admin_client, aerolinea):
        data = {
            "aerolinea": str(aerolinea.id),
            "matricula": "HC-NEW",
            "modelo": "Boeing 737",
            "fabricante": "Boeing",
            "capacidad": 162,
            "estado": "activa",
        }
        response = admin_client.post("/api/aeronaves/", data, format="json")
        assert response.status_code == 201

    def test_filtrar_por_estado(self, admin_client, aeronave):
        response = admin_client.get("/api/aeronaves/?estado=activa")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_aeronave_incluye_nombre_aerolinea(self, admin_client, aeronave):
        response = admin_client.get(f"/api/aeronaves/{aeronave.id}/")
        assert response.status_code == 200
        assert "aerolinea_nombre" in response.data
        assert response.data["aerolinea_nombre"] == "LATAM Airlines"