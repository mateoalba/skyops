from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from airport.models.audit_log import AuditLog
from airport.serializers.audit_log import AuditLogSerializer
from airport.permissions import EsAdmin


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("usuario", "content_type").all()
    serializer_class = AuditLogSerializer
    permission_classes = [EsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["usuario__username", "descripcion", "object_id"]
    ordering_fields = ["fecha_hora", "accion"]
    ordering = ["-fecha_hora"]
