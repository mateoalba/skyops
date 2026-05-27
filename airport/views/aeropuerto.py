from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Aeropuerto
from airport.serializers import AeropuertoSerializer
from airport.permissions import EsOperador
from airport.filters import AeropuertoFilter


class AeropuertoViewSet(viewsets.ModelViewSet):
    queryset = Aeropuerto.objects.all()
    serializer_class = AeropuertoSerializer
    permission_classes = [EsOperador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AeropuertoFilter
    search_fields = ["nombre", "codigo_iata", "ciudad", "pais"]
    ordering_fields = ["nombre", "ciudad", "pais"]
    ordering = ["pais", "ciudad"]