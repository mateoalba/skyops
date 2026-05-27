from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Tripulante
from airport.serializers import TripulanteSerializer
from airport.permissions import EsOperador
from airport.filters import TripulanteFilter


class TripulanteViewSet(viewsets.ModelViewSet):
    queryset = Tripulante.objects.select_related("aerolinea").all()
    serializer_class = TripulanteSerializer
    permission_classes = [EsOperador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TripulanteFilter
    search_fields = ["nombre", "apellido", "num_licencia"]
    ordering_fields = ["apellido", "nombre", "rol"]
    ordering = ["apellido", "nombre"]