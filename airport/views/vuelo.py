from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Vuelo
from airport.serializers import VueloSerializer
from airport.permissions import EsOperador, SoloLectura
from airport.filters import VueloFilter


class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.select_related(
        "aerolinea", "aeronave", "origen", "destino", "puerta"
    ).all()
    serializer_class = VueloSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VueloFilter
    search_fields = ["numero_vuelo", "origen__codigo_iata", "destino__codigo_iata"]
    ordering_fields = ["salida_programada", "llegada_programada", "numero_vuelo", "duracion_min"]
    ordering = ["salida_programada"]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "por_ruta"]:
            return [SoloLectura()]
        return [EsOperador()]

    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        """PATCH /api/vuelos/{id}/cambiar-estado/"""
        vuelo = self.get_object()
        nuevo_estado = request.data.get("estado")
        estados_validos = [e[0] for e in Vuelo.Estado.choices]
        if nuevo_estado not in estados_validos:
            return Response(
                {"error": f"Estado inválido. Opciones: {estados_validos}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vuelo.estado = nuevo_estado
        vuelo.save()
        return Response(self.get_serializer(vuelo).data)

    @action(detail=False, methods=["get"], url_path="por-ruta")
    def por_ruta(self, request):
        """GET /api/vuelos/por-ruta/?origen=UIO&destino=GYE"""
        origen = request.query_params.get("origen")
        destino = request.query_params.get("destino")
        if not origen or not destino:
            return Response(
                {"error": "Se requieren los parámetros 'origen' y 'destino'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vuelos = self.get_queryset().filter(
            origen__codigo_iata=origen.upper(),
            destino__codigo_iata=destino.upper(),
        )
        return Response(self.get_serializer(vuelos, many=True).data)