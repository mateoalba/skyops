from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from airport.models.sesion_usuario import SesionUsuario
from airport.serializers.sesion_usuario import SesionUsuarioSerializer


class SesionUsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SesionUsuario.objects.select_related("usuario").all()
    serializer_class = SesionUsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["usuario__username", "ip_address"]
    ordering_fields = ["fecha_hora", "resultado"]
    ordering = ["-fecha_hora"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return SesionUsuario.objects.select_related("usuario").all()
        return SesionUsuario.objects.select_related("usuario").filter(
            usuario=self.request.user
        )

    @action(detail=False, methods=["get"], url_path="mis-sesiones")
    def mis_sesiones(self, request):
        qs = SesionUsuario.objects.select_related("usuario").filter(usuario=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(qs, many=True).data)
