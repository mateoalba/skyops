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
from .auth import (
    CustomTokenObtainPairSerializer,
    RegistroUsuarioSerializer,
    PerfilUsuarioSerializer,
    CambiarPasswordSerializer,
)
from .perfil_usuario import PerfilUsuarioSerializer
from .sesion_usuario import SesionUsuarioSerializer
from .audit_log import AuditLogSerializer
from .mantenimiento_aeronave import MantenimientoAeronaveSerializer
from .certificacion_tripulante import CertificacionTripulanteSerializer

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
    "CustomTokenObtainPairSerializer",
    "RegistroUsuarioSerializer",
    "PerfilUsuarioSerializer",
    "CambiarPasswordSerializer",
]