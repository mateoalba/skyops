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
    # 'foto_url' se mantiene por compatibilidad (permite pegar un link a
    # mano); el flujo normal ahora es subir un archivo directamente desde
    # el dispositivo del admin -> 'foto'. Si 'foto' tiene un archivo, el
    # serializer lo prioriza sobre 'foto_url' (ver AeropuertoSerializer).
    foto_url = models.URLField(blank=True)
    foto = models.ImageField(upload_to="aeropuertos/", null=True, blank=True)

    class Meta:
        db_table = "aeropuerto"
        verbose_name = "Aeropuerto"
        verbose_name_plural = "Aeropuertos"
        ordering = ["pais", "ciudad"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iata})"
