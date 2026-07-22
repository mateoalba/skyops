import django_filters
from django.db.models import Q
from airport.models import (
    Aerolinea, Aeropuerto, Aeronave, Puerta,
    Vuelo, Pasajero, Reserva, Tripulante, Incidente,
)


class AerolineaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    pais = django_filters.CharFilter(lookup_expr="icontains")
    activa = django_filters.BooleanFilter()

    class Meta:
        model = Aerolinea
        fields = ["nombre", "pais", "activa"]


class AeropuertoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    ciudad = django_filters.CharFilter(lookup_expr="icontains")
    pais = django_filters.CharFilter(lookup_expr="icontains")
    codigo_iata = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Aeropuerto
        fields = ["nombre", "ciudad", "pais", "codigo_iata"]


class AeronaveFilter(django_filters.FilterSet):
    modelo = django_filters.CharFilter(lookup_expr="icontains")
    fabricante = django_filters.CharFilter(lookup_expr="icontains")
    estado = django_filters.ChoiceFilter(choices=Aeronave.Estado.choices)
    aerolinea = django_filters.UUIDFilter(field_name="aerolinea__id")
    capacidad_min = django_filters.NumberFilter(
        field_name="capacidad", lookup_expr="gte"
    )
    capacidad_max = django_filters.NumberFilter(
        field_name="capacidad", lookup_expr="lte"
    )

    class Meta:
        model = Aeronave
        fields = ["modelo", "fabricante", "estado", "aerolinea",
                  "capacidad_min", "capacidad_max"]


class PuertaFilter(django_filters.FilterSet):
    # 'terminal' ahora es una FK real (antes era texto libre con icontains).
    terminal = django_filters.UUIDFilter(field_name="terminal__id")
    terminal_codigo = django_filters.CharFilter(
        field_name="terminal__codigo", lookup_expr="iexact"
    )
    estado = django_filters.ChoiceFilter(choices=Puerta.Estado.choices)
    aeropuerto = django_filters.UUIDFilter(field_name="aeropuerto__id")
    aeropuerto_codigo = django_filters.CharFilter(
        field_name="aeropuerto__codigo_iata", lookup_expr="iexact"
    )

    class Meta:
        model = Puerta
        fields = ["terminal", "terminal_codigo", "estado", "aeropuerto", "aeropuerto_codigo"]


class VueloFilter(django_filters.FilterSet):
    numero_vuelo = django_filters.CharFilter(lookup_expr="icontains")
    estado = django_filters.ChoiceFilter(choices=Vuelo.Estado.choices)
    aerolinea = django_filters.UUIDFilter(field_name="aerolinea__id")
    aerolinea_codigo = django_filters.CharFilter(
        field_name="aerolinea__codigo_iata", lookup_expr="iexact"
    )
    origen = django_filters.UUIDFilter(field_name="origen__id")
    origen_codigo = django_filters.CharFilter(
        field_name="origen__codigo_iata", lookup_expr="iexact"
    )
    destino = django_filters.UUIDFilter(field_name="destino__id")
    destino_codigo = django_filters.CharFilter(
        field_name="destino__codigo_iata", lookup_expr="iexact"
    )
    # Filtros por fecha
    fecha = django_filters.DateFilter(
        field_name="salida_programada", lookup_expr="date"
    )
    fecha_desde = django_filters.DateTimeFilter(
        field_name="salida_programada", lookup_expr="gte"
    )
    fecha_hasta = django_filters.DateTimeFilter(
        field_name="salida_programada", lookup_expr="lte"
    )
    # Filtros por duración
    duracion_min = django_filters.NumberFilter(
        field_name="duracion_min", lookup_expr="gte"
    )
    duracion_max = django_filters.NumberFilter(
        field_name="duracion_min", lookup_expr="lte"
    )
    # Vuelos con retraso (salida real posterior a la programada)
    con_retraso = django_filters.BooleanFilter(method="filtrar_con_retraso")

    class Meta:
        model = Vuelo
        fields = [
            "numero_vuelo", "estado", "aerolinea", "aerolinea_codigo",
            "origen", "origen_codigo", "destino", "destino_codigo",
            "fecha", "fecha_desde", "fecha_hasta",
            "duracion_min", "duracion_max", "con_retraso",
        ]

    def filtrar_con_retraso(self, queryset, name, value):
        if value:
            return queryset.filter(
                salida_real__isnull=False,
                salida_real__gt=django_filters.utils.handle_timezone(
                    self.request
                ) if hasattr(django_filters.utils, 'handle_timezone')
                else queryset.filter(estado="retrasado")
            )
        return queryset.filter(estado="retrasado") if value else queryset


class PasajeroFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    apellido = django_filters.CharFilter(lookup_expr="icontains")
    nacionalidad = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    fecha_nacimiento_desde = django_filters.DateFilter(
        field_name="fecha_nacimiento", lookup_expr="gte"
    )
    fecha_nacimiento_hasta = django_filters.DateFilter(
        field_name="fecha_nacimiento", lookup_expr="lte"
    )

    class Meta:
        model = Pasajero
        fields = ["nombre", "apellido", "nacionalidad", "email",
                  "fecha_nacimiento_desde", "fecha_nacimiento_hasta"]


class ReservaFilter(django_filters.FilterSet):
    codigo_reserva = django_filters.CharFilter(lookup_expr="iexact")
    estado = django_filters.ChoiceFilter(choices=Reserva.Estado.choices)
    clase = django_filters.ChoiceFilter(choices=Reserva.Clase.choices)
    vuelo = django_filters.UUIDFilter(field_name="vuelo__id")
    numero_vuelo = django_filters.CharFilter(
        field_name="vuelo__numero_vuelo", lookup_expr="icontains"
    )
    pasajero = django_filters.UUIDFilter(field_name="pasajero__id")
    origen_codigo = django_filters.CharFilter(
        field_name="vuelo__origen__codigo_iata", lookup_expr="iexact"
    )
    destino_codigo = django_filters.CharFilter(
        field_name="vuelo__destino__codigo_iata", lookup_expr="iexact"
    )
    reservado_desde = django_filters.DateTimeFilter(
        field_name="reservado_en", lookup_expr="gte"
    )
    reservado_hasta = django_filters.DateTimeFilter(
        field_name="reservado_en", lookup_expr="lte"
    )

    class Meta:
        model = Reserva
        fields = [
            "codigo_reserva", "estado", "clase", "vuelo", "numero_vuelo",
            "pasajero", "origen_codigo", "destino_codigo",
            "reservado_desde", "reservado_hasta",
        ]


class TripulanteFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    apellido = django_filters.CharFilter(lookup_expr="icontains")
    rol = django_filters.ChoiceFilter(choices=Tripulante.Rol.choices)
    disponible = django_filters.BooleanFilter()
    aerolinea = django_filters.UUIDFilter(field_name="aerolinea__id")
    aerolinea_codigo = django_filters.CharFilter(
        field_name="aerolinea__codigo_iata", lookup_expr="iexact"
    )

    class Meta:
        model = Tripulante
        fields = ["nombre", "apellido", "rol", "disponible",
                  "aerolinea", "aerolinea_codigo"]


class IncidenteFilter(django_filters.FilterSet):
    tipo = django_filters.ChoiceFilter(choices=Incidente.Tipo.choices)
    severidad = django_filters.ChoiceFilter(choices=Incidente.Severidad.choices)
    estado_resolucion = django_filters.ChoiceFilter(
        choices=Incidente.EstadoResolucion.choices
    )
    vuelo = django_filters.UUIDFilter(field_name="vuelo__id")
    numero_vuelo = django_filters.CharFilter(
        field_name="vuelo__numero_vuelo", lookup_expr="icontains"
    )
    reportado_desde = django_filters.DateTimeFilter(
        field_name="reportado_en", lookup_expr="gte"
    )
    reportado_hasta = django_filters.DateTimeFilter(
        field_name="reportado_en", lookup_expr="lte"
    )
    descripcion = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Incidente
        fields = [
            "tipo", "severidad", "estado_resolucion", "vuelo",
            "numero_vuelo", "reportado_desde", "reportado_hasta", "descripcion",
        ]