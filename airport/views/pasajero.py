from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Pasajero
from airport.serializers import PasajeroSerializer
from airport.permissions import EsOperador
from airport.filters import PasajeroFilter


class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PasajeroFilter
    search_fields = ["nombre", "apellido", "num_pasaporte", "email"]
    ordering_fields = ["apellido", "nombre"]
    ordering = ["apellido", "nombre"]

    def get_permissions(self):
        # Cualquier usuario autenticado puede ver pasajeros (list/retrieve
        # queda filtrado a su propio registro en get_queryset). Crear,
        # editar o eliminar pasajeros de otra persona sigue siendo solo
        # para Operador/Admin.
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [EsOperador()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name="Operadores").exists():
            return Pasajero.objects.all()
        return Pasajero.objects.filter(email=user.email)