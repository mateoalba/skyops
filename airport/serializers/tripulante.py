from rest_framework import serializers
from airport.models import Tripulante


class TripulanteSerializer(serializers.ModelSerializer):
    aerolinea_nombre = serializers.CharField(
        source="aerolinea.nombre", read_only=True
    )
    rol_display = serializers.CharField(
        source="get_rol_display", read_only=True
    )
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Tripulante
        fields = [
            "id",
            "aerolinea",
            "aerolinea_nombre",
            "nombre",
            "apellido",
            "nombre_completo",
            "rol",
            "rol_display",
            "num_licencia",
            "disponible",
        ]
        read_only_fields = ["id"]

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
