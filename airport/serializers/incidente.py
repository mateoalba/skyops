from rest_framework import serializers
from airport.models import Incidente


class IncidenteSerializer(serializers.ModelSerializer):
    vuelo_numero = serializers.CharField(
        source="vuelo.numero_vuelo", read_only=True
    )
    tipo_display = serializers.CharField(
        source="get_tipo_display", read_only=True
    )
    severidad_display = serializers.CharField(
        source="get_severidad_display", read_only=True
    )
    estado_resolucion_display = serializers.CharField(
        source="get_estado_resolucion_display", read_only=True
    )

    class Meta:
        model = Incidente
        fields = [
            "id",
            "vuelo",
            "vuelo_numero",
            "tipo",
            "tipo_display",
            "descripcion",
            "severidad",
            "severidad_display",
            "reportado_en",
            "estado_resolucion",
            "estado_resolucion_display",
        ]
        read_only_fields = ["id", "reportado_en"]
