from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Incidente
from airport.serializers import IncidenteSerializer
from airport.permissions import EsOperador
from airport.filters import IncidenteFilter


class IncidenteViewSet(viewsets.ModelViewSet):
    queryset = Incidente.objects.select_related("vuelo").all()
    serializer_class = IncidenteSerializer
    permission_classes = [EsOperador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = IncidenteFilter
    search_fields = ["descripcion", "vuelo__numero_vuelo"]
    ordering_fields = ["reportado_en", "severidad"]
    ordering = ["-reportado_en"]