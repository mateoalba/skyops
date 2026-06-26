import uuid
from django.db import models
from django.contrib.auth.models import User


class SesionUsuario(models.Model):

    class Resultado(models.TextChoices):
        EXITOSO = "exitoso", "Exitoso"
        FALLIDO = "fallido", "Fallido"
        EXPIRADO = "expirado", "Expirado"
        CERRADO = "cerrado", "Cerrado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sesiones",
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    resultado = models.CharField(
        max_length=20, choices=Resultado.choices
    )
    token_jti = models.CharField(max_length=100, blank=True, db_index=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "sesion_usuario"
        verbose_name = "Sesión de usuario"
        verbose_name_plural = "Sesiones de usuario"
        ordering = ["-fecha_hora"]

    def __str__(self):
        return f"{self.usuario} - {self.get_resultado_display()} ({self.fecha_hora})"
