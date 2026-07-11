from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Puerta
from airport.serializers import PuertaSerializer
from airport.permissions import EsOperador, SoloLectura
from airport.filters import PuertaFilter


class PuertaViewSet(viewsets.ModelViewSet):
    queryset = Puerta.objects.select_related("aeropuerto").all()
    serializer_class = PuertaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PuertaFilter
    search_fields = ["codigo", "terminal"]
    ordering_fields = ["terminal", "codigo"]
    ordering = ["terminal", "codigo"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [SoloLectura()]
        return [EsOperador()]