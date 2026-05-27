import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestLogin:

    def test_login_exitoso(self, api_client, admin_user):
        url = "/api/auth/login/"
        data = {"username": "admin_test", "password": "Admin123!"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert "usuario" in response.data

    def test_login_credenciales_incorrectas(self, api_client, admin_user):
        url = "/api/auth/login/"
        data = {"username": "admin_test", "password": "wrongpassword"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 401

    def test_login_usuario_no_existe(self, api_client):
        url = "/api/auth/login/"
        data = {"username": "noexiste", "password": "test123"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 401

    def test_token_contiene_datos_usuario(self, api_client, admin_user):
        url = "/api/auth/login/"
        data = {"username": "admin_test", "password": "Admin123!"}
        response = api_client.post(url, data, format="json")
        assert response.data["usuario"]["username"] == "admin_test"
        assert response.data["usuario"]["es_staff"] is True


@pytest.mark.django_db
class TestRegistro:

    def test_registro_exitoso(self, api_client):
        url = "/api/auth/registro/"
        data = {
            "username": "nuevo_user",
            "email": "nuevo@test.com",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "password": "NuevoPass123!",
            "password2": "NuevoPass123!",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert "access" in response.data
        assert User.objects.filter(username="nuevo_user").exists()

    def test_registro_passwords_no_coinciden(self, api_client):
        url = "/api/auth/registro/"
        data = {
            "username": "nuevo_user2",
            "email": "nuevo2@test.com",
            "password": "NuevoPass123!",
            "password2": "OtraPass123!",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 400

    def test_registro_username_duplicado(self, api_client, admin_user):
        url = "/api/auth/registro/"
        data = {
            "username": "admin_test",
            "email": "otro@test.com",
            "password": "OtraPass123!",
            "password2": "OtraPass123!",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestPerfil:

    def test_ver_perfil_autenticado(self, admin_client):
        response = admin_client.get("/api/auth/perfil/")
        assert response.status_code == 200
        assert response.data["username"] == "admin_test"

    def test_ver_perfil_sin_token(self, api_client):
        response = api_client.get("/api/auth/perfil/")
        assert response.status_code == 401

    def test_actualizar_perfil(self, admin_client):
        data = {"first_name": "Administrador", "last_name": "Sistema",
                "username": "admin_test", "email": "admin@test.com"}
        response = admin_client.put("/api/auth/perfil/", data, format="json")
        assert response.status_code == 200
        assert response.data["first_name"] == "Administrador"


@pytest.mark.django_db
class TestLogout:

    def test_logout_exitoso(self, api_client, admin_user):
        # Primero login
        login = api_client.post("/api/auth/login/",
            {"username": "admin_test", "password": "Admin123!"}, format="json")
        refresh_token = login.data["refresh"]
        access_token = login.data["access"]

        # Logout
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = api_client.post("/api/auth/logout/",
            {"refresh": refresh_token}, format="json")
        assert response.status_code == 200
        assert "mensaje" in response.data