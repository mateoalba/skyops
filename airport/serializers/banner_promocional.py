from rest_framework import serializers
from airport.models.banner_promocional import BannerPromocional


class BannerPromocionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerPromocional
        fields = ["clave", "titulo", "texto", "imagen_url", "actualizado_en"]
        read_only_fields = ["actualizado_en"]
