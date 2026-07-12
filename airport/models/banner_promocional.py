import uuid
from django.db import models


class BannerPromocional(models.Model):
    """
    Contenido configurable por un administrador para los espacios
    promocionales/informativos de la app (encabezado del home, encabezado
    de la lista de vuelos, carrusel de ofertas, tarjetas del carrusel
    público y encabezado del login). 'clave' identifica cada espacio fijo
    del diseño Flutter (dashboard, vuelos, oferta_1, oferta_2, oferta_3,
    carrusel_operaciones, carrusel_infraestructura, carrusel_flota,
    carrusel_personas, carrusel_administracion, login_hero); las filas se
    crean solas (get_or_create) la primera vez que un admin guarda algo
    para esa clave. 'titulo'/'texto' son opcionales porque varios espacios
    (dashboard, vuelos, ofertas) solo usan la imagen.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(max_length=40, unique=True)
    titulo = models.CharField(max_length=200, blank=True)
    texto = models.TextField(blank=True)
    imagen_url = models.URLField(blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "banner_promocional"
        verbose_name = "Banner promocional"
        verbose_name_plural = "Banners promocionales"
        ordering = ["clave"]

    def __str__(self):
        return self.clave
