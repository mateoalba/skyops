import pytest
from django.contrib.auth.models import User
from airport.models import PerfilUsuario


@pytest.fixture
def perfil(db, admin_user, aeropuerto_origen):
    return PerfilUsuario.objects.create(
        usuario=admin_user,
        aeropuerto_asignado=aeropuerto_origen,
        tipo_documento="cedula",
        numero_documento="1712345678",
        telefono="0991234567",
        cargo="operador",
        activo=True,
    )


@pytest.mark.django_db
class TestPerfilUsuario:

    def test_listar_perfiles(self, admin_client, perfil):
        response = admin_client.get("/api/perfiles/")
        assert response.status_code == 200

    def test_mi_perfil_endpoint(self, admin_client, perfil):
        response = admin_client.get("/api/perfiles/mi-perfil/")
        assert response.status_code == 200
        assert "numero_documento" in response.data

    def test_mi_perfil_sin_perfil_da_404(self, usuario_client):
        response = usuario_client.get("/api/perfiles/mi-perfil/")
        assert response.status_code == 404

    def test_crear_perfil(self, admin_client):
        nuevo_user = User.objects.create_user(
            username="nuevo_op", password="Op123456!"
        )
        data = {
            "usuario": nuevo_user.id,
            "tipo_documento": "cedula",
            "numero_documento": "0987654321",
            "telefono": "0998765432",
            "cargo": "operador",
            "activo": True,
        }
        response = admin_client.post("/api/perfiles/", data, format="json")
        assert response.status_code == 201

    def test_obtener_perfil(self, admin_client, perfil):
        response = admin_client.get(f"/api/perfiles/{perfil.id}/")
        assert response.status_code == 200
        assert response.data["numero_documento"] == "1712345678"

    def test_perfil_incluye_username(self, admin_client, perfil):
        response = admin_client.get(f"/api/perfiles/{perfil.id}/")
        assert response.status_code == 200
        assert "username" in response.data
        assert "nombre_completo" in response.data

    def test_actualizar_perfil(self, admin_client, perfil):
        data = {"telefono": "0991111111"}
        response = admin_client.patch(f"/api/perfiles/{perfil.id}/", data, format="json")
        assert response.status_code == 200

    def test_eliminar_perfil(self, admin_client, perfil):
        response = admin_client.delete(f"/api/perfiles/{perfil.id}/")
        assert response.status_code == 204

    def test_filtrar_por_activo(self, admin_client, perfil):
        response = admin_client.get("/api/perfiles/?activo=true")
        assert response.status_code == 200

    def test_buscar_por_username(self, admin_client, perfil):
        response = admin_client.get("/api/perfiles/?search=admin")
        assert response.status_code == 200

    def test_documento_duplicado_falla(self, admin_client, perfil):
        otro_user = User.objects.create_user(username="otro2", password="Otro123!")
        data = {
            "usuario": otro_user.id,
            "tipo_documento": "cedula",
            "numero_documento": "1712345678",
            "cargo": "tecnico",
            "activo": True,
        }
        response = admin_client.post("/api/perfiles/", data, format="json")
        assert response.status_code == 400

    def test_no_autenticado_no_puede_ver(self, api_client, perfil):
        response = api_client.get("/api/perfiles/")
        assert response.status_code == 401
