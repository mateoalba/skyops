from rest_framework import serializers
from airport.models import CategoriaPasajero, Pasajero


class CategoriaPasajeroReadSerializer(serializers.ModelSerializer):
    tipo_display    = serializers.CharField(source="get_tipo_display", read_only=True)
    total_pasajeros = serializers.SerializerMethodField()

    class Meta:
        model = CategoriaPasajero
        fields = [
            "id",
            "nombre",
            "tipo",
            "tipo_display",
            "descripcion",
            "requiere_asistencia",
            "beneficios",
            "activa",
            "total_pasajeros",
        ]

    def get_total_pasajeros(self, obj):
        return obj.pasajeros.count()


class CategoriaPasajeroWriteSerializer(serializers.ModelSerializer):
    # Permite asignar/desasignar pasajeros al crear o actualizar
    pasajeros = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Pasajero.objects.all(),
        required=False,
    )

    class Meta:
        model = CategoriaPasajero
        fields = [
            "nombre",
            "tipo",
            "descripcion",
            "requiere_asistencia",
            "beneficios",
            "activa",
            "pasajeros",
        ]

    def validate_nombre(self, value):
        value = value.strip()
        qs = CategoriaPasajero.objects.filter(nombre__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(f"Ya existe una categoría con el nombre '{value}'.")
        return value

    def create(self, validated_data):
        pasajeros = validated_data.pop("pasajeros", [])
        categoria = CategoriaPasajero.objects.create(**validated_data)
        categoria.pasajeros.set(pasajeros)
        return categoria

    def update(self, instance, validated_data):
        pasajeros = validated_data.pop("pasajeros", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if pasajeros is not None:
            instance.pasajeros.set(pasajeros)
        return instance
