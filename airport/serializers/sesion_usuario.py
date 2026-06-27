from rest_framework import serializers
from airport.models.sesion_usuario import SesionUsuario


class SesionUsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)
    resultado_display = serializers.CharField(
        source="get_resultado_display", read_only=True
    )
    duracion_segundos = serializers.SerializerMethodField()

    class Meta:
        model = SesionUsuario
        fields = [
            "id",
            "usuario",
            "username",
            "ip_address",
            "user_agent",
            "resultado",
            "resultado_display",
            "token_jti",
            "fecha_hora",
            "fecha_cierre",
            "duracion_segundos",
        ]
        read_only_fields = ["id", "fecha_hora"]

    def get_duracion_segundos(self, obj):
        if obj.fecha_cierre is None:
            return None
        delta = obj.fecha_cierre - obj.fecha_hora
        return int(delta.total_seconds())
