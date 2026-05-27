from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Pasajero
from airport.serializers import PasajeroSerializer
from airport.permissions import EsOperador
from airport.filters import PasajeroFilter


class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
    permission_classes = [EsOperador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PasajeroFilter
    search_fields = ["nombre", "apellido", "num_pasaporte", "email"]
    ordering_fields = ["apellido", "nombre"]
    ordering = ["apellido", "nombre"]