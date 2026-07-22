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
    # Mismo patrón que AeropuertoSerializer.foto_resuelta / Aerolinea
    # logo_resuelta: prioriza el archivo subido y si no hay, cae al link
    # manual guardado en 'foto_url'.
    foto_resuelta = serializers.SerializerMethodField()

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
            "foto_url",
            "foto",
            "foto_resuelta",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "foto": {"required": False, "allow_null": True},
        }

    def get_foto_resuelta(self, obj):
        if obj.foto:
            request = self.context.get("request")
            url = obj.foto.url
            return request.build_absolute_uri(url) if request else url
        return obj.foto_url or None
