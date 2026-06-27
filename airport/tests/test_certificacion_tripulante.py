import pytest
import datetime
from datetime import timedelta
from airport.models import CertificacionTripulante


@pytest.fixture
def certificacion(db, tripulante):
    hoy = datetime.date.today()
    return CertificacionTripulante.objects.create(
        tripulante=tripulante,
        tipo="licencia_piloto",
        numero_certificado="DGAC-PL-TEST-001",
        entidad_emisora="DGAC Ecuador",
        fecha_emision=hoy - timedelta(days=365),
        fecha_vencimiento=hoy + timedelta(days=365),
        estado="vigente",
    )


@pytest.fixture
def certificacion_por_vencer(db, tripulante):
    hoy = datetime.date.today()
    return CertificacionTripulante.objects.create(
        tripulante=tripulante,
        tipo="cert_medico",
        numero_certificado="MED-PV-001",
        entidad_emisora="DGAC Ecuador",
        fecha_emision=hoy - timedelta(days=355),
        fecha_vencimiento=hoy + timedelta(days=10),
        estado="por_vencer",
    )


@pytest.mark.django_db
class TestCertificacionTripulante:

    def test_listar_certificaciones(self, admin_client, certificacion):
        response = admin_client.get("/api/certificaciones/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_crear_certificacion(self, admin_client, tripulante):
        hoy = datetime.date.today()
        data = {
            "tripulante": tripulante.id,
            "tipo": "cert_medico",
            "numero_certificado": "MED-2024-NEW",
            "entidad_emisora": "DGAC Ecuador",
            "fecha_emision": (hoy - timedelta(days=180)).isoformat(),
            "fecha_vencimiento": (hoy + timedelta(days=180)).isoformat(),
            "estado": "vigente",
        }
        response = admin_client.post("/api/certificaciones/", data, format="json")
        assert response.status_code == 201
        assert response.data["tipo"] == "cert_medico"

    def test_obtener_certificacion(self, admin_client, certificacion):
        response = admin_client.get(f"/api/certificaciones/{certificacion.id}/")
        assert response.status_code == 200
        assert "dias_para_vencer" in response.data
        assert "tripulante_nombre" in response.data
        assert response.data["dias_para_vencer"] > 0

    def test_actualizar_estado(self, admin_client, certificacion):
        data = {"estado": "por_vencer"}
        response = admin_client.patch(
            f"/api/certificaciones/{certificacion.id}/", data, format="json"
        )
        assert response.status_code == 200

    def test_eliminar_certificacion(self, admin_client, certificacion):
        response = admin_client.delete(f"/api/certificaciones/{certificacion.id}/")
        assert response.status_code == 204

    def test_endpoint_por_vencer(self, admin_client, certificacion_por_vencer):
        response = admin_client.get("/api/certificaciones/por-vencer/")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_endpoint_por_vencer_no_incluye_vigentes_lejanas(self, admin_client, certificacion):
        response = admin_client.get("/api/certificaciones/por-vencer/")
        assert response.status_code == 200
        ids = [str(item["id"]) for item in response.data]
        assert str(certificacion.id) not in ids

    def test_fecha_vencimiento_anterior_da_400(self, admin_client, tripulante):
        hoy = datetime.date.today()
        data = {
            "tripulante": tripulante.id,
            "tipo": "cert_medico",
            "numero_certificado": "INVALID-001",
            "entidad_emisora": "DGAC",
            "fecha_emision": (hoy - timedelta(days=10)).isoformat(),
            "fecha_vencimiento": (hoy - timedelta(days=100)).isoformat(),
            "estado": "vigente",
        }
        response = admin_client.post("/api/certificaciones/", data, format="json")
        assert response.status_code == 400

    def test_habilitacion_tipo_sin_aeronave_da_400(self, admin_client, tripulante):
        hoy = datetime.date.today()
        data = {
            "tripulante": tripulante.id,
            "tipo": "habilitacion_tipo",
            "numero_certificado": "HAB-INVALID-001",
            "entidad_emisora": "DGAC",
            "fecha_emision": (hoy - timedelta(days=30)).isoformat(),
            "fecha_vencimiento": (hoy + timedelta(days=365)).isoformat(),
            "estado": "vigente",
            "tipo_aeronave_habilitado": "",
        }
        response = admin_client.post("/api/certificaciones/", data, format="json")
        assert response.status_code == 400

    def test_numero_certificado_duplicado_da_400(self, admin_client, tripulante, certificacion):
        hoy = datetime.date.today()
        data = {
            "tripulante": tripulante.id,
            "tipo": "cert_medico",
            "numero_certificado": "DGAC-PL-TEST-001",
            "entidad_emisora": "DGAC",
            "fecha_emision": (hoy - timedelta(days=30)).isoformat(),
            "fecha_vencimiento": (hoy + timedelta(days=365)).isoformat(),
            "estado": "vigente",
        }
        response = admin_client.post("/api/certificaciones/", data, format="json")
        assert response.status_code == 400

    def test_operador_puede_ver(self, operador_client, certificacion):
        response = operador_client.get("/api/certificaciones/")
        assert response.status_code == 200

    def test_operador_no_puede_crear(self, operador_client, tripulante):
        hoy = datetime.date.today()
        data = {
            "tripulante": tripulante.id,
            "tipo": "cert_medico",
            "numero_certificado": "TEST-OP-001",
            "entidad_emisora": "DGAC",
            "fecha_emision": (hoy - timedelta(days=30)).isoformat(),
            "fecha_vencimiento": (hoy + timedelta(days=365)).isoformat(),
            "estado": "vigente",
        }
        response = operador_client.post("/api/certificaciones/", data, format="json")
        assert response.status_code == 403

    def test_operador_no_puede_eliminar(self, operador_client, certificacion):
        response = operador_client.delete(f"/api/certificaciones/{certificacion.id}/")
        assert response.status_code == 403

    def test_filtrar_por_tipo(self, admin_client, certificacion):
        response = admin_client.get("/api/certificaciones/?tipo=licencia_piloto")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_filtrar_por_estado(self, admin_client, certificacion):
        response = admin_client.get("/api/certificaciones/?estado=vigente")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_buscar_por_entidad(self, admin_client, certificacion):
        response = admin_client.get("/api/certificaciones/?search=DGAC")
        assert response.status_code == 200