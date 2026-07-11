from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Reserva
from airport.serializers import ReservaSerializer
from airport.permissions import EsAdmin, EsPropietarioOAdmin, EsPasajeroOOperador
from airport.filters import ReservaFilter


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReservaFilter
    search_fields = ["codigo_reserva", "pasajero__nombre", "pasajero__apellido", "vuelo__numero_vuelo"]
    ordering_fields = ["reservado_en", "clase"]
    ordering = ["-reservado_en"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name="Operadores").exists():
            return Reserva.objects.select_related(
                "vuelo", "vuelo__origen", "vuelo__destino", "pasajero"
            ).all()
        return Reserva.objects.select_related(
            "vuelo", "vuelo__origen", "vuelo__destino", "pasajero"
        ).filter(pasajero__email=user.email)

    def get_permissions(self):
        if self.action == "destroy":
            return [EsAdmin()]
        if self.action in ["list", "retrieve"]:
            return [EsPropietarioOAdmin()]
        return [EsPasajeroOOperador()]