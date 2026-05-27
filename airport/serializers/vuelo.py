from rest_framework import serializers
from airport.models import Vuelo


class VueloSerializer(serializers.ModelSerializer):
    # Campos de solo lectura con info legible
    aerolinea_nombre = serializers.CharField(
        source="aerolinea.nombre", read_only=True
    )
    aeronave_matricula = serializers.CharField(
        source="aeronave.matricula", read_only=True
    )
    origen_codigo = serializers.CharField(
        source="origen.codigo_iata", read_only=True
    )
    origen_ciudad = serializers.CharField(
        source="origen.ciudad", read_only=True
    )
    destino_codigo = serializers.CharField(
        source="destino.codigo_iata", read_only=True
    )
    destino_ciudad = serializers.CharField(
        source="destino.ciudad", read_only=True
    )
    puerta_codigo = serializers.CharField(
        source="puerta.codigo", read_only=True
    )
    estado_display = serializers.CharField(
        source="get_estado_display", read_only=True
    )

    class Meta:
        model = Vuelo
        fields = [
            "id",
            "numero_vuelo",
            "aerolinea",
            "aerolinea_nombre",
            "aeronave",
            "aeronave_matricula",
            "origen",
            "origen_codigo",
            "origen_ciudad",
            "destino",
            "destino_codigo",
            "destino_ciudad",
            "puerta",
            "puerta_codigo",
            "salida_programada",
            "llegada_programada",
            "salida_real",
            "llegada_real",
            "estado",
            "estado_display",
            "duracion_min",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        origen = data.get("origen")
        destino = data.get("destino")
        if origen and destino and origen == destino:
            raise serializers.ValidationError(
                "El origen y el destino no pueden ser el mismo aeropuerto."
            )
        salida = data.get("salida_programada")
        llegada = data.get("llegada_programada")
        if salida and llegada and llegada <= salida:
            raise serializers.ValidationError(
                "La llegada programada debe ser posterior a la salida."
            )
        return data
