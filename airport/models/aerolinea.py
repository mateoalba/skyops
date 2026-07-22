import uuid
from django.db import models


class Aerolinea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    codigo_iata = models.CharField(max_length=3, unique=True)
    pais = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    # 'logo_url' guarda un link pegado a mano (compat con aerolíneas viejas),
    # 'logo' es el archivo subido desde el panel — mismo patrón que
    # Aeropuerto.foto_url / Aeropuerto.foto.
    logo_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="aerolineas/", null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "aerolinea"
        verbose_name = "Aerolínea"
        verbose_name_plural = "Aerolíneas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iata})"
