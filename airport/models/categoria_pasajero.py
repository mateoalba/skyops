from django.db import models


class CategoriaPasajero(models.Model):
    """
    Categorías que puede tener un pasajero: VIP, Frequent Flyer, necesidades especiales, etc.
    Relación ManyToMany con Pasajero.
    """

    TIPO_CHOICES = [
        ("frequent_flyer", "Viajero frecuente"),
        ("vip", "VIP"),
        ("discapacidad", "Pasajero con discapacidad"),
        ("menor_no_acompanado", "Menor no acompañado"),
        ("asistencia_medica", "Requiere asistencia médica"),
        ("embarazada", "Embarazada"),
        ("deportista", "Deportista / equipo"),
        ("diplomatico", "Diplomático"),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    requiere_asistencia = models.BooleanField(default=False)
    beneficios = models.TextField(
        blank=True,
        help_text="Descripción de beneficios o servicios especiales asociados.",
    )
    activa = models.BooleanField(default=True)

    # ManyToMany definido desde Pasajero apuntando aquí
    pasajeros = models.ManyToManyField(
        "airport.Pasajero",
        related_name="categorias",
        blank=True,
    )

    class Meta:
        verbose_name = "Categoría de Pasajero"
        verbose_name_plural = "Categorías de Pasajero"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
