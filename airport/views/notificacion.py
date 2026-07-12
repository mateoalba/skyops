from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Notificacion
from airport.serializers import NotificacionReadSerializer, NotificacionWriteSerializer
from airport.pagination import StandardPagination


class NotificacionViewSet(viewsets.ModelViewSet):
    """
    CRUD de notificaciones a pasajeros.
    - Pasajeros ven solo sus propias notificaciones.
    Endpoint extra: POST /notificaciones/{id}/marcar-leida/
    """

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["tipo", "canal", "estado", "pasajero", "vuelo"]
    search_fields   = ["asunto", "mensaje", "pasajero__nombre", "pasajero__apellido"]
    ordering_fields = ["creada_en", "fecha_envio", "tipo", "estado"]
    ordering        = ["-creada_en"]
    pagination_class = StandardPagination

    def get_queryset(self):
        user = self.request.user
        qs = Notificacion.objects.select_related("pasajero", "vuelo")
        if not user.is_staff:
            qs = qs.filter(pasajero__email=user.email)
        return qs

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return NotificacionReadSerializer
        return NotificacionWriteSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["post"], url_path="marcar-leida")
    def marcar_leida(self, request, pk=None):
        """POST /api/notificaciones/{id}/marcar-leida/ — el pasajero marca como leída."""
        notificacion = self.get_object()
        if notificacion.estado == "leida":
            return Response({"detail": "Ya está marcada como leída."}, status=status.HTTP_200_OK)
        notificacion.estado       = "leida"
        notificacion.fecha_lectura = timezone.now()
        notificacion.save(update_fields=["estado", "fecha_lectura"])
        return Response({"detail": "Notificación marcada como leída."}, status=status.HTTP_200_OK)
