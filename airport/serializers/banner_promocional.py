from rest_framework import serializers
from airport.models.banner_promocional import BannerPromocional


class BannerPromocionalSerializer(serializers.ModelSerializer):
    # 'imagen_url' sale calculado: prioriza el archivo subido ('imagen',
    # servido desde MEDIA_URL con dominio absoluto) y si no hay, cae al
    # link manual guardado en el campo 'imagen_url' del modelo (compat con
    # banners viejos que solo tenían un link pegado a mano).
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = BannerPromocional
        fields = ["clave", "titulo", "texto", "imagen_url", "actualizado_en"]
        read_only_fields = ["actualizado_en"]

    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get("request")
            url = obj.imagen.url
            return request.build_absolute_uri(url) if request else url
        return obj.imagen_url or None
