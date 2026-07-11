from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import TipoAeronave
from airport.serializers import TipoAeronaveReadSerializer, TipoAeronaveWriteSerializer
from airport.pagination import StandardPagination


class TipoAeronaveViewSet(viewsets.ModelViewSet):
    """
    CRUD de tipos/modelos de aeronave.
    Endpoint extra: GET /tipos-aeronave/{id}/aeronaves/ — aeronaves de ese tipo.
    """

    queryset = TipoAeronave.objects.prefetch_related("aeronaves").all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["categoria", "en_produccion", "fabricante"]
    search_fields   = ["fabricante", "modelo", "codigo_iata"]
    ordering_fields = ["fabricante", "modelo", "capacidad_pasajeros_max", "autonomia_km"]
    ordering        = ["fabricante", "modelo"]
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TipoAeronaveReadSerializer
        return TipoAeronaveWriteSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["get"], url_path="aeronaves")
    def aeronaves(self, request, pk=None):
        """GET /api/tipos-aeronave/{id}/aeronaves/ — aeronaves de este tipo."""
        from airport.serializers import AeronaveSerializer
        tipo = self.get_object()
        qs   = tipo.aeronaves.select_related("aerolinea").all()
        serializer = AeronaveSerializer(qs, many=True)
        return Response(serializer.data)
