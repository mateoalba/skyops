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
    genero_display = serializers.CharField(
        source="get_genero_display", read_only=True
    )
    cargo_display = serializers.CharField(source="get_cargo_display", read_only=True)
    # Mismo patrón que AeropuertoSerializer.foto_resuelta: prioriza el
    # archivo subido y si no hay, cae al link manual guardado en 'foto_url'.
    foto_resuelta = serializers.SerializerMethodField()

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
            "pais",
            "tipo_documento",
            "tipo_documento_display",
            "numero_documento",
            "fecha_nacimiento",
            "genero",
            "genero_display",
            "telefono",
            "cargo",
            "cargo_display",
            "foto_url",
            "foto",
            "foto_resuelta",
            "activo",
            "creado_en",
            "actualizado_en",
        ]
        read_only_fields = ["id", "creado_en", "actualizado_en"]

    def get_nombre_completo(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip()

    def get_foto_resuelta(self, obj):
        if obj.foto:
            request = self.context.get("request")
            url = obj.foto.url
            return request.build_absolute_uri(url) if request else url
        return obj.foto_url or None

    def validate_numero_documento(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "El número de documento debe tener al menos 8 caracteres."
            )
        return value
