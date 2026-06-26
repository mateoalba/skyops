from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import HorarioVuelo
from airport.serializers import HorarioVueloSerializer
from airport.permissions import EsUsuarioOAdmin


class HorarioVueloViewSet(viewsets.ModelViewSet):
    queryset = HorarioVuelo.objects.select_related(
        'aerolinea', 'origen', 'destino'
    ).all()
    serializer_class = HorarioVueloSerializer
    permission_classes = [EsUsuarioOAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activo', 'aerolinea', 'origen', 'destino']
    search_fields = ['numero_vuelo_base', 'aerolinea__nombre', 'origen__codigo_iata', 'destino__codigo_iata']
    ordering_fields = ['hora_salida', 'numero_vuelo_base']
    ordering = ['hora_salida']