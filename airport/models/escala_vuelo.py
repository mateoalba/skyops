from django.db import models
import uuid


class EscalaVuelo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vuelo = models.ForeignKey(
        'airport.Vuelo',
        on_delete=models.CASCADE,
        related_name='escalas'
    )
    aeropuerto_escala = models.ForeignKey(
        'airport.Aeropuerto',
        on_delete=models.CASCADE,
        related_name='escalas'
    )
    numero_secuencia = models.IntegerField()
    hora_llegada = models.DateTimeField()
    hora_salida = models.DateTimeField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['vuelo', 'numero_secuencia']
        verbose_name = 'Escala de Vuelo'
        verbose_name_plural = 'Escalas de Vuelo'
        unique_together = ['vuelo', 'numero_secuencia']

    def __str__(self):
        return f"{self.vuelo} - Escala {self.numero_secuencia} en {self.aeropuerto_escala}"