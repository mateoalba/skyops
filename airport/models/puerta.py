import uuid
from django.db import models
from .aeropuerto import Aeropuerto
from .terminal import Terminal


class Puerta(models.Model):

    class Estado(models.TextChoices):
        DISPONIBLE = "disponible", "Disponible"
        OCUPADA = "ocupada", "Ocupada"
        MANTENIMIENTO = "mantenimiento", "En mantenimiento"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aeropuerto = models.ForeignKey(
        Aeropuerto, on_delete=models.CASCADE, related_name="puertas"
    )
    codigo = models.CharField(max_length=10)
    # Antes era un CharField de texto libre, sin ninguna relación real con la
    # tabla Terminal (se podía escribir "T1", "Terminal 1" o "t1" para lo
    # mismo, sin validar que esa terminal existiera de verdad). Ahora es una
    # FK real — `null=True` es solo para no romper las filas creadas antes de
    # este cambio (quedan con terminal=None hasta que se reasignen a mano);
    # el serializer sigue exigiendo el campo en cualquier alta/edición nueva.
    terminal = models.ForeignKey(
        Terminal, on_delete=models.CASCADE, related_name="puertas", null=True
    )
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.DISPONIBLE
    )

    class Meta:
        db_table = "puerta"
        verbose_name = "Puerta"
        verbose_name_plural = "Puertas"
        ordering = ["terminal", "codigo"]
        unique_together = ["aeropuerto", "codigo"]

    def __str__(self):
        terminal_str = self.terminal.codigo if self.terminal else "s/n"
        return f"Terminal {terminal_str} - Puerta {self.codigo} ({self.aeropuerto.codigo_iata})"
