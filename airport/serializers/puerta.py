from rest_framework import serializers
from airport.models import Puerta


class PuertaSerializer(serializers.ModelSerializer):
    aeropuerto_nombre = serializers.CharField(
        source="aeropuerto.nombre", read_only=True
    )
    aeropuerto_codigo = serializers.CharField(
        source="aeropuerto.codigo_iata", read_only=True
    )
    # 'terminal' ahora es el id de una Terminal real (antes era texto
    # libre) — estos dos, igual que aeropuerto_nombre/aeropuerto_codigo,
    # son solo para mostrar sin tener que pedir /terminales/ aparte.
    # SerializerMethodField (no CharField con source anidado) porque
    # 'terminal' puede ser None en filas creadas antes de este cambio.
    terminal_nombre = serializers.SerializerMethodField()
    terminal_codigo = serializers.SerializerMethodField()
    estado_display = serializers.CharField(
        source="get_estado_display", read_only=True
    )

    class Meta:
        model = Puerta
        fields = [
            "id",
            "aeropuerto",
            "aeropuerto_nombre",
            "aeropuerto_codigo",
            "codigo",
            "terminal",
            "terminal_nombre",
            "terminal_codigo",
            "estado",
            "estado_display",
        ]
        read_only_fields = ["id"]

    def get_terminal_nombre(self, obj):
        return obj.terminal.nombre if obj.terminal else None

    def get_terminal_codigo(self, obj):
        return obj.terminal.codigo if obj.terminal else None
