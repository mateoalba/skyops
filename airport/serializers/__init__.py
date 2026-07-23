from .aerolinea import AerolineaSerializer
from .aeropuerto import AeropuertoSerializer
from .aeronave import AeronaveSerializer
from .puerta import PuertaSerializer
from .vuelo import VueloSerializer
from .pasajero import PasajeroSerializer
from .reserva import ReservaSerializer
from .tripulante import TripulanteSerializer
from .asignacion_tripulacion import AsignacionTripulacionSerializer
from .incidente import IncidenteSerializer
from .terminal import TerminalSerializer
from .pista_aterrizaje import PistaAterrizajeSerializer
from .asignacion_pista import AsignacionPistaSerializer
from .horario_vuelo import HorarioVueloSerializer
from .escala_vuelo import EscalaVueloSerializer
from .tipo_aeronave import TipoAeronaveReadSerializer, TipoAeronaveWriteSerializer
from .equipaje import EquipajeReadSerializer, EquipajeWriteSerializer
from .tarjeta_embarque import TarjetaEmbarqueReadSerializer, TarjetaEmbarqueWriteSerializer
from .categoria_pasajero import CategoriaPasajeroReadSerializer, CategoriaPasajeroWriteSerializer
from .notificacion import NotificacionReadSerializer, NotificacionWriteSerializer
from .auth import (
    CustomTokenObtainPairSerializer,
    RegistroUsuarioSerializer,
    PerfilUsuarioSerializer,
    CambiarPasswordSerializer,
)
from .banner_promocional import BannerPromocionalSerializer
from .contenido_institucional import ContenidoInstitucionalSerializer

__all__ = [
    "AerolineaSerializer",
    "AeropuertoSerializer",
    "AeronaveSerializer",
    "PuertaSerializer",
    "VueloSerializer",
    "PasajeroSerializer",
    "ReservaSerializer",
    "TripulanteSerializer",
    "AsignacionTripulacionSerializer",
    "IncidenteSerializer",
    "TerminalSerializer",
    "PistaAterrizajeSerializer",
    "AsignacionPistaSerializer",
    "HorarioVueloSerializer",
    "EscalaVueloSerializer",
    "TipoAeronaveReadSerializer",
    "TipoAeronaveWriteSerializer",
    "EquipajeReadSerializer",
    "EquipajeWriteSerializer",
    "TarjetaEmbarqueReadSerializer",
    "TarjetaEmbarqueWriteSerializer",
    "CategoriaPasajeroReadSerializer",
    "CategoriaPasajeroWriteSerializer",
    "NotificacionReadSerializer",
    "NotificacionWriteSerializer",
    "CustomTokenObtainPairSerializer",
    "RegistroUsuarioSerializer",
    "PerfilUsuarioSerializer",
    "CambiarPasswordSerializer",
    "BannerPromocionalSerializer",
    "ContenidoInstitucionalSerializer",
]