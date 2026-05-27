from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Aerolinea
from airport.serializers import AerolineaSerializer
from airport.permissions import EsOperador
from airport.filters import AerolineaFilter


class AerolineaViewSet(viewsets.ModelViewSet):
    queryset = Aerolinea.objects.all()
    serializer_class = AerolineaSerializer
    permission_classes = [EsOperador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AerolineaFilter
    search_fields = ["nombre", "codigo_iata", "pais"]
    ordering_fields = ["nombre", "creado_en"]
    ordering = ["nombre"]