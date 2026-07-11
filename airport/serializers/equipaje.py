from rest_framework import serializers
from airport.models import Equipaje


class EquipajeReadSerializer(serializers.ModelSerializer):
    tipo_display   = serializers.CharField(source="get_tipo_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    pasajero_nombre = serializers.SerializerMethodField()
    vuelo_numero    = serializers.SerializerMethodField()

    class Meta:
        model = Equipaje
        fields = [
            "id",
            "reserva",
            "pasajero_nombre",
            "vuelo_numero",
            "tipo",
            "tipo_display",
            "peso_kg",
            "descripcion",
            "codigo_etiqueta",
            "estado",
            "estado_display",
            "costo_adicional",
            "fecha_registro",
        ]

    def get_pasajero_nombre(self, obj):
        p = obj.reserva.pasajero
        return f"{p.nombre} {p.apellido}"

    def get_vuelo_numero(self, obj):
        return obj.reserva.vuelo.numero_vuelo


class EquipajeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipaje
        fields = [
            "reserva",
            "tipo",
            "peso_kg",
            "descripcion",
            "codigo_etiqueta",
            "estado",
            "costo_adicional",
        ]

    def validate_peso_kg(self, value):
        if value <= 0:
            raise serializers.ValidationError("El peso debe ser mayor a 0 kg.")
        if value > 500:
            raise serializers.ValidationError("El peso no puede superar los 500 kg.")
        return value

    def validate_codigo_etiqueta(self, value):
        value = value.upper().strip()
        qs = Equipaje.objects.filter(codigo_etiqueta=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(f"El código de etiqueta '{value}' ya está en uso.")
        return value

    def validate(self, attrs):
        tipo    = attrs.get("tipo")
        peso_kg = attrs.get("peso_kg", 0)
        # Equipaje de mano: máximo 10 kg
        if tipo == "mano" and peso_kg > 10:
            raise serializers.ValidationError(
                {"peso_kg": "El equipaje de mano no puede superar los 10 kg."}
            )
        return attrs
