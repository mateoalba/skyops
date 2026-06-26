from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import CategoriaPasajero
from airport.serializers import CategoriaPasajeroReadSerializer, CategoriaPasajeroWriteSerializer
from airport.pagination import StandardPagination


class CategoriaPasajeroViewSet(viewsets.ModelViewSet):
    """
    CRUD de categorías de pasajero.
    Endpoint extra: GET /categorias-pasajero/{id}/pasajeros/ — lista los pasajeros de esa categoría.
    """

    queryset = CategoriaPasajero.objects.prefetch_related("pasajeros").all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["tipo", "activa", "requiere_asistencia"]
    search_fields   = ["nombre", "descripcion"]
    ordering_fields = ["nombre", "tipo"]
    ordering        = ["nombre"]
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CategoriaPasajeroReadSerializer
        return CategoriaPasajeroWriteSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["get"], url_path="pasajeros")
    def pasajeros(self, request, pk=None):
        """GET /api/categorias-pasajero/{id}/pasajeros/ — pasajeros en esa categoría."""
        from airport.serializers import PasajeroSerializer
        categoria = self.get_object()
        qs = categoria.pasajeros.all()
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(PasajeroSerializer(page, many=True).data)
        return Response(PasajeroSerializer(qs, many=True).data)
