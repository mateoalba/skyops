from rest_framework import serializers
from airport.models.mantenimiento_aeronave import MantenimientoAeronave


class MantenimientoAeronaveSerializer(serializers.ModelSerializer):
    aeronave_matricula = serializers.CharField(
        source="aeronave.matricula", read_only=True
    )
    aeronave_modelo = serializers.CharField(
        source="aeronave.modelo", read_only=True
    )
    aerolinea_nombre = serializers.CharField(
        source="aeronave.aerolinea.nombre", read_only=True
    )
    aeropuerto_codigo = serializers.CharField(
        source="aeropuerto.codigo_iata", read_only=True
    )
    aeropuerto_ciudad = serializers.CharField(
        source="aeropuerto.ciudad", read_only=True
    )
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = MantenimientoAeronave
        fields = [
            "id",
            "aeronave",
            "aeronave_matricula",
            "aeronave_modelo",
            "aerolinea_nombre",
            "aeropuerto",
            "aeropuerto_codigo",
            "aeropuerto_ciudad",
            "tipo",
            "tipo_display",
            "estado",
            "estado_display",
            "descripcion",
            "tecnico_responsable",
            "fecha_inicio",
            "fecha_fin_estimada",
            "fecha_fin_real",
            "costo_estimado",
            "costo_real",
            "horas_fuera_servicio",
            "observaciones",
            "creado_en",
        ]
        read_only_fields = ["id", "creado_en"]

    def validate(self, data):
        fecha_inicio = data.get("fecha_inicio")
        fecha_fin_estimada = data.get("fecha_fin_estimada")
        if fecha_inicio and fecha_fin_estimada and fecha_fin_estimada <= fecha_inicio:
            raise serializers.ValidationError(
                "La fecha de fin estimada debe ser posterior a la fecha de inicio."
            )
        return data
