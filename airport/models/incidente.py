import uuid
from django.db import models
from .vuelo import Vuelo


class Incidente(models.Model):

    class Tipo(models.TextChoices):
        TECNICO = "tecnico", "Técnico"
        MEDICO = "medico", "Médico"
        SEGURIDAD = "seguridad", "Seguridad"
        METEOROLOGICO = "meteorologico", "Meteorológico"
        OPERACIONAL = "operacional", "Operacional"
        OTRO = "otro", "Otro"

    class Severidad(models.TextChoices):
        BAJA = "baja", "Baja"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"
        CRITICA = "critica", "Crítica"

    class EstadoResolucion(models.TextChoices):
        ABIERTO = "abierto", "Abierto"
        EN_PROCESO = "en_proceso", "En proceso"
        RESUELTO = "resuelto", "Resuelto"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vuelo = models.ForeignKey(
        Vuelo, on_delete=models.CASCADE, related_name="incidentes"
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    descripcion = models.TextField()
    severidad = models.CharField(max_length=10, choices=Severidad.choices)
    reportado_en = models.DateTimeField(auto_now_add=True)
    estado_resolucion = models.CharField(
        max_length=20,
        choices=EstadoResolucion.choices,
        default=EstadoResolucion.ABIERTO,
    )

    class Meta:
        db_table = "incidente"
        verbose_name = "Incidente"
        verbose_name_plural = "Incidentes"
        ordering = ["-reportado_en"]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.get_severidad_display()} | Vuelo {self.vuelo.numero_vuelo}"
