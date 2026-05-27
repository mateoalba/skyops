from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Puerta
from airport.serializers import PuertaSerializer
from airport.permissions import EsOperador
from airport.filters import PuertaFilter


class PuertaViewSet(viewsets.ModelViewSet):
    queryset = Puerta.objects.select_related("aeropuerto").all()
    serializer_class = PuertaSerializer
    permission_classes = [EsOperador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PuertaFilter
    search_fields = ["codigo", "terminal"]
    ordering_fields = ["terminal", "codigo"]
    ordering = ["terminal", "codigo"]