from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import AsignacionTripulacion
from airport.serializers import AsignacionTripulacionSerializer
from airport.permissions import EsOperador


class AsignacionTripulacionViewSet(viewsets.ModelViewSet):
    queryset = AsignacionTripulacion.objects.select_related("vuelo", "tripulante").all()
    serializer_class = AsignacionTripulacionSerializer
    permission_classes = [EsOperador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["vuelo", "tripulante"]
    search_fields = ["rol_asignado", "tripulante__nombre", "tripulante__apellido"]
    ordering_fields = ["vuelo__salida_programada"]
    ordering = ["vuelo__salida_programada"]