from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Aeronave
from airport.serializers import AeronaveSerializer
from airport.permissions import EsOperador
from airport.filters import AeronaveFilter


class AeronaveViewSet(viewsets.ModelViewSet):
    queryset = Aeronave.objects.select_related("aerolinea").all()
    serializer_class = AeronaveSerializer
    permission_classes = [EsOperador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AeronaveFilter
    search_fields = ["matricula", "modelo", "fabricante"]
    ordering_fields = ["matricula", "modelo", "capacidad"]
    ordering = ["matricula"]