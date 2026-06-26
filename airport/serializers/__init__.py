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
from .auth import (
    CustomTokenObtainPairSerializer,
    RegistroUsuarioSerializer,
    PerfilUsuarioSerializer,
    CambiarPasswordSerializer,
)

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
    "CustomTokenObtainPairSerializer",
    "RegistroUsuarioSerializer",
    "PerfilUsuarioSerializer",
    "CambiarPasswordSerializer",
]