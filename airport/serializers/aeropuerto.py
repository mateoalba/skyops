from rest_framework import serializers
from airport.models import Aeropuerto


class AeropuertoSerializer(serializers.ModelSerializer):
    total_puertas = serializers.SerializerMethodField()

    class Meta:
        model = Aeropuerto
        fields = [
            "id",
            "nombre",
            "codigo_iata",
            "ciudad",
            "pais",
            "latitud",
            "longitud",
            "zona_horaria",
            "foto_url",
            "total_puertas",
        ]
        read_only_fields = ["id"]

    def get_total_puertas(self, obj):
        return obj.puertas.count()
