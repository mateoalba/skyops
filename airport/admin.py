from django.contrib import admin
from airport.models import (
    Aerolinea,
    Aeropuerto,
    Aeronave,
    Puerta,
    Vuelo,
    Pasajero,
    Reserva,
    Tripulante,
    AsignacionTripulacion,
    Incidente,
)


@admin.register(Aerolinea)
class AerolineaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "codigo_iata", "pais", "activa", "creado_en"]
    list_filter = ["activa", "pais"]
    search_fields = ["nombre", "codigo_iata"]
    ordering = ["nombre"]


@admin.register(Aeropuerto)
class AeropuertoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "codigo_iata", "ciudad", "pais", "zona_horaria"]
    list_filter = ["pais"]
    search_fields = ["nombre", "codigo_iata", "ciudad"]
    ordering = ["pais", "ciudad"]


@admin.register(Aeronave)
class AeronaveAdmin(admin.ModelAdmin):
    list_display = ["matricula", "modelo", "fabricante", "capacidad", "estado", "aerolinea"]
    list_filter = ["estado", "fabricante", "aerolinea"]
    search_fields = ["matricula", "modelo"]
    ordering = ["matricula"]


@admin.register(Puerta)
class PuertaAdmin(admin.ModelAdmin):
    list_display = ["codigo", "terminal", "estado", "aeropuerto"]
    list_filter = ["estado", "terminal", "aeropuerto"]
    search_fields = ["codigo", "terminal"]
    ordering = ["aeropuerto", "terminal", "codigo"]


@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = [
        "numero_vuelo", "aerolinea", "origen", "destino",
        "salida_programada", "llegada_programada", "estado",
    ]
    list_filter = ["estado", "aerolinea", "origen", "destino"]
    search_fields = ["numero_vuelo"]
    ordering = ["salida_programada"]
    date_hierarchy = "salida_programada"


@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ["nombre", "apellido", "num_pasaporte", "nacionalidad", "email"]
    list_filter = ["nacionalidad"]
    search_fields = ["nombre", "apellido", "num_pasaporte", "email"]
    ordering = ["apellido", "nombre"]


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = [
        "codigo_reserva", "pasajero", "vuelo",
        "numero_asiento", "clase", "estado", "reservado_en",
    ]
    list_filter = ["estado", "clase"]
    search_fields = ["codigo_reserva", "pasajero__nombre", "pasajero__apellido"]
    ordering = ["-reservado_en"]


@admin.register(Tripulante)
class TripulanteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "apellido", "rol", "num_licencia", "disponible", "aerolinea"]
    list_filter = ["rol", "disponible", "aerolinea"]
    search_fields = ["nombre", "apellido", "num_licencia"]
    ordering = ["apellido", "nombre"]


@admin.register(AsignacionTripulacion)
class AsignacionTripulacionAdmin(admin.ModelAdmin):
    list_display = ["vuelo", "tripulante", "rol_asignado"]
    list_filter = ["vuelo", "tripulante"]
    search_fields = ["rol_asignado", "tripulante__nombre", "vuelo__numero_vuelo"]


@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ["vuelo", "tipo", "severidad", "estado_resolucion", "reportado_en"]
    list_filter = ["tipo", "severidad", "estado_resolucion"]
    search_fields = ["descripcion", "vuelo__numero_vuelo"]
    ordering = ["-reportado_en"]