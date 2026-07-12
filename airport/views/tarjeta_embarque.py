from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import TarjetaEmbarque
from airport.serializers import TarjetaEmbarqueReadSerializer, TarjetaEmbarqueWriteSerializer
from airport.pagination import StandardPagination


class TarjetaEmbarqueViewSet(viewsets.ModelViewSet):
    """
    CRUD de tarjetas de embarque.
    Endpoint extra: POST /tarjetas/{id}/usar/ — marca la tarjeta como usada.
    """

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["estado", "check_in_online"]
    search_fields   = [
        "asiento", "puerta_embarque",
        "reserva__vuelo__numero",
        "reserva__pasajero__nombre",
        "reserva__pasajero__apellido",
    ]
    ordering_fields = ["fecha_emision", "hora_limite_embarque", "asiento"]
    ordering        = ["-fecha_emision"]
    pagination_class = StandardPagination

    def get_queryset(self):
        user = self.request.user
        qs = TarjetaEmbarque.objects.select_related(
            "reserva", "reserva__vuelo", "reserva__vuelo__aerolinea",
            "reserva__pasajero",
        )
        if not user.is_staff:
            qs = qs.filter(reserva__pasajero__email=user.email)
        return qs

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TarjetaEmbarqueReadSerializer
        return TarjetaEmbarqueWriteSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["post"], url_path="usar")
    def usar(self, request, pk=None):
        """POST /api/tarjetas/{id}/usar/ — marca la tarjeta como usada al embarcar."""
        tarjeta = self.get_object()
        if tarjeta.estado != "generada":
            return Response(
                {"detail": f"La tarjeta está en estado '{tarjeta.estado}' y no puede usarse."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tarjeta.estado = "usada"
        tarjeta.save(update_fields=["estado"])
        return Response({"detail": "Tarjeta marcada como usada."}, status=status.HTTP_200_OK)
