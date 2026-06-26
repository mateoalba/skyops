from rest_framework import serializers
from airport.models import PistaAterrizaje


class PistaAterrizajeSerializer(serializers.ModelSerializer):
    aeropuerto_nombre = serializers.CharField(
        source='aeropuerto.nombre', read_only=True
    )
    aeropuerto_codigo = serializers.CharField(
        source='aeropuerto.codigo_iata', read_only=True
    )
    superficie_display = serializers.CharField(
        source='get_superficie_display', read_only=True
    )
    estado_display = serializers.CharField(
        source='get_estado_display', read_only=True
    )

    class Meta:
        model = PistaAterrizaje
        fields = [
            'id', 'aeropuerto', 'aeropuerto_nombre', 'aeropuerto_codigo',
            'identificador', 'longitud_metros', 'superficie', 'superficie_display',
            'estado', 'estado_display', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']