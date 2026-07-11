from rest_framework import serializers
from airport.models import TarjetaEmbarque, Reserva


class TarjetaEmbarqueReadSerializer(serializers.ModelSerializer):
    estado_display  = serializers.CharField(source="get_estado_display", read_only=True)
    pasajero_nombre = serializers.SerializerMethodField()
    vuelo_numero    = serializers.SerializerMethodField()
    vuelo_salida    = serializers.SerializerMethodField()
    aerolinea       = serializers.SerializerMethodField()

    class Meta:
        model = TarjetaEmbarque
        fields = [
            "id",
            "reserva",
            "pasajero_nombre",
            "vuelo_numero",
            "vuelo_salida",
            "aerolinea",
            "codigo_barras",
            "asiento",
            "puerta_embarque",
            "grupo_embarque",
            "hora_limite_embarque",
            "estado",
            "estado_display",
            "fecha_emision",
            "check_in_online",
            "observaciones",
        ]

    def get_pasajero_nombre(self, obj):
        p = obj.reserva.pasajero
        return f"{p.nombre} {p.apellido}"

    def get_vuelo_numero(self, obj):
        return obj.reserva.vuelo.numero_vuelo

    def get_vuelo_salida(self, obj):
        return obj.reserva.vuelo.salida_programada

    def get_aerolinea(self, obj):
        return obj.reserva.vuelo.aerolinea.nombre


class TarjetaEmbarqueWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarjetaEmbarque
        fields = [
            "reserva",
            "asiento",
            "puerta_embarque",
            "grupo_embarque",
            "hora_limite_embarque",
            "estado",
            "check_in_online",
            "observaciones",
        ]

    def validate_reserva(self, value):
        # Solo reservas confirmadas pueden tener tarjeta de embarque
        if value.estado not in ("confirmada", "checked_in"):
            raise serializers.ValidationError(
                "Solo se puede generar tarjeta para reservas confirmadas."
            )
        # Verificar que no exista ya una tarjeta para esta reserva (OneToOne)
        qs = TarjetaEmbarque.objects.filter(reserva=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Esta reserva ya tiene una tarjeta de embarque generada."
            )
        return value

    def validate_asiento(self, value):
        return value.upper().strip()
