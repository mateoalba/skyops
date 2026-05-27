import pytest
from airport.models import Reserva


@pytest.mark.django_db
class TestReservaPermisos:

    def test_admin_ve_todas_las_reservas(self, admin_client, reserva):
        response = admin_client.get("/api/reservas/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_operador_ve_todas_las_reservas(self, operador_client, reserva):
        response = operador_client.get("/api/reservas/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_usuario_solo_ve_sus_reservas(self, usuario_client, reserva):
        # usuario_test tiene email diferente al pasajero de la reserva
        response = usuario_client.get("/api/reservas/")
        assert response.status_code == 200
        assert response.data["total"] == 0

    def test_sin_token_no_puede_ver(self, api_client, reserva):
        response = api_client.get("/api/reservas/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestReservaCrear:

    def test_admin_puede_crear_reserva(self, admin_client, vuelo, pasajero):
        data = {
            "vuelo": str(vuelo.id),
            "pasajero": str(pasajero.id),
            "numero_asiento": "15B",
            "clase": "economica",
            "estado": "confirmada",
        }
        response = admin_client.post("/api/reservas/", data, format="json")
        assert response.status_code == 201
        assert response.data["numero_asiento"] == "15B"
        assert "codigo_reserva" in response.data

    def test_operador_puede_crear_reserva(self, operador_client, vuelo, pasajero):
        data = {
            "vuelo": str(vuelo.id),
            "pasajero": str(pasajero.id),
            "numero_asiento": "16C",
            "clase": "ejecutiva",
            "estado": "pendiente",
        }
        response = operador_client.post("/api/reservas/", data, format="json")
        assert response.status_code == 201

    def test_asiento_duplicado_falla(self, admin_client, vuelo, pasajero, reserva):
        # reserva ya tiene el asiento 12A
        data = {
            "vuelo": str(vuelo.id),
            "pasajero": str(pasajero.id),
            "numero_asiento": "12A",
            "clase": "economica",
            "estado": "confirmada",
        }
        response = admin_client.post("/api/reservas/", data, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestReservaEliminar:

    def test_admin_puede_eliminar(self, admin_client, reserva):
        response = admin_client.delete(f"/api/reservas/{reserva.id}/")
        assert response.status_code == 204

    def test_operador_no_puede_eliminar(self, operador_client, reserva):
        response = operador_client.delete(f"/api/reservas/{reserva.id}/")
        assert response.status_code == 403

    def test_usuario_no_puede_eliminar(self, usuario_client, reserva):
        response = usuario_client.delete(f"/api/reservas/{reserva.id}/")
        assert response.status_code == 403


@pytest.mark.django_db
class TestReservaCodigo:

    def test_codigo_reserva_generado_automaticamente(self, admin_client, vuelo, pasajero):
        data = {
            "vuelo": str(vuelo.id),
            "pasajero": str(pasajero.id),
            "numero_asiento": "20A",
            "clase": "primera",
            "estado": "confirmada",
        }
        response = admin_client.post("/api/reservas/", data, format="json")
        assert response.status_code == 201
        assert len(response.data["codigo_reserva"]) == 6

    def test_codigos_son_unicos(self, admin_client, vuelo, pasajero):
        data1 = {"vuelo": str(vuelo.id), "pasajero": str(pasajero.id),
                 "numero_asiento": "21A", "clase": "economica", "estado": "confirmada"}
        data2 = {"vuelo": str(vuelo.id), "pasajero": str(pasajero.id),
                 "numero_asiento": "22B", "clase": "economica", "estado": "confirmada"}
        r1 = admin_client.post("/api/reservas/", data1, format="json")
        r2 = admin_client.post("/api/reservas/", data2, format="json")
        assert r1.data["codigo_reserva"] != r2.data["codigo_reserva"]