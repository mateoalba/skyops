from datetime import date
from rest_framework import serializers
from airport.models.certificacion_tripulante import CertificacionTripulante


class CertificacionTripulanteSerializer(serializers.ModelSerializer):
    tripulante_nombre = serializers.SerializerMethodField()
    tripulante_rol = serializers.CharField(
        source="tripulante.get_rol_display", read_only=True
    )
    aerolinea_nombre = serializers.CharField(
        source="tripulante.aerolinea.nombre", read_only=True
    )
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    dias_para_vencer = serializers.SerializerMethodField()

    class Meta:
        model = CertificacionTripulante
        fields = [
            "id",
            "tripulante",
            "tripulante_nombre",
            "tripulante_rol",
            "aerolinea_nombre",
            "tipo_aeronave_habilitado",
            "tipo",
            "tipo_display",
            "estado",
            "estado_display",
            "numero_certificado",
            "entidad_emisora",
            "fecha_emision",
            "fecha_vencimiento",
            "dias_para_vencer",
            "observaciones",
            "creado_en",
        ]
        read_only_fields = ["id", "creado_en"]

    def get_tripulante_nombre(self, obj):
        return f"{obj.tripulante.nombre} {obj.tripulante.apellido}"

    def get_dias_para_vencer(self, obj):
        return (obj.fecha_vencimiento - date.today()).days

    def validate(self, data):
        tipo = data.get("tipo")
        tipo_aeronave = (data.get("tipo_aeronave_habilitado") or "").strip()
        if tipo == "habilitacion_tipo" and not tipo_aeronave:
            raise serializers.ValidationError(
                {"tipo_aeronave_habilitado": "Este campo es requerido para certificaciones de habilitación de tipo."}
            )
        fecha_emision = data.get("fecha_emision")
        fecha_vencimiento = data.get("fecha_vencimiento")
        if fecha_emision and fecha_vencimiento and fecha_vencimiento <= fecha_emision:
            raise serializers.ValidationError(
                "La fecha de vencimiento debe ser posterior a la fecha de emisión."
            )
        return data
