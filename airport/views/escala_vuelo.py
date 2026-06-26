from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import EscalaVuelo
from airport.serializers import EscalaVueloSerializer
from airport.permissions import EsUsuarioOAdmin


class EscalaVueloViewSet(viewsets.ModelViewSet):
    queryset = EscalaVuelo.objects.select_related(
        'vuelo', 'aeropuerto_escala'
    ).all()
    serializer_class = EscalaVueloSerializer
    permission_classes = [EsUsuarioOAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vuelo', 'aeropuerto_escala']
    search_fields = ['vuelo__numero_vuelo', 'aeropuerto_escala__codigo_iata']
    ordering_fields = ['numero_secuencia', 'hora_llegada', 'hora_salida']
    ordering = ['vuelo', 'numero_secuencia']