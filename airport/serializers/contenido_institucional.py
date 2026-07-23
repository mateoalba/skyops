from rest_framework import serializers
from airport.models.contenido_institucional import ContenidoInstitucional


class ContenidoInstitucionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoInstitucional
        fields = ["clave", "titulo", "texto", "items", "actualizado_en"]
        read_only_fields = ["actualizado_en"]
