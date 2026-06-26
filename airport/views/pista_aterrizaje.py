from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import PistaAterrizaje
from airport.serializers import PistaAterrizajeSerializer
from airport.permissions import EsUsuarioOAdmin


class PistaAterrizajeViewSet(viewsets.ModelViewSet):
    queryset = PistaAterrizaje.objects.select_related('aeropuerto').all()
    serializer_class = PistaAterrizajeSerializer
    permission_classes = [EsUsuarioOAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'superficie', 'aeropuerto']
    search_fields = ['identificador', 'aeropuerto__nombre']
    ordering_fields = ['identificador', 'longitud_metros', 'estado']
    ordering = ['aeropuerto', 'identificador']