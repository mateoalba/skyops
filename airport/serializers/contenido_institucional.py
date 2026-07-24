from rest_framework import serializers
from airport.models.contenido_institucional import ContenidoInstitucional


class ContenidoInstitucionalSerializer(serializers.ModelSerializer):
    # Igual que BannerPromocionalSerializer.imagen_url: prioriza el archivo
    # subido ('imagen') y si no hay, cae al link manual guardado en el
    # campo 'imagen_url' del modelo.
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = ContenidoInstitucional
        fields = ["clave", "titulo", "texto", "items", "imagen_url", "actualizado_en"]
        read_only_fields = ["actualizado_en"]

    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get("request")
            url = obj.imagen.url
            return request.build_absolute_uri(url) if request else url
        return obj.imagen_url or None
