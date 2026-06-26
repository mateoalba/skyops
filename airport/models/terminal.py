from django.db import models
import uuid


class Terminal(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
        ('mantenimiento', 'En mantenimiento'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aeropuerto = models.ForeignKey(
        'airport.Aeropuerto',
        on_delete=models.CASCADE,
        related_name='terminales'
    )
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    capacidad_puertas = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['aeropuerto', 'codigo']
        verbose_name = 'Terminal'
        verbose_name_plural = 'Terminales'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"