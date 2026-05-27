from rest_framework import serializers
from airport.models import AsignacionTripulacion


class AsignacionTripulacionSerializer(serializers.ModelSerializer):
    tripulante_nombre = serializers.SerializerMethodField()
    tripulante_rol = serializers.CharField(
        source="tripulante.get_rol_display", read_only=True
    )
    vuelo_numero = serializers.CharField(
        source="vuelo.numero_vuelo", read_only=True
    )

    class Meta:
        model = AsignacionTripulacion
        fields = [
            "id",
            "vuelo",
            "vuelo_numero",
            "tripulante",
            "tripulante_nombre",
            "tripulante_rol",
            "rol_asignado",
        ]
        read_only_fields = ["id"]

    def get_tripulante_nombre(self, obj):
        return f"{obj.tripulante.nombre} {obj.tripulante.apellido}"
