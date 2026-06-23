from rest_framework import serializers
from airport.models.perfil_usuario import PerfilUsuario


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)
    email = serializers.EmailField(source="usuario.email", read_only=True)
    nombre_completo = serializers.SerializerMethodField()
    aeropuerto_codigo = serializers.CharField(
        source="aeropuerto_asignado.codigo_iata", read_only=True, default=None
    )
    aeropuerto_ciudad = serializers.CharField(
        source="aeropuerto_asignado.ciudad", read_only=True
    )
    tipo_documento_display = serializers.CharField(
        source="get_tipo_documento_display", read_only=True
    )
    cargo_display = serializers.CharField(source="get_cargo_display", read_only=True)

    class Meta:
        model = PerfilUsuario
        fields = [
            "id",
            "usuario",
            "username",
            "email",
            "nombre_completo",
            "aeropuerto_asignado",
            "aeropuerto_codigo",
            "aeropuerto_ciudad",
            "tipo_documento",
            "tipo_documento_display",
            "numero_documento",
            "telefono",
            "cargo",
            "cargo_display",
            "foto_url",
            "activo",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ["id", "creado_en", "actualizado_en"]

    def get_nombre_completo(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip()

    def validate_numero_documento(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "El número de documento debe tener al menos 8 caracteres."
            )
        return value
