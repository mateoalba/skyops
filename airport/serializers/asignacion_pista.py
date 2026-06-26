from rest_framework import serializers
from airport.models import AsignacionPista


class AsignacionPistaSerializer(serializers.ModelSerializer):
    vuelo_numero = serializers.CharField(
        source='vuelo.numero_vuelo', read_only=True
    )
    pista_identificador = serializers.CharField(
        source='pista.identificador', read_only=True
    )
    tipo_operacion_display = serializers.CharField(
        source='get_tipo_operacion_display', read_only=True
    )

    class Meta:
        model = AsignacionPista
        fields = [
            'id', 'vuelo', 'vuelo_numero', 'pista', 'pista_identificador',
            'tipo_operacion', 'tipo_operacion_display',
            'hora_inicio', 'hora_fin', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']