import uuid
from django.db import models
from .vuelo import Vuelo
from .tripulante import Tripulante


class AsignacionTripulacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vuelo = models.ForeignKey(
        Vuelo, on_delete=models.CASCADE, related_name="asignaciones_tripulacion"
    )
    tripulante = models.ForeignKey(
        Tripulante, on_delete=models.CASCADE, related_name="asignaciones"
    )
    rol_asignado = models.CharField(max_length=50)

    class Meta:
        db_table = "asignacion_tripulacion"
        verbose_name = "Asignación de tripulación"
        verbose_name_plural = "Asignaciones de tripulación"
        unique_together = ["vuelo", "tripulante"]

    def __str__(self):
        return f"{self.tripulante} → {self.vuelo.numero_vuelo} ({self.rol_asignado})"
