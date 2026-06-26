from django.db import models
import uuid


class AsignacionPista(models.Model):
    TIPO_OPERACION_CHOICES = [
        ('aterrizaje', 'Aterrizaje'),
        ('despegue', 'Despegue'),
        ('prueba', 'Prueba'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vuelo = models.ForeignKey(
        'airport.Vuelo',
        on_delete=models.CASCADE,
        related_name='asignaciones_pista'
    )
    pista = models.ForeignKey(
        'airport.PistaAterrizaje',
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    tipo_operacion = models.CharField(max_length=20, choices=TIPO_OPERACION_CHOICES)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['hora_inicio']
        verbose_name = 'Asignación de Pista'
        verbose_name_plural = 'Asignaciones de Pista'

    def __str__(self):
        return f"{self.vuelo} - {self.pista} - {self.tipo_operacion}"