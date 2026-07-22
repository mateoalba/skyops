import uuid
from django.db import models
from .aerolinea import Aerolinea


class Aeronave(models.Model):

    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        MANTENIMIENTO = "mantenimiento", "En mantenimiento"
        RETIRADA = "retirada", "Retirada"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aerolinea = models.ForeignKey(
        Aerolinea, on_delete=models.CASCADE, related_name="aeronaves"
    )
    matricula = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.ACTIVA
    )
    # 'foto_url' guarda un link pegado a mano, 'foto' es el archivo subido
    # desde el panel — mismo patrón que Aeropuerto.foto_url / Aeropuerto.foto
    # y Aerolinea.logo_url / Aerolinea.logo.
    foto_url = models.URLField(blank=True)
    foto = models.ImageField(upload_to="aeronaves/", null=True, blank=True)

    class Meta:
        db_table = "aeronave"
        verbose_name = "Aeronave"
        verbose_name_plural = "Aeronaves"
        ordering = ["matricula"]

    def __str__(self):
        return f"{self.matricula} - {self.modelo} ({self.aerolinea.codigo_iata})"
