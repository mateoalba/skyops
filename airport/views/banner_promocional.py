from rest_framework import viewsets, permissions
from rest_framework.response import Response
from airport.models.banner_promocional import BannerPromocional
from airport.serializers.banner_promocional import BannerPromocionalSerializer
from airport.permissions import EsAdmin


class BannerPromocionalViewSet(viewsets.ViewSet):
    """
    GET  /api/banners/          -> lista los banners configurados (público, sin login:
                                    se usa en el carrusel público y en el login)
    PUT  /api/banners/{clave}/  -> crea o reemplaza el contenido de esa clave (solo admin)

    No hay 'create' ni 'destroy' clásicos: las claves las define el propio
    Flutter (dashboard, vuelos, oferta_1, oferta_2, oferta_3,
    carrusel_operaciones, carrusel_infraestructura, carrusel_flota,
    carrusel_personas, carrusel_administracion, login_hero) y la fila se
    crea sola (get_or_create) la primera vez que un admin guarda algo.
    Mandar un campo en '' lo "quita" sin borrar la fila.
    """

    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            return [EsAdmin()]
        # list/retrieve son públicos a propósito: el carrusel público y el
        # encabezado del login se muestran ANTES de iniciar sesión.
        return [permissions.AllowAny()]

    def list(self, request):
        qs = BannerPromocional.objects.all()
        return Response(BannerPromocionalSerializer(qs, many=True).data)

    def update(self, request, pk=None):
        banner, _ = BannerPromocional.objects.get_or_create(clave=pk)
        if "titulo" in request.data:
            banner.titulo = request.data.get("titulo") or ""
        if "texto" in request.data:
            banner.texto = request.data.get("texto") or ""
        if "imagen_url" in request.data:
            banner.imagen_url = request.data.get("imagen_url") or ""
        banner.save()
        return Response(BannerPromocionalSerializer(banner).data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)
