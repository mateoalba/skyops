from datetime import date, timedelta
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from airport.models.certificacion_tripulante import CertificacionTripulante
from airport.serializers.certificacion_tripulante import CertificacionTripulanteSerializer
from airport.permissions import EsAdmin, EsOperador


class CertificacionTripulanteViewSet(viewsets.ModelViewSet):
    queryset = CertificacionTripulante.objects.select_related(
        "tripulante", "tripulante__aerolinea"
    ).all()
    serializer_class = CertificacionTripulanteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "tripulante__nombre",
        "tripulante__apellido",
        "numero_certificado",
        "entidad_emisora",
    ]
    ordering_fields = ["fecha_vencimiento", "tipo", "estado"]
    ordering = ["fecha_vencimiento"]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "por_vencer"]:
            return [EsOperador()]
        return [EsAdmin()]

    @action(detail=False, methods=["get"], url_path="por-vencer")
    def por_vencer(self, request):
        """GET /api/certificaciones/por-vencer/?dias=30"""
        dias = int(request.query_params.get("dias", 30))
        limite = date.today() + timedelta(days=dias)
        qs = self.get_queryset().filter(
            fecha_vencimiento__lte=limite,
            estado__in=["vigente", "por_vencer"],
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(qs, many=True).data)
