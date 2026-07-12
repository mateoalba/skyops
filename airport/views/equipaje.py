from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Equipaje
from airport.serializers import EquipajeReadSerializer, EquipajeWriteSerializer
from airport.pagination import StandardPagination
from airport.permissions import IsOwnerOrAdmin  # permiso existente en el proyecto


class EquipajeViewSet(viewsets.ModelViewSet):
    """
    CRUD de equipaje.
    - Pasajeros ven solo su propio equipaje.
    - Admins y operadores ven todo.
    Filtros: ?tipo=bodega ?estado=perdido ?reserva=4
    """

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["tipo", "estado", "reserva"]
    search_fields   = ["codigo_etiqueta", "descripcion", "reserva__vuelo__numero"]
    ordering_fields = ["peso_kg", "fecha_registro", "estado"]
    ordering        = ["-fecha_registro"]
    pagination_class = StandardPagination

    def get_queryset(self):
        user = self.request.user
        qs = Equipaje.objects.select_related(
            "reserva", "reserva__vuelo", "reserva__pasajero"
        )
        # Un usuario normal solo ve su propio equipaje
        if not user.is_staff:
            qs = qs.filter(reserva__pasajero__email=user.email)
        return qs

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EquipajeReadSerializer
        return EquipajeWriteSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["get"], url_path="perdidos")
    def perdidos(self, request):
        """GET /api/equipajes/perdidos/ — equipaje con estado perdido o dañado."""
        qs = self.get_queryset().filter(estado__in=["perdido", "dañado"])
        serializer = EquipajeReadSerializer(qs, many=True)
        return Response(serializer.data)
