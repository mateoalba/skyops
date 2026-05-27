import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from airport.models import (
    Aerolinea, Aeropuerto, Aeronave, Puerta,
    Vuelo, Pasajero, Reserva, Tripulante,
)


@pytest.mark.django_db
class TestModeloAerolinea:

    def test_str_representation(self, aerolinea):
        assert str(aerolinea) == "LATAM Airlines (LA)"

    def test_campos_requeridos(self):
        aerolinea = Aerolinea(nombre="Test", codigo_iata="TX", pais="Ecuador")
        assert aerolinea.nombre == "Test"
        assert aerolinea.activa is True  # valor por defecto

    def test_codigo_iata_unico(self, aerolinea):
        with pytest.raises(Exception):
            Aerolinea.objects.create(
                nombre="Duplicada", codigo_iata="LA", pais="Chile"
            )


@pytest.mark.django_db
class TestModeloVuelo:

    def test_str_representation(self, vuelo):
        assert "LA101" in str(vuelo)
        assert "UIO" in str(vuelo)
        assert "GYE" in str(vuelo)

    def test_estado_por_defecto(self, aerolinea, aeronave,
                                 aeropuerto_origen, aeropuerto_destino):
        ahora = timezone.now()
        vuelo = Vuelo.objects.create(
            aerolinea=aerolinea,
            aeronave=aeronave,
            origen=aeropuerto_origen,
            destino=aeropuerto_destino,
            numero_vuelo="LA200",
            salida_programada=ahora + timedelta(hours=1),
            llegada_programada=ahora + timedelta(hours=2),
        )
        assert vuelo.estado == "programado"

    def test_choices_estado(self, vuelo):
        estados = [e[0] for e in Vuelo.Estado.choices]
        assert "programado" in estados
        assert "embarcando" in estados
        assert "despegado" in estados
        assert "aterrizado" in estados
        assert "cancelado" in estados
        assert "retrasado" in estados


@pytest.mark.django_db
class TestModeloReserva:

    def test_str_representation(self, reserva):
        assert reserva.codigo_reserva in str(reserva)

    def test_codigo_generado_automaticamente(self, reserva):
        assert reserva.codigo_reserva is not None
        assert len(reserva.codigo_reserva) == 6

    def test_asiento_unico_por_vuelo(self, vuelo, pasajero, reserva):
        with pytest.raises(Exception):
            Reserva.objects.create(
                vuelo=vuelo,
                pasajero=pasajero,
                numero_asiento="12A",  # ya existe
                clase="economica",
                estado="confirmada",
            )

    def test_clase_por_defecto(self, vuelo, pasajero):
        reserva = Reserva.objects.create(
            vuelo=vuelo,
            pasajero=pasajero,
            numero_asiento="99Z",
            estado="confirmada",
        )
        assert reserva.clase == "economica"


@pytest.mark.django_db
class TestModeloTripulante:

    def test_str_representation(self, tripulante):
        assert "Carlos" in str(tripulante)
        assert "Piloto" in str(tripulante)

    def test_disponible_por_defecto(self, aerolinea):
        t = Tripulante.objects.create(
            aerolinea=aerolinea,
            nombre="Ana",
            apellido="Gómez",
            rol="auxiliar",
            num_licencia="AX-999",
        )
        assert t.disponible is True


@pytest.mark.django_db
class TestModeloPuerta:

    def test_str_representation(self, puerta):
        assert "A1" in str(puerta)
        assert "UIO" in str(puerta)

    def test_codigo_unico_por_aeropuerto(self, aeropuerto_origen, puerta):
        with pytest.raises(Exception):
            Puerta.objects.create(
                aeropuerto=aeropuerto_origen,
                codigo="A1",
                terminal="Terminal A",
            )