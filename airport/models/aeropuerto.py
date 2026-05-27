import uuid
from django.db import models


class Aeropuerto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200)
    codigo_iata = models.CharField(max_length=3, unique=True)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()
    zona_horaria = models.CharField(max_length=50, default="America/Guayaquil")

    class Meta:
        db_table = "aeropuerto"
        verbose_name = "Aeropuerto"
        verbose_name_plural = "Aeropuertos"
        ordering = ["pais", "ciudad"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iata})"
