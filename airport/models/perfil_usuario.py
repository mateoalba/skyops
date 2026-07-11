import uuid
from django.db import models
from django.contrib.auth.models import User
from .aeropuerto import Aeropuerto


class PerfilUsuario(models.Model):

    class TipoDocumento(models.TextChoices):
        CEDULA = "cedula", "Cédula"
        PASAPORTE = "pasaporte", "Pasaporte"
        RUC = "ruc", "RUC"
        DNI = "dni", "DNI"

    class Cargo(models.TextChoices):
        ADMINISTRADOR = "administrador", "Administrador"
        OPERADOR = "operador", "Operador"
        SUPERVISOR = "supervisor", "Supervisor"
        ANALISTA = "analista", "Analista"
        TECNICO = "tecnico", "Técnico"
        USUARIO = "usuario", "Usuario"  # cuentas creadas por auto-registro público

    class Genero(models.TextChoices):
        FEMENINO = "femenino", "Femenino"
        MASCULINO = "masculino", "Masculino"
        PREFIERO_NO_DECIRLO = "prefiero_no_decirlo", "Prefiero no decirlo"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="perfil"
    )
    aeropuerto_asignado = models.ForeignKey(
        Aeropuerto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="perfiles_usuario",
    )
    pais = models.CharField(max_length=100, blank=True, default="")
    tipo_documento = models.CharField(
        max_length=20, choices=TipoDocumento.choices, blank=True, default=TipoDocumento.CEDULA
    )
    numero_documento = models.CharField(max_length=30, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=25, choices=Genero.choices, blank=True, default="")
    telefono = models.CharField(max_length=20, blank=True)
    cargo = models.CharField(max_length=20, choices=Cargo.choices, default=Cargo.USUARIO)
    foto_url = models.URLField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "perfil_usuario"
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"
        ordering = ["usuario__username"]

    def __str__(self):
        return f"{self.usuario.username} - {self.get_cargo_display()}"
