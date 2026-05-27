from rest_framework import serializers
from airport.models import Aerolinea


class AerolineaSerializer(serializers.ModelSerializer):
    total_aeronaves = serializers.SerializerMethodField()
    total_vuelos = serializers.SerializerMethodField()

    class Meta:
        model = Aerolinea
        fields = [
            "id",
            "nombre",
            "codigo_iata",
            "pais",
            "activa",
            "creado_en",
            "total_aeronaves",
            "total_vuelos",
        ]
        read_only_fields = ["id", "creado_en"]

    def get_total_aeronaves(self, obj):
        return obj.aeronaves.count()

    def get_total_vuelos(self, obj):
        return obj.vuelos.count()
