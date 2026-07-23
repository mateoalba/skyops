from django.urls import path, include
from rest_framework.routers import DefaultRouter
from airport.views import (
    AerolineaViewSet, AeropuertoViewSet, AeronaveViewSet,
    PuertaViewSet, VueloViewSet, PasajeroViewSet,
    ReservaViewSet, TripulanteViewSet, AsignacionTripulacionViewSet,
    IncidenteViewSet, TerminalViewSet, PistaAterrizajeViewSet,
    AsignacionPistaViewSet, HorarioVueloViewSet, EscalaVueloViewSet,
    TipoAeronaveViewSet, EquipajeViewSet, TarjetaEmbarqueViewSet,
    CategoriaPasajeroViewSet, NotificacionViewSet, health_check,
    LoginView, RefreshTokenView, RegistroView,
    logout_view, PerfilView, cambiar_password, google_login,
    PerfilUsuarioViewSet, SesionUsuarioViewSet, AuditLogViewSet,
    MantenimientoAeronaveViewSet, CertificacionTripulanteViewSet,
    BannerPromocionalViewSet, ContenidoInstitucionalViewSet,
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
router.register("escalas", EscalaVueloViewSet, basename="escala")
router.register("tipos-aeronave", TipoAeronaveViewSet, basename="tipo-aeronave")
router.register("equipajes", EquipajeViewSet, basename="equipaje")
router.register("tarjetas-embarque", TarjetaEmbarqueViewSet, basename="tarjeta-embarque")
router.register("categorias-pasajero", CategoriaPasajeroViewSet, basename="categoria-pasajero")
router.register("notificaciones", NotificacionViewSet, basename="notificacion")
router.register("perfiles-usuario", PerfilUsuarioViewSet, basename="perfil-usuario")
router.register("sesiones-usuario", SesionUsuarioViewSet, basename="sesion-usuario")
router.register("audit-log", AuditLogViewSet, basename="audit-log")
router.register("mantenimientos", MantenimientoAeronaveViewSet, basename="mantenimiento")
router.register("certificaciones", CertificacionTripulanteViewSet, basename="certificacion")
router.register("banners", BannerPromocionalViewSet, basename="banner")
router.register("contenido-institucional", ContenidoInstitucionalViewSet, basename="contenido-institucional")

auth_urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
    path("registro/", RegistroView.as_view(), name="auth-registro"),
    path("logout/", logout_view, name="auth-logout"),
    path("perfil/", PerfilView.as_view(), name="auth-perfil"),
    path("cambiar-password/", cambiar_password, name="auth-cambiar-password"),
    path("google/", google_login, name="auth-google"),
]

urlpatterns = [
    path("health/", health_check, name="health"),
    path("auth/", include(auth_urlpatterns)),
    path("", include(router.urls)),
]