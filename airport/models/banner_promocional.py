import uuid
from django.db import models


class BannerPromocional(models.Model):
    """
    Imagen configurable por un administrador para los espacios
    promocionales de la app (encabezado del home, encabezado de la
    lista de vuelos, carrusel de ofertas). 'clave' identifica cada
    espacio fijo del diseño Flutter (dashboard, vuelos, oferta_1,
    oferta_2, oferta_3); las filas se crean solas (get_or_create) la
    primera vez que un admin guarda una imagen para esa clave.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(max_length=40, unique=True)
    imagen_url = models.URLField(blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "banner_promocional"
        verbose_name = "Banner promocional"
        verbose_name_plural = "Banners promocionales"
        ordering = ["clave"]

    def __str__(self):
        return self.clave
