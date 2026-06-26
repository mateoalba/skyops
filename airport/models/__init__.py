from .aerolinea import Aerolinea
from .aeropuerto import Aeropuerto
from .aeronave import Aeronave
from .puerta import Puerta
from .vuelo import Vuelo
from .pasajero import Pasajero
from .reserva import Reserva
from .tripulante import Tripulante
from .asignacion_tripulacion import AsignacionTripulacion
from .incidente import Incidente
from .tipo_aeronave import TipoAeronave
from .equipaje import Equipaje
from .tarjeta_embarque import TarjetaEmbarque
from .categoria_pasajero import CategoriaPasajero
from .notificacion import Notificacion

__all__ = [
    "Aerolinea",
    "Aeropuerto",
    "Aeronave",
    "Puerta",
    "Vuelo",
    "Pasajero",
    "Reserva",
    "Tripulante",
    "AsignacionTripulacion",
    "Incidente",
    "TipoAeronave",      # 👈 nuevo
    "Equipaje",           # 👈 nuevo
    "TarjetaEmbarque",    # 👈 nuevo
    "CategoriaPasajero",  # 👈 nuevo
    "Notificacion",       # 👈 nuevo
]
