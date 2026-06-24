from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from airport.models.mantenimiento_aeronave import MantenimientoAeronave
from airport.serializers.mantenimiento_aeronave import MantenimientoAeronaveSerializer
from airport.permissions import EsAdmin, EsOperador


class MantenimientoAeronaveViewSet(viewsets.ModelViewSet):
    queryset = MantenimientoAeronave.objects.select_related(
        "aeronave", "aeronave__aerolinea", "aeropuerto"
    ).all()
    serializer_class = MantenimientoAeronaveSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["aeronave__matricula", "tecnico_responsable", "descripcion"]
    ordering_fields = ["fecha_inicio", "estado", "tipo"]
    ordering = ["fecha_inicio"]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "activos"]:
            return [EsOperador()]
        return [EsAdmin()]

    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        """PATCH /api/mantenimientos/{id}/cambiar-estado/"""
        mantenimiento = self.get_object()
        nuevo_estado = request.data.get("estado")
        estados_validos = [e[0] for e in MantenimientoAeronave.Estado.choices]
        if nuevo_estado not in estados_validos:
            return Response(
                {"error": f"Estado inválido. Opciones: {estados_validos}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        mantenimiento.estado = nuevo_estado
        mantenimiento.save()
        return Response(self.get_serializer(mantenimiento).data)

    @action(detail=False, methods=["get"], url_path="activos")
    def activos(self, request):
        """GET /api/mantenimientos/activos/"""
        qs = self.get_queryset().filter(
            estado__in=["programado", "en_progreso"]
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(qs, many=True).data)
