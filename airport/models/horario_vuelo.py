from django.db import models
import uuid


class HorarioVuelo(models.Model):
    DIAS_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aerolinea = models.ForeignKey(
        'airport.Aerolinea',
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    origen = models.ForeignKey(
        'airport.Aeropuerto',
        on_delete=models.CASCADE,
        related_name='horarios_origen'
    )
    destino = models.ForeignKey(
        'airport.Aeropuerto',
        on_delete=models.CASCADE,
        related_name='horarios_destino'
    )
    numero_vuelo_base = models.CharField(max_length=20)
    hora_salida = models.TimeField()
    dias_operacion = models.JSONField(default=list)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['hora_salida']
        verbose_name = 'Horario de Vuelo'
        verbose_name_plural = 'Horarios de Vuelo'

    def __str__(self):
        return f"{self.numero_vuelo_base} - {self.origen} → {self.destino}"