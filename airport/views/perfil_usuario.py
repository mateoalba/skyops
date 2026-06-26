from rest_framework import viewsets, filters
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
        if self.action in ["list", "retrieve"]:
            return [EsOperador()]
        return [EsAdmin()]
