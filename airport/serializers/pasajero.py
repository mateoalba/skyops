from rest_framework import serializers
from airport.models import Pasajero


class PasajeroSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    total_reservas = serializers.SerializerMethodField()

    class Meta:
        model = Pasajero
        fields = [
            "id",
            "nombre",
            "apellido",
            "nombre_completo",
            "num_pasaporte",
            "nacionalidad",
            "fecha_nacimiento",
            "email",
            "telefono",
            "total_reservas",
        ]
        read_only_fields = ["id"]

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"

    def get_total_reservas(self, obj):
        return obj.reservas.count()
