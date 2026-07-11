from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from airport.models.perfil_usuario import PerfilUsuario


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Agrega datos del usuario al token JWT."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["usuario"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "nombre": self.user.first_name,
            "apellido": self.user.last_name,
            "es_staff": self.user.is_staff,
        }
        return data


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    """
    Registro público. Crea el User de Django y, en la misma transacción, un
    PerfilUsuario (cargo='usuario' por defecto) con los datos personales que
    pide el formulario de la app: país, tipo/número de documento, fecha de
    nacimiento, género y teléfono. Todos los campos de perfil son opcionales
    para no romper integraciones que solo mandan username/email/password.
    """

    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label="Confirmar contraseña")

    # Datos de perfil (no son campos del modelo User; se guardan en PerfilUsuario)
    pais = serializers.CharField(required=False, allow_blank=True, default="")
    tipo_documento = serializers.ChoiceField(
        choices=PerfilUsuario.TipoDocumento.choices, required=False, allow_blank=True, default=""
    )
    numero_documento = serializers.CharField(required=False, allow_blank=True, allow_null=True, default=None)
    fecha_nacimiento = serializers.DateField(required=False, allow_null=True, default=None)
    genero = serializers.ChoiceField(
        choices=PerfilUsuario.Genero.choices, required=False, allow_blank=True, default=""
    )
    telefono = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "pais",
            "tipo_documento",
            "numero_documento",
            "fecha_nacimiento",
            "genero",
            "telefono",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden."}
            )
        numero_documento = data.get("numero_documento")
        if numero_documento:
            if PerfilUsuario.objects.filter(numero_documento=numero_documento).exists():
                raise serializers.ValidationError(
                    {"numero_documento": "Ya existe una cuenta registrada con ese número de documento."}
                )
        return data

    @transaction.atomic
    def create(self, validated_data):
        perfil_data = {
            "pais": validated_data.pop("pais", "") or "",
            "tipo_documento": validated_data.pop("tipo_documento", "") or PerfilUsuario.TipoDocumento.CEDULA,
            "numero_documento": validated_data.pop("numero_documento", None) or None,
            "fecha_nacimiento": validated_data.pop("fecha_nacimiento", None),
            "genero": validated_data.pop("genero", "") or "",
            "telefono": validated_data.pop("telefono", "") or "",
        }
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            password=validated_data["password"],
        )
        PerfilUsuario.objects.create(
            usuario=user,
            cargo=PerfilUsuario.Cargo.USUARIO,
            **perfil_data,
        )
        return user


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    """Serializer de /auth/perfil/ — datos de sesión del usuario autenticado."""

    pais = serializers.SerializerMethodField()
    tipo_documento = serializers.SerializerMethodField()
    numero_documento = serializers.SerializerMethodField()
    fecha_nacimiento = serializers.SerializerMethodField()
    genero = serializers.SerializerMethodField()
    telefono = serializers.SerializerMethodField()
    cargo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "date_joined",
            "pais",
            "tipo_documento",
            "numero_documento",
            "fecha_nacimiento",
            "genero",
            "telefono",
            "cargo",
        ]
        read_only_fields = ["id", "is_staff", "date_joined"]

    def _perfil(self, obj):
        return getattr(obj, "perfil", None)

    def get_pais(self, obj):
        p = self._perfil(obj)
        return p.pais if p else ""

    def get_tipo_documento(self, obj):
        p = self._perfil(obj)
        return p.tipo_documento if p else ""

    def get_numero_documento(self, obj):
        p = self._perfil(obj)
        return p.numero_documento if p else None

    def get_fecha_nacimiento(self, obj):
        p = self._perfil(obj)
        return p.fecha_nacimiento if p else None

    def get_genero(self, obj):
        p = self._perfil(obj)
        return p.genero if p else ""

    def get_telefono(self, obj):
        p = self._perfil(obj)
        return p.telefono if p else ""

    def get_cargo(self, obj):
        p = self._perfil(obj)
        return p.cargo if p else ""


class CambiarPasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(write_only=True)
    password_nuevo = serializers.CharField(write_only=True, min_length=8)
    password_nuevo2 = serializers.CharField(write_only=True, label="Confirmar nueva contraseña")

    def validate(self, data):
        if data["password_nuevo"] != data["password_nuevo2"]:
            raise serializers.ValidationError(
                {"password_nuevo2": "Las contraseñas nuevas no coinciden."}
            )
        return data

    def validate_password_actual(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["password_nuevo"])
        user.save()
        return user
