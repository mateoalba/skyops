from rest_framework import serializers
from airport.models import Terminal


class TerminalSerializer(serializers.ModelSerializer):
    aeropuerto_nombre = serializers.CharField(
        source='aeropuerto.nombre', read_only=True
    )
    aeropuerto_codigo = serializers.CharField(
        source='aeropuerto.codigo_iata', read_only=True
    )
    estado_display = serializers.CharField(
        source='get_estado_display', read_only=True
    )

    class Meta:
        model = Terminal
        fields = [
            'id', 'aeropuerto', 'aeropuerto_nombre', 'aeropuerto_codigo',
            'nombre', 'codigo', 'capacidad_puertas', 'estado',
            'estado_display', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']