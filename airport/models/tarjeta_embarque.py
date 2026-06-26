from django.db import models
import uuid


class TarjetaEmbarque(models.Model):
    """
    Boarding pass generado para una reserva confirmada.
    Relación OneToOne con Reserva.
    """

    ESTADO_CHOICES = [
        ("generada", "Generada"),
        ("usada", "Usada — pasajero abordó"),
        ("cancelada", "Cancelada"),
        ("expirada", "Expirada"),
    ]

    reserva = models.OneToOneField(
        "airport.Reserva",
        on_delete=models.CASCADE,
        related_name="tarjeta_embarque",
    )
    codigo_barras = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    asiento = models.CharField(max_length=5)             # Ej: "14A", "22C"
    puerta_embarque = models.CharField(max_length=10)    # Ej: "G12"
    grupo_embarque = models.CharField(max_length=5, blank=True)  # Ej: "A", "B1"
    hora_limite_embarque = models.DateTimeField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="generada")
    fecha_emision = models.DateTimeField(auto_now_add=True)
    check_in_online = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tarjeta de Embarque"
        verbose_name_plural = "Tarjetas de Embarque"
        ordering = ["-fecha_emision"]

    def __str__(self):
        return f"Boarding Pass {self.codigo_barras} — Asiento {self.asiento}"
