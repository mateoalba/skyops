from django.urls import path, include
from rest_framework.routers import DefaultRouter
from airport.views import (
    AerolineaViewSet, AeropuertoViewSet, AeronaveViewSet,
    PuertaViewSet, VueloViewSet, PasajeroViewSet,
    ReservaViewSet, TripulanteViewSet, AsignacionTripulacionViewSet,
    IncidenteViewSet, TerminalViewSet, PistaAterrizajeViewSet, 
    AsignacionPistaViewSet, HorarioVueloViewSet, health_check,
    LoginView, RefreshTokenView, RegistroView,
    logout_view, PerfilView, cambiar_password,
)

router = DefaultRouter()
router.register("aerolineas", AerolineaViewSet, basename="aerolinea")
router.register("aeropuertos", AeropuertoViewSet, basename="aeropuerto")
router.register("aeronaves", AeronaveViewSet, basename="aeronave")
router.register("puertas", PuertaViewSet, basename="puerta")
router.register("vuelos", VueloViewSet, basename="vuelo")
router.register("pasajeros", PasajeroViewSet, basename="pasajero")
router.register("reservas", ReservaViewSet, basename="reserva")
router.register("tripulantes", TripulanteViewSet, basename="tripulante")
router.register("asignaciones", AsignacionTripulacionViewSet, basename="asignacion")
router.register("incidentes", IncidenteViewSet, basename="incidente")
router.register("terminales", TerminalViewSet, basename="terminal")
router.register("pistas", PistaAterrizajeViewSet, basename="pista")
router.register("asignaciones-pista", AsignacionPistaViewSet, basename="asignacion-pista")
router.register("horarios", HorarioVueloViewSet, basename="horario")


auth_urlpatterns = [
    path("login/",            LoginView.as_view(),        name="auth-login"),
    path("refresh/",          RefreshTokenView.as_view(), name="auth-refresh"),
    path("registro/",         RegistroView.as_view(),     name="auth-registro"),
    path("logout/",           logout_view,                name="auth-logout"),
    path("perfil/",           PerfilView.as_view(),       name="auth-perfil"),
    path("cambiar-password/", cambiar_password,           name="auth-cambiar-password"),
]

urlpatterns = [
    path("health/", health_check, name="health"),
    path("auth/", include(auth_urlpatterns)),
    path("", include(router.urls)),
]