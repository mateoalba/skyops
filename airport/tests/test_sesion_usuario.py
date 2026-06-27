import pytest
from airport.models import SesionUsuario


@pytest.fixture
def sesion(db, admin_user):
    return SesionUsuario.objects.create(
        usuario=admin_user,
        ip_address="127.0.0.1",
        user_agent="Mozilla/5.0",
        resultado="exitoso",
        token_jti="jti-test-abc123",
    )


@pytest.fixture
def sesion_fallida(db):
    return SesionUsuario.objects.create(
        usuario=None,
        ip_address="192.168.1.99",
        user_agent="curl/7.0",
        resultado="fallido_password",
        token_jti="",
    )


@pytest.mark.django_db
class TestSesionUsuario:

    def test_listar_sesiones(self, admin_client, sesion):
        response = admin_client.get("/api/sesiones/")
        assert response.status_code == 200

    def test_obtener_sesion(self, admin_client, sesion):
        response = admin_client.get(f"/api/sesiones/{sesion.id}/")
        assert response.status_code == 200
        assert response.data["ip_address"] == "127.0.0.1"
        assert response.data["resultado"] == "exitoso"

    def test_sesion_incluye_username(self, admin_client, sesion):
        response = admin_client.get(f"/api/sesiones/{sesion.id}/")
        assert response.status_code == 200
        assert "username" in response.data
        assert "duracion_segundos" in response.data

    def test_sesion_es_solo_lectura(self, admin_client):
        response = admin_client.post(
            "/api/sesiones/",
            {"resultado": "exitoso", "ip_address": "1.1.1.1"},
            format="json",
        )
        assert response.status_code == 405

    def test_filtrar_por_resultado_exitoso(self, admin_client, sesion):
        response = admin_client.get("/api/sesiones/?resultado=exitoso")
        assert response.status_code == 200

    def test_filtrar_por_resultado_fallido(self, admin_client, sesion_fallida):
        response = admin_client.get("/api/sesiones/?resultado=fallido_password")
        assert response.status_code == 200

    def test_buscar_por_ip(self, admin_client, sesion):
        response = admin_client.get("/api/sesiones/?search=127.0.0.1")
        assert response.status_code == 200

    def test_usuario_normal_solo_ve_sus_sesiones(self, usuario_client, sesion):
        response = usuario_client.get("/api/sesiones/")
        assert response.status_code == 200
        items = response.data.get("resultados", response.data)
        ids = [str(item["id"]) for item in items]
        assert str(sesion.id) not in ids

    def test_no_autenticado_no_puede_ver(self, api_client, sesion):
        response = api_client.get("/api/sesiones/")
        assert response.status_code == 401