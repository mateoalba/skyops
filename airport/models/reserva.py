import uuid
import random
import string
from django.db import models
from .vuelo import Vuelo
from .pasajero import Pasajero


def generar_codigo_reserva():
    """Genera un código único de 6 caracteres alfanuméricos en mayúsculas."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Reserva(models.Model):

    class Clase(models.TextChoices):
        ECONOMICA = "economica", "Económica"
        EJECUTIVA = "ejecutiva", "Ejecutiva"
        PRIMERA = "primera", "Primera clase"

    class Estado(models.TextChoices):
        CONFIRMADA = "confirmada", "Confirmada"
        PENDIENTE = "pendiente", "Pendiente"
        CANCELADA = "cancelada", "Cancelada"
        ABORDADA = "abordada", "Abordada"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vuelo = models.ForeignKey(
        Vuelo, on_delete=models.CASCADE, related_name="reservas"
    )
    pasajero = models.ForeignKey(
        Pasajero, on_delete=models.CASCADE, related_name="reservas"
    )
    # Uno o varios códigos de asiento separados por coma (ej. "12A,12B"),
    # uno por cada pasajero que SÍ ocupa asiento (adultos + niños; los
    # bebés viajan en brazos y no cuentan aquí). Antes era un solo asiento
    # por reserva; ahora una reserva puede cubrir un grupo completo. Ver
    # validate() en ReservaSerializer para el chequeo de solapamiento
    # (ya no se puede usar unique_together porque el campo es una lista).
    numero_asiento = models.CharField(max_length=120)
    # Desglose de personas cubiertas por esta reserva. pasajeros_adultos
    # siempre debe ser >= 1 (el titular). El precio se calcula sobre
    # (pasajeros_adultos + pasajeros_ninos) asientos — ver _calcular_precio
    # en el serializer.
    pasajeros_adultos = models.PositiveIntegerField(default=1)
    pasajeros_ninos = models.PositiveIntegerField(default=0)
    pasajeros_bebes = models.PositiveIntegerField(default=0)
    clase = models.CharField(
        max_length=20, choices=Clase.choices, default=Clase.ECONOMICA
    )
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PENDIENTE
    )
    codigo_reserva = models.CharField(
        max_length=6, unique=True, default=generar_codigo_reserva
    )
    reservado_en = models.DateTimeField(auto_now_add=True)

    # Precio "congelado" en el momento de la reserva (vuelo.precio_base x
    # multiplicador de la clase elegida). Se calcula una sola vez al crear
    # o al cambiar de clase/vuelo en una edición — ver ReservaSerializer.
    # Si después el admin sube el precio_base del vuelo, las reservas ya
    # hechas NO cambian de precio (igual que en una aerolínea real).
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "reserva"
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-reservado_en"]
        # Ya no hay unique_together de (vuelo, numero_asiento): ese campo
        # ahora puede contener varios asientos separados por coma, así que
        # el solapamiento entre reservas se valida a mano en el serializer.

    def __str__(self):
        return f"{self.codigo_reserva} | {self.pasajero} | {self.vuelo.numero_vuelo}"
