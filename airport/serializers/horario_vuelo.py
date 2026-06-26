from rest_framework import serializers
from airport.models import HorarioVuelo


class HorarioVueloSerializer(serializers.ModelSerializer):
    aerolinea_nombre = serializers.CharField(
        source='aerolinea.nombre', read_only=True
    )
    origen_codigo = serializers.CharField(
        source='origen.codigo_iata', read_only=True
    )
    origen_ciudad = serializers.CharField(
        source='origen.ciudad', read_only=True
    )
    destino_codigo = serializers.CharField(
        source='destino.codigo_iata', read_only=True
    )
    destino_ciudad = serializers.CharField(
        source='destino.ciudad', read_only=True
    )

    class Meta:
        model = HorarioVuelo
        fields = [
            'id', 'aerolinea', 'aerolinea_nombre',
            'origen', 'origen_codigo', 'origen_ciudad',
            'destino', 'destino_codigo', 'destino_ciudad',
            'numero_vuelo_base', 'hora_salida',
            'dias_operacion', 'activo', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']