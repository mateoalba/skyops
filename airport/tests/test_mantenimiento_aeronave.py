import pytest
from django.utils import timezone
from datetime import timedelta
from airport.models import MantenimientoAeronave


@pytest.fixture
def mantenimiento(db, aeronave):
    ahora = timezone.now()
    return MantenimientoAeronave.objects.create(
        aeronave=aeronave,
        tipo="preventivo",
        estado="programado",
        descripcion="Revision rutinaria de motores",
        fecha_inicio=ahora + timedelta(days=1),
        fecha_fin_estimada=ahora + timedelta(days=3),
        tecnico_responsable="Ing. Garcia",
        costo_estimado=8500.00,
    )


@pytest.mark.django_db
class TestMantenimientoAeronave:

    def test_listar_mantenimientos(self, admin_client, mantenimiento):
        response = admin_client.get("/api/mantenimientos/")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_crear_mantenimiento(self, admin_client, aeronave):
        ahora = timezone.now()
        data = {
            "aeronave": aeronave.id,
            "tipo": "correctivo",
            "estado": "programado",
            "descripcion": "Reparacion de tren de aterrizaje",
            "fecha_inicio": (ahora + timedelta(days=2)).isoformat(),
            "fecha_fin_estimada": (ahora + timedelta(days=5)).isoformat(),
            "tecnico_responsable": "Ing. Lopez",
        }
        response = admin_client.post("/api/mantenimientos/", data, format="json")
        assert response.status_code == 201
        assert response.data["tipo"] == "correctivo"

    def test_obtener_mantenimiento(self, admin_client, mantenimiento):
        response = admin_client.get(f"/api/mantenimientos/{mantenimiento.id}/")
        assert response.status_code == 200
        assert "aeronave_matricula" in response.data
        assert "aeronave_modelo" in response.data
        assert "duracion_real_horas" in response.data

    def test_actualizar_mantenimiento(self, admin_client, mantenimiento):
        data = {"estado": "en_progreso", "observaciones": "Iniciado cambio de filtros"}
        response = admin_client.patch(
            f"/api/mantenimientos/{mantenimiento.id}/", data, format="json"
        )
        assert response.status_code == 200
        assert response.data["estado"] == "en_progreso"

    def test_completar_mantenimiento(self, admin_client, mantenimiento):
        response = admin_client.post(
            f"/api/mantenimientos/{mantenimiento.id}/completar/",
            {"costo_real": "9200.00"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["estado"] == "completado"

    def test_completar_sin_costo_real_da_400(self, admin_client, mantenimiento):
        response = admin_client.post(
            f"/api/mantenimientos/{mantenimiento.id}/completar/",
            {},
            format="json",
        )
        assert response.status_code == 400

    def test_completar_ya_completado_da_400(self, admin_client, mantenimiento):
        mantenimiento.estado = "completado"
        mantenimiento.save()
        response = admin_client.post(
            f"/api/mantenimientos/{mantenimiento.id}/completar/",
            {"costo_real": "9200.00"},
            format="json",
        )
        assert response.status_code == 400

    def test_eliminar_mantenimiento(self, admin_client, mantenimiento):
        response = admin_client.delete(f"/api/mantenimientos/{mantenimiento.id}/")
        assert response.status_code == 204

    def test_fecha_fin_anterior_a_inicio_da_400(self, admin_client, aeronave):
        ahora = timezone.now()
        data = {
            "aeronave": aeronave.id,
            "tipo": "preventivo",
            "estado": "programado",
            "descripcion": "Test validacion",
            "fecha_inicio": (ahora + timedelta(days=5)).isoformat(),
            "fecha_fin_estimada": (ahora + timedelta(days=2)).isoformat(),
            "tecnico_responsable": "Test",
        }
        response = admin_client.post("/api/mantenimientos/", data, format="json")
        assert response.status_code == 400

    def test_operador_puede_ver(self, operador_client, mantenimiento):
        response = operador_client.get("/api/mantenimientos/")
        assert response.status_code == 200

    def test_operador_no_puede_crear(self, operador_client, aeronave):
        ahora = timezone.now()
        data = {
            "aeronave": aeronave.id,
            "tipo": "preventivo",
            "estado": "programado",
            "descripcion": "Test",
            "fecha_inicio": (ahora + timedelta(days=1)).isoformat(),
            "fecha_fin_estimada": (ahora + timedelta(days=3)).isoformat(),
            "tecnico_responsable": "Test",
        }
        response = operador_client.post("/api/mantenimientos/", data, format="json")
        assert response.status_code == 403

    def test_operador_no_puede_eliminar(self, operador_client, mantenimiento):
        response = operador_client.delete(f"/api/mantenimientos/{mantenimiento.id}/")
        assert response.status_code == 403

    def test_filtrar_por_tipo(self, admin_client, mantenimiento):
        response = admin_client.get("/api/mantenimientos/?tipo=preventivo")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_filtrar_por_estado(self, admin_client, mantenimiento):
        response = admin_client.get("/api/mantenimientos/?estado=programado")
        assert response.status_code == 200
        assert response.data["total"] >= 1

    def test_buscar_por_tecnico(self, admin_client, mantenimiento):
        response = admin_client.get("/api/mantenimientos/?search=Garcia")
        assert response.status_code == 200