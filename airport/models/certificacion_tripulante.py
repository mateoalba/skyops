import uuid
from django.db import models
from .tripulante import Tripulante


class CertificacionTripulante(models.Model):

    class Tipo(models.TextChoices):
        LICENCIA_PILOTO = "licencia_piloto", "Licencia de piloto"
        HABILITACION_TIPO = "habilitacion_tipo", "Habilitación de tipo"
        CERT_MEDICO = "cert_medico", "Certificado médico"
        RECURRENTE = "recurrente", "Recurrente"
        EMERGENCIAS = "emergencias", "Emergencias"
        SERVICIO_CABINA = "servicio_cabina", "Servicio de cabina"
        SEGURIDAD = "seguridad", "Seguridad"

    class Estado(models.TextChoices):
        VIGENTE = "vigente", "Vigente"
        POR_VENCER = "por_vencer", "Por vencer"
        VENCIDA = "vencida", "Vencida"
        SUSPENDIDA = "suspendida", "Suspendida"
        RENOVADA = "renovada", "Renovada"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tripulante = models.ForeignKey(
        Tripulante, on_delete=models.CASCADE, related_name="certificaciones"
    )
    tipo_aeronave_habilitado = models.CharField(
        max_length=100,
        blank=True,
        help_text="Modelo de aeronave habilitado. Ej: Boeing 737, Airbus A320.",
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.VIGENTE
    )
    numero_certificado = models.CharField(max_length=50, unique=True)
    entidad_emisora = models.CharField(max_length=200)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "certificacion_tripulante"
        verbose_name = "Certificación de tripulante"
        verbose_name_plural = "Certificaciones de tripulante"
        ordering = ["fecha_vencimiento"]

    def __str__(self):
        return f"{self.tripulante} - {self.get_tipo_display()} - {self.numero_certificado}"
