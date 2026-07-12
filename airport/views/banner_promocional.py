from rest_framework import viewsets, permissions
from rest_framework.response import Response
from airport.models.banner_promocional import BannerPromocional
from airport.serializers.banner_promocional import BannerPromocionalSerializer
from airport.permissions import EsAdmin


class BannerPromocionalViewSet(viewsets.ViewSet):
    """
    GET  /api/banners/          -> lista los banners configurados (cualquier usuario autenticado)
    PUT  /api/banners/{clave}/  -> crea o reemplaza la imagen de esa clave (solo admin)

    No hay 'create' ni 'destroy' clásicos: las claves las define el propio
    Flutter (dashboard, vuelos, oferta_1, oferta_2, oferta_3) y la fila se
    crea sola (get_or_create) la primera vez que un admin guarda una URL.
    Mandar imagen_url='' "quita" la imagen sin borrar la fila.
    """

    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            return [EsAdmin()]
        return [permissions.IsAuthenticated()]

    def list(self, request):
        qs = BannerPromocional.objects.all()
        return Response(BannerPromocionalSerializer(qs, many=True).data)

    def update(self, request, pk=None):
        banner, _ = BannerPromocional.objects.get_or_create(clave=pk)
        banner.imagen_url = request.data.get("imagen_url", "") or ""
        banner.save(update_fields=["imagen_url", "actualizado_en"])
        return Response(BannerPromocionalSerializer(banner).data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)
