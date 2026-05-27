"""
Script de datos de prueba para SkyOps.
Ejecutar con: python manage.py shell < seed_data.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.utils import timezone
from datetime import timedelta
from airport.models import (
    Aerolinea, Aeropuerto, Aeronave, Puerta,
    Vuelo, Pasajero, Reserva, Tripulante,
    AsignacionTripulacion, Incidente,
)

print("🧹 Limpiando datos anteriores...")
Incidente.objects.all().delete()
AsignacionTripulacion.objects.all().delete()
Reserva.objects.all().delete()
Vuelo.objects.all().delete()
Puerta.objects.all().delete()
Aeronave.objects.all().delete()
Tripulante.objects.all().delete()
Pasajero.objects.all().delete()
Aeropuerto.objects.all().delete()
Aerolinea.objects.all().delete()

# ------------------------------------------------------------------
# Aerolíneas
# ------------------------------------------------------------------
print("✈️  Creando aerolíneas...")
latam = Aerolinea.objects.create(nombre="LATAM Airlines", codigo_iata="LA", pais="Chile")
avianca = Aerolinea.objects.create(nombre="Avianca", codigo_iata="AV", pais="Colombia")
copa = Aerolinea.objects.create(nombre="Copa Airlines", codigo_iata="CM", pais="Panamá")

# ------------------------------------------------------------------
# Aeropuertos
# ------------------------------------------------------------------
print("🏢 Creando aeropuertos...")
uio = Aeropuerto.objects.create(
    nombre="Aeropuerto Internacional Mariscal Sucre",
    codigo_iata="UIO", ciudad="Quito", pais="Ecuador",
    latitud=-0.1292, longitud=-78.3575, zona_horaria="America/Guayaquil",
)
gye = Aeropuerto.objects.create(
    nombre="Aeropuerto Internacional José Joaquín de Olmedo",
    codigo_iata="GYE", ciudad="Guayaquil", pais="Ecuador",
    latitud=-2.1574, longitud=-79.8836, zona_horaria="America/Guayaquil",
)
bog = Aeropuerto.objects.create(
    nombre="Aeropuerto Internacional El Dorado",
    codigo_iata="BOG", ciudad="Bogotá", pais="Colombia",
    latitud=4.7016, longitud=-74.1469, zona_horaria="America/Bogota",
)
lim = Aeropuerto.objects.create(
    nombre="Aeropuerto Internacional Jorge Chávez",
    codigo_iata="LIM", ciudad="Lima", pais="Perú",
    latitud=-12.0219, longitud=-77.1143, zona_horaria="America/Lima",
)

# ------------------------------------------------------------------
# Puertas
# ------------------------------------------------------------------
print("🚪 Creando puertas...")
puerta_uio_a1 = Puerta.objects.create(aeropuerto=uio, codigo="A1", terminal="Terminal A")
puerta_uio_a2 = Puerta.objects.create(aeropuerto=uio, codigo="A2", terminal="Terminal A")
puerta_gye_b1 = Puerta.objects.create(aeropuerto=gye, codigo="B1", terminal="Terminal B")
puerta_bog_c1 = Puerta.objects.create(aeropuerto=bog, codigo="C1", terminal="Terminal C")

# ------------------------------------------------------------------
# Aeronaves
# ------------------------------------------------------------------
print("🛩️  Creando aeronaves...")
a320 = Aeronave.objects.create(
    aerolinea=latam, matricula="HC-CLA", modelo="Airbus A320",
    fabricante="Airbus", capacidad=180,
)
b737 = Aeronave.objects.create(
    aerolinea=avianca, matricula="HK-AVB", modelo="Boeing 737-800",
    fabricante="Boeing", capacidad=162,
)
b737_copa = Aeronave.objects.create(
    aerolinea=copa, matricula="HP-COP", modelo="Boeing 737 MAX",
    fabricante="Boeing", capacidad=166,
)

# ------------------------------------------------------------------
# Tripulantes
# ------------------------------------------------------------------
print("👨‍✈️ Creando tripulantes...")
piloto1 = Tripulante.objects.create(
    aerolinea=latam, nombre="Carlos", apellido="Mendoza",
    rol="piloto", num_licencia="PL-EC-001",
)
copiloto1 = Tripulante.objects.create(
    aerolinea=latam, nombre="Ana", apellido="Torres",
    rol="copiloto", num_licencia="CO-EC-002",
)
auxiliar1 = Tripulante.objects.create(
    aerolinea=latam, nombre="María", apellido="Vega",
    rol="auxiliar", num_licencia="AX-EC-003",
)
piloto2 = Tripulante.objects.create(
    aerolinea=avianca, nombre="Jorge", apellido="Ramírez",
    rol="piloto", num_licencia="PL-CO-004",
)

# ------------------------------------------------------------------
# Pasajeros
# ------------------------------------------------------------------
print("🧑 Creando pasajeros...")
p1 = Pasajero.objects.create(
    nombre="Luis", apellido="García", num_pasaporte="PE123456",
    nacionalidad="Ecuatoriano", fecha_nacimiento="1990-05-15",
    email="luis.garcia@email.com", telefono="0991234567",
)
p2 = Pasajero.objects.create(
    nombre="Sofía", apellido="Martínez", num_pasaporte="PE789012",
    nacionalidad="Colombiana", fecha_nacimiento="1985-08-22",
    email="sofia.martinez@email.com", telefono="0997654321",
)
p3 = Pasajero.objects.create(
    nombre="Pedro", apellido="López", num_pasaporte="PE345678",
    nacionalidad="Peruano", fecha_nacimiento="1995-03-10",
    email="pedro.lopez@email.com", telefono="0993456789",
)

# ------------------------------------------------------------------
# Vuelos
# ------------------------------------------------------------------
print("🛫 Creando vuelos...")
ahora = timezone.now()

vuelo1 = Vuelo.objects.create(
    aerolinea=latam, aeronave=a320, origen=uio, destino=gye,
    puerta=puerta_uio_a1, numero_vuelo="LA101",
    salida_programada=ahora + timedelta(hours=2),
    llegada_programada=ahora + timedelta(hours=2, minutes=50),
    estado="programado", duracion_min=50,
)
vuelo2 = Vuelo.objects.create(
    aerolinea=avianca, aeronave=b737, origen=gye, destino=bog,
    puerta=puerta_gye_b1, numero_vuelo="AV205",
    salida_programada=ahora + timedelta(hours=4),
    llegada_programada=ahora + timedelta(hours=5, minutes=30),
    estado="programado", duracion_min=90,
)
vuelo3 = Vuelo.objects.create(
    aerolinea=latam, aeronave=a320, origen=uio, destino=lim,
    puerta=puerta_uio_a2, numero_vuelo="LA310",
    salida_programada=ahora - timedelta(hours=1),
    llegada_programada=ahora + timedelta(hours=2),
    estado="despegado", duracion_min=180,
)

# ------------------------------------------------------------------
# Reservas
# ------------------------------------------------------------------
print("🎫 Creando reservas...")
Reserva.objects.create(vuelo=vuelo1, pasajero=p1, numero_asiento="12A", clase="economica", estado="confirmada")
Reserva.objects.create(vuelo=vuelo1, pasajero=p2, numero_asiento="12B", clase="economica", estado="confirmada")
Reserva.objects.create(vuelo=vuelo2, pasajero=p3, numero_asiento="3C", clase="ejecutiva", estado="confirmada")
Reserva.objects.create(vuelo=vuelo3, pasajero=p1, numero_asiento="1A", clase="primera", estado="abordada")

# ------------------------------------------------------------------
# Asignaciones de tripulación
# ------------------------------------------------------------------
print("👥 Asignando tripulación...")
AsignacionTripulacion.objects.create(vuelo=vuelo1, tripulante=piloto1, rol_asignado="Piloto al mando")
AsignacionTripulacion.objects.create(vuelo=vuelo1, tripulante=copiloto1, rol_asignado="Primer oficial")
AsignacionTripulacion.objects.create(vuelo=vuelo1, tripulante=auxiliar1, rol_asignado="Auxiliar principal")
AsignacionTripulacion.objects.create(vuelo=vuelo2, tripulante=piloto2, rol_asignado="Piloto al mando")

# ------------------------------------------------------------------
# Incidentes
# ------------------------------------------------------------------
print("⚠️  Creando incidentes...")
Incidente.objects.create(
    vuelo=vuelo3, tipo="tecnico",
    descripcion="Falla menor en sistema de presurización, resuelta antes del despegue.",
    severidad="media", estado_resolucion="resuelto",
)
Incidente.objects.create(
    vuelo=vuelo2, tipo="meteorologico",
    descripcion="Turbulencia moderada esperada en ruta. Pasajeros notificados.",
    severidad="baja", estado_resolucion="en_proceso",
)

print("")
print("✅ Datos de prueba creados exitosamente!")
print(f"   • {Aerolinea.objects.count()} aerolíneas")
print(f"   • {Aeropuerto.objects.count()} aeropuertos")
print(f"   • {Aeronave.objects.count()} aeronaves")
print(f"   • {Puerta.objects.count()} puertas")
print(f"   • {Vuelo.objects.count()} vuelos")
print(f"   • {Pasajero.objects.count()} pasajeros")
print(f"   • {Reserva.objects.count()} reservas")
print(f"   • {Tripulante.objects.count()} tripulantes")
print(f"   • {AsignacionTripulacion.objects.count()} asignaciones")
print(f"   • {Incidente.objects.count()} incidentes")