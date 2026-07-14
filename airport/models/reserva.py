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
    numero_asiento = models.CharField(max_length=5)
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
        unique_together = ["vuelo", "numero_asiento"]

    def __str__(self):
        return f"{self.codigo_reserva} | {self.pasajero} | {self.vuelo.numero_vuelo}"
