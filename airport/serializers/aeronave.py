from rest_framework import serializers
from airport.models import Aeronave


class AeronaveSerializer(serializers.ModelSerializer):
    aerolinea_nombre = serializers.CharField(
        source="aerolinea.nombre", read_only=True
    )
    aerolinea_codigo = serializers.CharField(
        source="aerolinea.codigo_iata", read_only=True
    )
    estado_display = serializers.CharField(
        source="get_estado_display", read_only=True
    )

    class Meta:
        model = Aeronave
        fields = [
            "id",
            "aerolinea",
            "aerolinea_nombre",
            "aerolinea_codigo",
            "matricula",
            "modelo",
            "fabricante",
            "capacidad",
            "estado",
            "estado_display",
        ]
        read_only_fields = ["id"]
