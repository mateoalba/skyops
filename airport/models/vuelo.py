import uuid
from django.db import models
from .aerolinea import Aerolinea
from .aeronave import Aeronave
from .aeropuerto import Aeropuerto
from .puerta import Puerta


class Vuelo(models.Model):

    class Estado(models.TextChoices):
        PROGRAMADO = "programado", "Programado"
        EMBARCANDO = "embarcando", "Embarcando"
        DESPEGADO = "despegado", "Despegado"
        ATERRIZADO = "aterrizado", "Aterrizado"
        CANCELADO = "cancelado", "Cancelado"
        RETRASADO = "retrasado", "Retrasado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aerolinea = models.ForeignKey(
        Aerolinea, on_delete=models.CASCADE, related_name="vuelos"
    )
    aeronave = models.ForeignKey(
        Aeronave, on_delete=models.SET_NULL, null=True, related_name="vuelos"
    )
    origen = models.ForeignKey(
        Aeropuerto, on_delete=models.CASCADE, related_name="vuelos_salida"
    )
    destino = models.ForeignKey(
        Aeropuerto, on_delete=models.CASCADE, related_name="vuelos_llegada"
    )
    puerta = models.ForeignKey(
        Puerta, on_delete=models.SET_NULL, null=True, blank=True, related_name="vuelos"
    )
    numero_vuelo = models.CharField(max_length=10)
    salida_programada = models.DateTimeField()
    llegada_programada = models.DateTimeField()
    salida_real = models.DateTimeField(null=True, blank=True)
    llegada_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PROGRAMADO
    )
    duracion_min = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "vuelo"
        verbose_name = "Vuelo"
        verbose_name_plural = "Vuelos"
        ordering = ["salida_programada"]
        unique_together = ["aerolinea", "numero_vuelo", "salida_programada"]

    def __str__(self):
        return f"{self.numero_vuelo} | {self.origen.codigo_iata} → {self.destino.codigo_iata} | {self.salida_programada.strftime('%d/%m/%Y %H:%M')}"
