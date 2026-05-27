import pytest
from django.utils import timezone
from datetime import timedelta
from airport.models import Vuelo


@pytest.mark.django_db
class TestVueloListar:

    def test_admin_puede_listar(self, admin_client, vuelo):
        response = admin_client.get("/api/vuelos/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_operador_puede_listar(self, operador_client, vuelo):
        response = operador_client.get("/api/vuelos/")
        assert response.status_code == 200

    def test_usuario_puede_listar(self, usuario_client, vuelo):
        response = usuario_client.get("/api/vuelos/")
        assert response.status_code == 200

    def test_sin_token_no_puede_listar(self, api_client, vuelo):
        response = api_client.get("/api/vuelos/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestVueloCrear:

    def test_admin_puede_crear(self, admin_client, aerolinea, aeronave,
                                aeropuerto_origen, aeropuerto_destino, puerta):
        ahora = timezone.now()
        data = {
            "numero_vuelo": "LA999",
            "aerolinea": str(aerolinea.id),
            "aeronave": str(aeronave.id),
            "origen": str(aeropuerto_origen.id),
            "destino": str(aeropuerto_destino.id),
            "puerta": str(puerta.id),
            "salida_programada": (ahora + timedelta(hours=5)).isoformat(),
            "llegada_programada": (ahora + timedelta(hours=6)).isoformat(),
            "estado": "programado",
        }
        response = admin_client.post("/api/vuelos/", data, format="json")
        assert response.status_code == 201
        assert response.data["numero_vuelo"] == "LA999"

    def test_operador_puede_crear(self, operador_client, aerolinea, aeronave,
                                   aeropuerto_origen, aeropuerto_destino, puerta):
        ahora = timezone.now()
        data = {
            "numero_vuelo": "LA888",
            "aerolinea": str(aerolinea.id),
            "aeronave": str(aeronave.id),
            "origen": str(aeropuerto_origen.id),
            "destino": str(aeropuerto_destino.id),
            "puerta": str(puerta.id),
            "salida_programada": (ahora + timedelta(hours=5)).isoformat(),
            "llegada_programada": (ahora + timedelta(hours=6)).isoformat(),
            "estado": "programado",
        }
        response = operador_client.post("/api/vuelos/", data, format="json")
        assert response.status_code == 201

    def test_usuario_no_puede_crear(self, usuario_client, aerolinea, aeronave,
                                     aeropuerto_origen, aeropuerto_destino, puerta):
        ahora = timezone.now()
        data = {
            "numero_vuelo": "LA777",
            "aerolinea": str(aerolinea.id),
            "aeronave": str(aeronave.id),
            "origen": str(aeropuerto_origen.id),
            "destino": str(aeropuerto_destino.id),
            "puerta": str(puerta.id),
            "salida_programada": (ahora + timedelta(hours=5)).isoformat(),
            "llegada_programada": (ahora + timedelta(hours=6)).isoformat(),
        }
        response = usuario_client.post("/api/vuelos/", data, format="json")
        assert response.status_code == 403

    def test_origen_igual_destino_falla(self, admin_client, aerolinea, aeronave,
                                         aeropuerto_origen, puerta):
        ahora = timezone.now()
        data = {
            "numero_vuelo": "LA666",
            "aerolinea": str(aerolinea.id),
            "aeronave": str(aeronave.id),
            "origen": str(aeropuerto_origen.id),
            "destino": str(aeropuerto_origen.id),
            "puerta": str(puerta.id),
            "salida_programada": (ahora + timedelta(hours=5)).isoformat(),
            "llegada_programada": (ahora + timedelta(hours=6)).isoformat(),
        }
        response = admin_client.post("/api/vuelos/", data, format="json")
        assert response.status_code == 400

    def test_llegada_antes_salida_falla(self, admin_client, aerolinea, aeronave,
                                         aeropuerto_origen, aeropuerto_destino, puerta):
        ahora = timezone.now()
        data = {
            "numero_vuelo": "LA555",
            "aerolinea": str(aerolinea.id),
            "aeronave": str(aeronave.id),
            "origen": str(aeropuerto_origen.id),
            "destino": str(aeropuerto_destino.id),
            "puerta": str(puerta.id),
            "salida_programada": (ahora + timedelta(hours=5)).isoformat(),
            "llegada_programada": (ahora + timedelta(hours=3)).isoformat(),
        }
        response = admin_client.post("/api/vuelos/", data, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestVueloCambiarEstado:

    def test_admin_puede_cambiar_estado(self, admin_client, vuelo):
        url = f"/api/vuelos/{vuelo.id}/cambiar-estado/"
        response = admin_client.patch(url, {"estado": "embarcando"}, format="json")
        assert response.status_code == 200
        assert response.data["estado"] == "embarcando"

    def test_estado_invalido_falla(self, admin_client, vuelo):
        url = f"/api/vuelos/{vuelo.id}/cambiar-estado/"
        response = admin_client.patch(url, {"estado": "volando"}, format="json")
        assert response.status_code == 400

    def test_usuario_no_puede_cambiar_estado(self, usuario_client, vuelo):
        url = f"/api/vuelos/{vuelo.id}/cambiar-estado/"
        response = usuario_client.patch(url, {"estado": "embarcando"}, format="json")
        assert response.status_code == 403


@pytest.mark.django_db
class TestVueloPorRuta:

    def test_buscar_por_ruta(self, usuario_client, vuelo):
        response = usuario_client.get("/api/vuelos/por-ruta/?origen=UIO&destino=GYE")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_ruta_sin_parametros_falla(self, usuario_client):
        response = usuario_client.get("/api/vuelos/por-ruta/")
        assert response.status_code == 400

    def test_ruta_sin_resultados(self, usuario_client, vuelo):
        response = usuario_client.get("/api/vuelos/por-ruta/?origen=UIO&destino=BOG")
        assert response.status_code == 200
        assert len(response.data) == 0


@pytest.mark.django_db
class TestVueloEliminar:

    def test_admin_puede_eliminar(self, admin_client, vuelo):
        url = f"/api/vuelos/{vuelo.id}/"
        response = admin_client.delete(url)
        assert response.status_code == 204

    def test_operador_no_puede_eliminar(self, operador_client, vuelo):
        url = f"/api/vuelos/{vuelo.id}/"
        response = operador_client.delete(url)
        assert response.status_code == 403