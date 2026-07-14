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


def _calcular_precio(vuelo, clase, cantidad_asientos=1):
    """Precio total = precio de un asiento en esa clase x cantidad de
    asientos ocupados (adultos + niños; los bebés no pagan asiento)."""
    multiplicador = MULTIPLICADOR_CLASE.get(clase, Decimal("1.0"))
    base = vuelo.precio_base if vuelo and vuelo.precio_base else Decimal("0")
    return base * multiplicador * max(cantidad_asientos, 1)


def _parsear_asientos(numero_asiento):
    """'12A, 12B,12C' -> ['12A', '12B', '12C'] (sin vacíos, en mayúsculas)."""
    if not numero_asiento:
        return []
    return [s.strip().upper() for s in numero_asiento.split(",") if s.strip()]


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

    total_pasajeros = serializers.SerializerMethodField()

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
            "pasajeros_adultos",
            "pasajeros_ninos",
            "pasajeros_bebes",
            "total_pasajeros",
            "clase",
            "clase_display",
            "estado",
            "estado_display",
            "reservado_en",
            "precio",
        ]
        read_only_fields = ["id", "codigo_reserva", "reservado_en", "precio"]

    def get_total_pasajeros(self, obj):
        return obj.pasajeros_adultos + obj.pasajeros_ninos + obj.pasajeros_bebes

    def validate(self, data):
        request = self.context.get("request")
        if request is not None:
            user = request.user
            es_staff = user.is_staff or user.groups.filter(name="Operadores").exists()
            if not es_staff:
                # Un usuario normal solo puede reservar para sí mismo: el
                # pasajero elegido debe tener el mismo email que su cuenta.
                pasajero = data.get("pasajero") or getattr(self.instance, "pasajero", None)
                if pasajero is None or pasajero.email != user.email:
                    raise serializers.ValidationError(
                        {"pasajero": "Solo puedes crear o editar reservas a tu propio nombre."}
                    )

        adultos = data.get("pasajeros_adultos", getattr(self.instance, "pasajeros_adultos", 1))
        ninos = data.get("pasajeros_ninos", getattr(self.instance, "pasajeros_ninos", 0))
        if adultos < 1:
            raise serializers.ValidationError(
                {"pasajeros_adultos": "Debe haber al menos 1 pasajero adulto en la reserva."}
            )

        if "numero_asiento" in data:
            asientos = _parsear_asientos(data["numero_asiento"])
            if len(asientos) != adultos + ninos:
                raise serializers.ValidationError(
                    {"numero_asiento": f"Elegiste {len(asientos)} asiento(s) pero se necesitan {adultos + ninos} "
                                        "(uno por cada adulto y niño; los bebés no ocupan asiento)."}
                )
            if len(set(asientos)) != len(asientos):
                raise serializers.ValidationError(
                    {"numero_asiento": "Hay asientos repetidos en la misma reserva."}
                )

            vuelo = data.get("vuelo") or getattr(self.instance, "vuelo", None)
            if vuelo is not None:
                otras = Reserva.objects.filter(vuelo=vuelo).exclude(estado=Reserva.Estado.CANCELADA)
                if self.instance is not None:
                    otras = otras.exclude(pk=self.instance.pk)
                ocupados = set()
                for r in otras:
                    ocupados.update(_parsear_asientos(r.numero_asiento))
                choque = ocupados.intersection(asientos)
                if choque:
                    raise serializers.ValidationError(
                        {"numero_asiento": f"Estos asientos ya están ocupados en este vuelo: {', '.join(sorted(choque))}."}
                    )

        return data

    def create(self, validated_data):
        vuelo = validated_data.get("vuelo")
        clase = validated_data.get("clase", Reserva.Clase.ECONOMICA)
        adultos = validated_data.get("pasajeros_adultos", 1)
        ninos = validated_data.get("pasajeros_ninos", 0)
        validated_data["precio"] = _calcular_precio(vuelo, clase, adultos + ninos)
        reserva = super().create(validated_data)
        _notificar_estado_reserva(reserva)
        return reserva

    def update(self, instance, validated_data):
        estado_anterior = instance.estado
        # El precio solo se recalcula si cambia el vuelo, la clase o la
        # cantidad de pasajeros (p. ej. un admin corrige la reserva); si
        # no, queda "congelado" tal como se cobró originalmente aunque el
        # precio_base del vuelo haya cambiado.
        campos_que_afectan_precio = {"vuelo", "clase", "pasajeros_adultos", "pasajeros_ninos"}
        if campos_que_afectan_precio.intersection(validated_data.keys()):
            vuelo = validated_data.get("vuelo", instance.vuelo)
            clase = validated_data.get("clase", instance.clase)
            adultos = validated_data.get("pasajeros_adultos", instance.pasajeros_adultos)
            ninos = validated_data.get("pasajeros_ninos", instance.pasajeros_ninos)
            validated_data["precio"] = _calcular_precio(vuelo, clase, adultos + ninos)
        reserva = super().update(instance, validated_data)
        if reserva.estado != estado_anterior:
            _notificar_estado_reserva(reserva)
        return reserva
