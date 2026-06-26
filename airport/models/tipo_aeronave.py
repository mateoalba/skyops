from django.db import models
from django.core.validators import MinValueValidator


class TipoAeronave(models.Model):
    """
    Catálogo de tipos/modelos de aeronave (Boeing 737, Airbus A320, etc.).
    Las aeronaves concretas referencian su tipo aquí.
    """

    CATEGORIA_CHOICES = [
        ("narrow", "Narrow-body (pasillo único)"),
        ("wide", "Wide-body (doble pasillo)"),
        ("regional", "Regional / turbohélice"),
        ("cargo", "Carguero"),
        ("privado", "Aviación privada"),
    ]

    fabricante = models.CharField(max_length=100)         # Ej: "Boeing", "Airbus"
    modelo = models.CharField(max_length=100)             # Ej: "737-800", "A320neo"
    codigo_iata = models.CharField(max_length=10, unique=True, blank=True)  # Ej: "738"
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    capacidad_pasajeros_min = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    capacidad_pasajeros_max = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    autonomia_km = models.PositiveIntegerField(help_text="Alcance máximo en kilómetros.")
    velocidad_crucero_kmh = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True)
    en_produccion = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de Aeronave"
        verbose_name_plural = "Tipos de Aeronave"
        ordering = ["fabricante", "modelo"]
        unique_together = ["fabricante", "modelo"]

    def __str__(self):
        return f"{self.fabricante} {self.modelo}"
