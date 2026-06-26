from rest_framework import serializers
from airport.models.audit_log import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)
    accion_display = serializers.CharField(
        source="get_accion_display", read_only=True
    )
    modelo_afectado = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "usuario",
            "username",
            "accion",
            "accion_display",
            "content_type",
            "object_id",
            "modelo_afectado",
            "descripcion",
            "datos_anteriores",
            "datos_nuevos",
            "ip_address",
            "fecha_hora",
        ]
        read_only_fields = ["id", "fecha_hora"]

    def get_modelo_afectado(self, obj):
        if obj.content_type:
            return obj.content_type.model
        return None
