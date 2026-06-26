from rest_framework import serializers
from airport.models import EscalaVuelo


class EscalaVueloSerializer(serializers.ModelSerializer):
    vuelo_numero = serializers.CharField(
        source='vuelo.numero_vuelo', read_only=True
    )
    aeropuerto_nombre = serializers.CharField(
        source='aeropuerto_escala.nombre', read_only=True
    )
    aeropuerto_codigo = serializers.CharField(
        source='aeropuerto_escala.codigo_iata', read_only=True
    )
    aeropuerto_ciudad = serializers.CharField(
        source='aeropuerto_escala.ciudad', read_only=True
    )

    class Meta:
        model = EscalaVuelo
        fields = [
            'id', 'vuelo', 'vuelo_numero',
            'aeropuerto_escala', 'aeropuerto_nombre',
            'aeropuerto_codigo', 'aeropuerto_ciudad',
            'numero_secuencia', 'hora_llegada',
            'hora_salida', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']