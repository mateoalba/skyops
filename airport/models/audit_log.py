import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class AuditLog(models.Model):

    class Accion(models.TextChoices):
        CREAR = "crear", "Crear"
        EDITAR = "editar", "Editar"
        ELIMINAR = "eliminar", "Eliminar"
        VER = "ver", "Ver"
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        CAMBIO_ESTADO = "cambio_estado", "Cambio de estado"
        EXPORTAR = "exportar", "Exportar"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    accion = models.CharField(max_length=20, choices=Accion.choices)
    content_type = models.ForeignKey(
        ContentType, null=True, blank=True, on_delete=models.SET_NULL
    )
    object_id = models.CharField(max_length=100, blank=True)
    objeto = GenericForeignKey("content_type", "object_id")
    descripcion = models.TextField(blank=True)
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_log"
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Registros de auditoría"
        ordering = ["-fecha_hora"]

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} ({self.fecha_hora})"
