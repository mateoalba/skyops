from decimal import Decimal
from django.utils import timezone
from rest_framework import serializers
from airport.models import Reserva
from airport.models.notificacion import Notificacion


# Multiplicador sobre vuelo.precio_base (que representa el precio de
# económica) para calcular el precio real de cada clase de cabina.
MULTIPLICADOR_CLASE = {
    Reserva.Clase.ECONOMICA: Decimal("1.0"),
    Reserva.Clase.EJECUTIVA: Decimal("1.8"),
    Reserva.Clase.PRIMERA: Decimal("2.5"),
}


def _calcular_precio(vuelo, clase):
    multiplicador = MULTIPLICADOR_CLASE.get(clase, Decimal("1.0"))
    base = vuelo.precio_base if vuelo and vuelo.precio_base else Decimal("0")
    return base * multiplicador


# Texto de la notificación automática que recibe el pasajero cada vez que
# el estado de su reserva cambia (por ejemplo, cuando un admin la confirma).
# Cubre tanto el alta inicial (create) como cualquier cambio posterior
# (update/partial_update), sin importar quién lo haga (admin u operador).
_MENSAJES_ESTADO = {
    Reserva.Estado.CONFIRMADA: (
        "confirmacion",
        "Reserva confirmada",
        "Tu reserva {codigo} para el vuelo {numero_vuelo} ({origen} → {destino}) fue confirmada.",
    ),
    Reserva.Estado.PENDIENTE: (
        "otro",
        "Reserva pendiente",
        "Tu reserva {codigo} para el vuelo {numero_vuelo} ({origen} → {destino}) quedó pendiente de confirmación.",
    ),
    Reserva.Estado.CANCELADA: (
        "cancelacion",
        "Reserva cancelada",
        "Tu reserva {codigo} para el vuelo {numero_vuelo} ({origen} → {destino}) fue cancelada.",
    ),
    Reserva.Estado.ABORDADA: (
        "embarque",
        "Embarque registrado",
        "Se registró tu embarque para el vuelo {numero_vuelo} ({origen} → {destino}). ¡Buen viaje!",
    ),
}


def _notificar_estado_reserva(reserva):
    """Crea una Notificacion para el pasajero dueño de la reserva, con un
    mensaje según el estado actual (confirmada/pendiente/cancelada/abordada).
    Se llama al crear una reserva y cada vez que su estado cambia al
    actualizarla, para que el pasajero se entere sin tener que consultar
    la app activamente."""
    tipo, asunto, plantilla = _MENSAJES_ESTADO.get(
        reserva.estado,
        ("otro", "Actualización de tu reserva", "Tu reserva {codigo} cambió de estado a " + reserva.get_estado_display() + "."),
    )
    mensaje = plantilla.format(
        codigo=reserva.codigo_reserva,
        numero_vuelo=reserva.vuelo.numero_vuelo,
        origen=reserva.vuelo.origen.codigo_iata,
        destino=reserva.vuelo.destino.codigo_iata,
    )
    Notificacion.objects.create(
        pasajero=reserva.pasajero,
        vuelo=reserva.vuelo,
        tipo=tipo,
        canal="sistema",
        asunto=asunto,
        mensaje=mensaje,
        estado="enviada",
        fecha_envio=timezone.now(),
    )


class ReservaSerializer(serializers.ModelSerializer):
    pasajero_nombre = serializers.CharField(
        source="pasajero.nombre", read_only=True
    )
    pasajero_apellido = serializers.CharField(
        source="pasajero.apellido", read_only=True
    )
    vuelo_numero = serializers.CharField(
        source="vuelo.numero_vuelo", read_only=True
    )
    vuelo_origen = serializers.CharField(
        source="vuelo.origen.codigo_iata", read_only=True
    )
    vuelo_destino = serializers.CharField(
        source="vuelo.destino.codigo_iata", read_only=True
    )
    clase_display = serializers.CharField(
        source="get_clase_display", read_only=True
    )
    estado_display = serializers.CharField(
        source="get_estado_display", read_only=True
    )

    class Meta:
        model = Reserva
        fields = [
            "id",
            "codigo_reserva",
            "vuelo",
            "vuelo_numero",
            "vuelo_origen",
            "vuelo_destino",
            "pasajero",
            "pasajero_nombre",
            "pasajero_apellido",
            "numero_asiento",
            "clase",
            "clase_display",
            "estado",
            "estado_display",
            "reservado_en",
            "precio",
        ]
        read_only_fields = ["id", "codigo_reserva", "reservado_en", "precio"]

    def validate(self, data):
        request = self.context.get("request")
        if request is None:
            return data
        user = request.user
        if user.is_staff or user.groups.filter(name="Operadores").exists():
            return data
        # Un usuario normal solo puede reservar para sí mismo: el pasajero
        # elegido debe tener el mismo email que su cuenta.
        pasajero = data.get("pasajero") or getattr(self.instance, "pasajero", None)
        if pasajero is None or pasajero.email != user.email:
            raise serializers.ValidationError(
                {"pasajero": "Solo puedes crear o editar reservas a tu propio nombre."}
            )
        return data

    def create(self, validated_data):
        vuelo = validated_data.get("vuelo")
        clase = validated_data.get("clase", Reserva.Clase.ECONOMICA)
        validated_data["precio"] = _calcular_precio(vuelo, clase)
        reserva = super().create(validated_data)
        _notificar_estado_reserva(reserva)
        return reserva

    def update(self, instance, validated_data):
        estado_anterior = instance.estado
        # El precio solo se recalcula si cambia el vuelo o la clase (p. ej.
        # un admin corrige la reserva); si no, queda "congelado" tal como se
        # cobró originalmente aunque el precio_base del vuelo haya cambiado.
        if "vuelo" in validated_data or "clase" in validated_data:
            vuelo = validated_data.get("vuelo", instance.vuelo)
            clase = validated_data.get("clase", instance.clase)
            validated_data["precio"] = _calcular_precio(vuelo, clase)
        reserva = super().update(instance, validated_data)
        if reserva.estado != estado_anterior:
            _notificar_estado_reserva(reserva)
        return reserva
