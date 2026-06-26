import uuid
from django.db import models
from .aeronave import Aeronave
from .aeropuerto import Aeropuerto


class MantenimientoAeronave(models.Model):

    class Tipo(models.TextChoices):
        PREVENTIVO = "preventivo", "Preventivo"
        CORRECTIVO = "correctivo", "Correctivo"
        REVISION_A = "revision_a", "Revisión A"
        REVISION_B = "revision_b", "Revisión B"
        REVISION_C = "revision_c", "Revisión C"
        EMERGENCIA = "emergencia", "Emergencia"

    class Estado(models.TextChoices):
        PROGRAMADO = "programado", "Programado"
        EN_PROGRESO = "en_progreso", "En progreso"
        COMPLETADO = "completado", "Completado"
        CANCELADO = "cancelado", "Cancelado"
        POSTERGADO = "postergado", "Postergado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aeronave = models.ForeignKey(
        Aeronave, on_delete=models.CASCADE, related_name="mantenimientos"
    )
    aeropuerto = models.ForeignKey(
        Aeropuerto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mantenimientos_aeronave",
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PROGRAMADO
    )
    descripcion = models.TextField()
    tecnico_responsable = models.CharField(max_length=200)
    fecha_inicio = models.DateTimeField()
    fecha_fin_estimada = models.DateTimeField()
    fecha_fin_real = models.DateTimeField(null=True, blank=True)
    costo_estimado = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    costo_real = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    horas_fuera_servicio = models.PositiveIntegerField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mantenimiento_aeronave"
        verbose_name = "Mantenimiento de aeronave"
        verbose_name_plural = "Mantenimientos de aeronave"
        ordering = ["fecha_inicio"]

    def __str__(self):
        return f"{self.aeronave.matricula} - {self.get_tipo_display()} ({self.get_estado_display()})"
