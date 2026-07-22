from rest_framework import serializers
from airport.models import Aerolinea


class AerolineaSerializer(serializers.ModelSerializer):
    total_aeronaves = serializers.SerializerMethodField()
    total_vuelos = serializers.SerializerMethodField()
    # Mismo patrón que AeropuertoSerializer.foto_resuelta: prioriza el
    # archivo subido y si no hay, cae al link manual guardado en 'logo_url'.
    logo_resuelta = serializers.SerializerMethodField()

    class Meta:
        model = Aerolinea
        fields = [
            "id",
            "nombre",
            "codigo_iata",
            "pais",
            "activa",
            "creado_en",
            "logo_url",
            "logo",
            "logo_resuelta",
            "total_aeronaves",
            "total_vuelos",
        ]
        read_only_fields = ["id", "creado_en"]
        extra_kwargs = {
            "logo": {"required": False, "allow_null": True},
        }

    def get_total_aeronaves(self, obj):
        return obj.aeronaves.count()

    def get_total_vuelos(self, obj):
        return obj.vuelos.count()

    def get_logo_resuelta(self, obj):
        if obj.logo:
            request = self.context.get("request")
            url = obj.logo.url
            return request.build_absolute_uri(url) if request else url
        return obj.logo_url or None
