from rest_framework import serializers
from airport.models import TipoAeronave


class TipoAeronaveReadSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source="get_categoria_display", read_only=True)
    total_aeronaves   = serializers.SerializerMethodField()

    class Meta:
        model = TipoAeronave
        fields = [
            "id",
            "fabricante",
            "modelo",
            "codigo_iata",
            "categoria",
            "categoria_display",
            "capacidad_pasajeros_min",
            "capacidad_pasajeros_max",
            "autonomia_km",
            "velocidad_crucero_kmh",
            "descripcion",
            "en_produccion",
            "total_aeronaves",
        ]

    def get_total_aeronaves(self, obj):
        return obj.aeronaves.count()


class TipoAeronaveWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAeronave
        fields = [
            "fabricante",
            "modelo",
            "codigo_iata",
            "categoria",
            "capacidad_pasajeros_min",
            "capacidad_pasajeros_max",
            "autonomia_km",
            "velocidad_crucero_kmh",
            "descripcion",
            "en_produccion",
        ]

    def validate(self, attrs):
        cap_min = attrs.get("capacidad_pasajeros_min")
        cap_max = attrs.get("capacidad_pasajeros_max")
        if cap_min and cap_max and cap_max < cap_min:
            raise serializers.ValidationError(
                {"capacidad_pasajeros_max": "La capacidad máxima no puede ser menor a la mínima."}
            )

        fabricante = attrs.get("fabricante", "").strip()
        modelo     = attrs.get("modelo", "").strip()
        qs = TipoAeronave.objects.filter(fabricante__iexact=fabricante, modelo__iexact=modelo)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                {"modelo": f"Ya existe el tipo '{fabricante} {modelo}'."}
            )
        return attrs
