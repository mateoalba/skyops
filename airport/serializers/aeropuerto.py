from rest_framework import serializers
from airport.models import Aeropuerto


class AeropuertoSerializer(serializers.ModelSerializer):
    total_puertas = serializers.SerializerMethodField()
    # 'foto' se sube como archivo (multipart) y DRF ya la serializa como URL
    # absoluta al leer. 'foto_resuelta' es la que consume el frontend para
    # mostrar la imagen: prioriza el archivo subido y si no hay, cae al
    # link manual guardado en 'foto_url' (compat con aeropuertos viejos que
    # solo tenían un link pegado a mano).
    foto_resuelta = serializers.SerializerMethodField()

    class Meta:
        model = Aeropuerto
        fields = [
            "id",
            "nombre",
            "codigo_iata",
            "ciudad",
            "pais",
            "latitud",
            "longitud",
            "zona_horaria",
            "foto_url",
            "foto",
            "foto_resuelta",
            "total_puertas",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "foto": {"required": False, "allow_null": True},
        }

    def get_total_puertas(self, obj):
        return obj.puertas.count()

    def get_foto_resuelta(self, obj):
        if obj.foto:
            request = self.context.get("request")
            url = obj.foto.url
            return request.build_absolute_uri(url) if request else url
        return obj.foto_url or None
