from django.contrib.auth.models import User
from rest_framework import serializers
from airport.models import Pasajero


class PasajeroSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    total_reservas = serializers.SerializerMethodField()
    # Un Pasajero no tiene FK a User (el vínculo real, usado en todo el
    # backend para autoreserva, es por email — ver PasajeroViewSet.get_queryset
    # y ReservaSerializer.validate). Acá se usa ese mismo email para mostrar
    # la foto de perfil real que el usuario ya subió en su cuenta, sin
    # inventar ni permitir subir una foto aparte desde este formulario.
    foto_resuelta = serializers.SerializerMethodField()

    class Meta:
        model = Pasajero
        fields = [
            "id",
            "nombre",
            "apellido",
            "nombre_completo",
            "num_pasaporte",
            "nacionalidad",
            "fecha_nacimiento",
            "email",
            "telefono",
            "total_reservas",
            "foto_resuelta",
        ]
        read_only_fields = ["id"]

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"

    def get_total_reservas(self, obj):
        return obj.reservas.count()

    def get_foto_resuelta(self, obj):
        if not obj.email:
            return None
        user = User.objects.filter(email=obj.email).select_related("perfil").first()
        perfil = getattr(user, "perfil", None) if user else None
        if not perfil:
            return None
        if perfil.foto:
            request = self.context.get("request")
            url = perfil.foto.url
            return request.build_absolute_uri(url) if request else url
        return perfil.foto_url or None
