from django.db import models
import uuid


class PistaAterrizaje(models.Model):
    SUPERFICIE_CHOICES = [
        ('asfalto', 'Asfalto'),
        ('concreto', 'Concreto'),
        ('cesped', 'Césped'),
        ('grava', 'Grava'),
    ]
    ESTADO_CHOICES = [
        ('operativa', 'Operativa'),
        ('cerrada', 'Cerrada'),
        ('mantenimiento', 'En mantenimiento'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aeropuerto = models.ForeignKey(
        'airport.Aeropuerto',
        on_delete=models.CASCADE,
        related_name='pistas'
    )
    identificador = models.CharField(max_length=10)
    longitud_metros = models.IntegerField()
    superficie = models.CharField(max_length=20, choices=SUPERFICIE_CHOICES, default='asfalto')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='operativa')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['aeropuerto', 'identificador']
        verbose_name = 'Pista de Aterrizaje'
        verbose_name_plural = 'Pistas de Aterrizaje'

    def __str__(self):
        return f"{self.identificador} - {self.aeropuerto}"