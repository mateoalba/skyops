from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Terminal
from airport.serializers import TerminalSerializer
from airport.permissions import EsUsuarioOAdmin


class TerminalViewSet(viewsets.ModelViewSet):
    queryset = Terminal.objects.select_related('aeropuerto').all()
    serializer_class = TerminalSerializer
    permission_classes = [EsUsuarioOAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'aeropuerto']
    search_fields = ['nombre', 'codigo', 'aeropuerto__nombre']
    ordering_fields = ['nombre', 'codigo', 'estado']
    ordering = ['aeropuerto', 'codigo']