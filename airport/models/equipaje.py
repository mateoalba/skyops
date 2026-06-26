from django.db import models
from django.core.validators import MinValueValidator


class Equipaje(models.Model):
    """Equipaje registrado asociado a una reserva específica."""

    TIPO_CHOICES = [
        ("mano", "Equipaje de mano"),
        ("bodega", "Equipaje de bodega"),
        ("especial", "Equipaje especial (bicicleta, instrumento, etc.)"),
    ]

    ESTADO_CHOICES = [
        ("registrado", "Registrado"),
        ("en_vuelo", "En vuelo"),
        ("entregado", "Entregado"),
        ("perdido", "Perdido"),
        ("dañado", "Dañado"),
        ("retenido", "Retenido por aduana"),
    ]

    reserva = models.ForeignKey(
        "airport.Reserva",
        on_delete=models.CASCADE,
        related_name="equipajes",
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="bodega")
    peso_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
    )
    descripcion = models.CharField(max_length=200, blank=True)
    codigo_etiqueta = models.CharField(max_length=20, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="registrado")
    costo_adicional = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        help_text="Cobro extra por sobrepeso o equipaje especial.",
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Equipaje"
        verbose_name_plural = "Equipajes"
        ordering = ["reserva", "tipo"]

    def __str__(self):
        return f"[{self.codigo_etiqueta}] {self.get_tipo_display()} — Reserva {self.reserva}"
