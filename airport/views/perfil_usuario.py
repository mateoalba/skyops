from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from airport.models.perfil_usuario import PerfilUsuario
from airport.serializers.perfil_usuario import PerfilUsuarioSerializer
from airport.permissions import EsAdmin, EsOperador


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.select_related(
        "usuario", "aeropuerto_asignado"
    ).all()
    serializer_class = PerfilUsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "numero_documento",
    ]
    ordering_fields = ["cargo", "creado_en"]
    ordering = ["usuario__username"]

    def get_permissions(self):
        if self.action == "mi_perfil":
            return [IsAuthenticated()]
        if self.action in ["list", "retrieve"]:
            return [EsOperador()]
        return [EsAdmin()]

    @action(detail=False, methods=["get"], url_path="mi-perfil")
    def mi_perfil(self, request):
        try:
            perfil = PerfilUsuario.objects.select_related(
                "usuario", "aeropuerto_asignado"
            ).get(usuario=request.user)
        except PerfilUsuario.DoesNotExist:
            raise NotFound()
        serializer = self.get_serializer(perfil)
        return Response(serializer.data)
