import uuid
from django.db import models


class Aerolinea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    codigo_iata = models.CharField(max_length=3, unique=True)
    pais = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "aerolinea"
        verbose_name = "Aerolínea"
        verbose_name_plural = "Aerolíneas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iata})"
