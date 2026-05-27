import uuid
from django.db import models
from .aeropuerto import Aeropuerto


class Puerta(models.Model):

    class Estado(models.TextChoices):
        DISPONIBLE = "disponible", "Disponible"
        OCUPADA = "ocupada", "Ocupada"
        MANTENIMIENTO = "mantenimiento", "En mantenimiento"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aeropuerto = models.ForeignKey(
        Aeropuerto, on_delete=models.CASCADE, related_name="puertas"
    )
    codigo = models.CharField(max_length=10)
    terminal = models.CharField(max_length=50)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.DISPONIBLE
    )

    class Meta:
        db_table = "puerta"
        verbose_name = "Puerta"
        verbose_name_plural = "Puertas"
        ordering = ["terminal", "codigo"]
        unique_together = ["aeropuerto", "codigo"]

    def __str__(self):
        return f"Terminal {self.terminal} - Puerta {self.codigo} ({self.aeropuerto.codigo_iata})"
