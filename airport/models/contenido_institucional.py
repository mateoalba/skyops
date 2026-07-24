import uuid
from django.db import models


class ContenidoInstitucional(models.Model):
    """
    Texto configurable por un administrador para las páginas institucionales
    del sitio web (Acerca de, Centro de ayuda, Sala de prensa, Trabaja con
    nosotros, GitHub, y las 4 páginas legales). Mismo patrón que
    BannerPromocional: 'clave' identifica cada bloque fijo del diseño
    (about_hero, about_features, help_faq, legal_terminos, etc., definidas
    en el frontend), y la fila se crea sola (get_or_create) la primera vez
    que un admin guarda algo para esa clave.

    'items' es una lista JSON genérica de {titulo, texto, extra} que cubre
    tanto tarjetas de funcionalidades como preguntas frecuentes, integrantes
    del equipo, repositorios o secciones legales — el frontend decide cómo
    interpretar/etiquetar cada campo según la clave.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(max_length=60, unique=True)
    titulo = models.CharField(max_length=200, blank=True)
    texto = models.TextField(blank=True)
    items = models.JSONField(default=list, blank=True)
    # Mismo patrón que BannerPromocional.imagen/imagen_url: 'imagen' es el
    # archivo subido desde el panel admin, 'imagen_url' un link pegado a
    # mano (compat); el serializer prioriza el archivo subido al armar la
    # URL final. Solo los bloques "hero" de cada página usan esto por ahora.
    imagen_url = models.URLField(blank=True)
    imagen = models.ImageField(upload_to="contenido_institucional/", null=True, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "contenido_institucional"
        verbose_name = "Contenido institucional"
        verbose_name_plural = "Contenidos institucionales"
        ordering = ["clave"]

    def __str__(self):
        return self.clave
