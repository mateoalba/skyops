import uuid
from django.db import models


class Pasajero(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    num_pasaporte = models.CharField(max_length=20, unique=True)
    nacionalidad = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = "pasajero"
        verbose_name = "Pasajero"
        verbose_name_plural = "Pasajeros"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.num_pasaporte})"
