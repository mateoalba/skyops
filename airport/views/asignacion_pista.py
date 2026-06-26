from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import AsignacionPista
from airport.serializers import AsignacionPistaSerializer
from airport.permissions import EsUsuarioOAdmin


class AsignacionPistaViewSet(viewsets.ModelViewSet):
    queryset = AsignacionPista.objects.select_related('vuelo', 'pista').all()
    serializer_class = AsignacionPistaSerializer
    permission_classes = [EsUsuarioOAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_operacion', 'vuelo', 'pista']
    search_fields = ['vuelo__numero_vuelo', 'pista__identificador']
    ordering_fields = ['hora_inicio', 'hora_fin', 'tipo_operacion']
    ordering = ['hora_inicio']