import uuid
from django.db import models
from .aerolinea import Aerolinea


class Tripulante(models.Model):

    class Rol(models.TextChoices):
        PILOTO = "piloto", "Piloto"
        COPILOTO = "copiloto", "Copiloto"
        AUXILIAR = "auxiliar", "Auxiliar de vuelo"
        JEFE_CABINA = "jefe_cabina", "Jefe de cabina"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aerolinea = models.ForeignKey(
        Aerolinea, on_delete=models.CASCADE, related_name="tripulantes"
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=Rol.choices)
    num_licencia = models.CharField(max_length=30, unique=True)
    disponible = models.BooleanField(default=True)

    class Meta:
        db_table = "tripulante"
        verbose_name = "Tripulante"
        verbose_name_plural = "Tripulantes"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.get_rol_display()}"
