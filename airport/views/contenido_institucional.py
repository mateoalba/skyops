import json

from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from airport.models.contenido_institucional import ContenidoInstitucional
from airport.serializers.contenido_institucional import ContenidoInstitucionalSerializer
from airport.permissions import EsAdmin


class ContenidoInstitucionalViewSet(viewsets.ViewSet):
    """
    GET  /api/contenido-institucional/          -> lista todo el contenido configurado
                                                    (público: las páginas institucionales
                                                    son públicas, se ven sin sesión)
    PUT  /api/contenido-institucional/{clave}/  -> crea o reemplaza el contenido de esa
                                                    clave (solo admin)

    Mismo patrón que BannerPromocionalViewSet: no hay 'create'/'destroy' clásicos,
    las claves las define el frontend (about_hero, about_features, help_faq,
    legal_terminos, etc.) y la fila se crea sola (get_or_create) la primera vez
    que un admin guarda algo.

    La imagen admite las mismas dos formas que los banners: archivo subido
    (multipart, campo 'imagen_upload') o link pegado a mano (JSON,
    'imagen_url'), con 'quitar_imagen' para borrarla sin eliminar la fila.
    Cuando se manda archivo, 'items' viaja como texto JSON (FormData no
    soporta arrays anidados) y se decodifica acá.
    """

    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            return [EsAdmin()]
        return [permissions.AllowAny()]

    def list(self, request):
        qs = ContenidoInstitucional.objects.all()
        return Response(ContenidoInstitucionalSerializer(qs, many=True, context={"request": request}).data)

    def update(self, request, pk=None):
        contenido, _ = ContenidoInstitucional.objects.get_or_create(clave=pk)
        if "titulo" in request.data:
            contenido.titulo = request.data.get("titulo") or ""
        if "texto" in request.data:
            contenido.texto = request.data.get("texto") or ""
        if "items" in request.data:
            items = request.data.get("items") or []
            if isinstance(items, str):
                try:
                    items = json.loads(items)
                except ValueError:
                    items = []
            contenido.items = items
        if "imagen_url" in request.data:
            contenido.imagen_url = request.data.get("imagen_url") or ""
        if str(request.data.get("quitar_imagen", "")).lower() in ("1", "true"):
            contenido.imagen.delete(save=False)
            contenido.imagen = None
            contenido.imagen_url = ""
        imagen_upload = request.FILES.get("imagen_upload")
        if imagen_upload:
            contenido.imagen = imagen_upload
        contenido.save()
        return Response(ContenidoInstitucionalSerializer(contenido, context={"request": request}).data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)
