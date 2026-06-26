from rest_framework import serializers
from airport.models import Notificacion


class NotificacionReadSerializer(serializers.ModelSerializer):
    tipo_display   = serializers.CharField(source="get_tipo_display", read_only=True)
    canal_display  = serializers.CharField(source="get_canal_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    pasajero_nombre = serializers.SerializerMethodField()
    vuelo_numero    = serializers.CharField(source="vuelo.numero", read_only=True, default=None)

    class Meta:
        model = Notificacion
        fields = [
            "id",
            "pasajero",
            "pasajero_nombre",
            "vuelo",
            "vuelo_numero",
            "tipo",
            "tipo_display",
            "canal",
            "canal_display",
            "asunto",
            "mensaje",
            "estado",
            "estado_display",
            "fecha_envio",
            "fecha_lectura",
            "creada_en",
        ]

    def get_pasajero_nombre(self, obj):
        return f"{obj.pasajero.nombre} {obj.pasajero.apellido}"


class NotificacionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = [
            "pasajero",
            "vuelo",
            "tipo",
            "canal",
            "asunto",
            "mensaje",
            "estado",
            "fecha_envio",
            "fecha_lectura",
        ]

    def validate(self, attrs):
        estado       = attrs.get("estado", "pendiente")
        fecha_envio  = attrs.get("fecha_envio")
        fecha_lectura = attrs.get("fecha_lectura")

        if estado in ("enviada", "leida") and not fecha_envio:
            raise serializers.ValidationError(
                {"fecha_envio": "Una notificación enviada debe tener fecha de envío."}
            )
        if estado == "leida" and not fecha_lectura:
            raise serializers.ValidationError(
                {"fecha_lectura": "Una notificación leída debe tener fecha de lectura."}
            )
        if fecha_envio and fecha_lectura and fecha_lectura < fecha_envio:
            raise serializers.ValidationError(
                {"fecha_lectura": "La fecha de lectura no puede ser anterior a la de envío."}
            )
        return attrs
