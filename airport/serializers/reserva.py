from rest_framework import serializers
from airport.models import Reserva


class ReservaSerializer(serializers.ModelSerializer):
    pasajero_nombre = serializers.CharField(
        source="pasajero.nombre", read_only=True
    )
    pasajero_apellido = serializers.CharField(
        source="pasajero.apellido", read_only=True
    )
    vuelo_numero = serializers.CharField(
        source="vuelo.numero_vuelo", read_only=True
    )
    vuelo_origen = serializers.CharField(
        source="vuelo.origen.codigo_iata", read_only=True
    )
    vuelo_destino = serializers.CharField(
        source="vuelo.destino.codigo_iata", read_only=True
    )
    clase_display = serializers.CharField(
        source="get_clase_display", read_only=True
    )
    estado_display = serializers.CharField(
        source="get_estado_display", read_only=True
    )

    class Meta:
        model = Reserva
        fields = [
            "id",
            "codigo_reserva",
            "vuelo",
            "vuelo_numero",
            "vuelo_origen",
            "vuelo_destino",
            "pasajero",
            "pasajero_nombre",
            "pasajero_apellido",
            "numero_asiento",
            "clase",
            "clase_display",
            "estado",
            "estado_display",
            "reservado_en",
        ]
        read_only_fields = ["id", "codigo_reserva", "reservado_en"]
