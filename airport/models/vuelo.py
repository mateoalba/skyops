import uuid
from django.db import models
from .aerolinea import Aerolinea
from .aeronave import Aeronave
from .aeropuerto import Aeropuerto
from .puerta import Puerta


class Vuelo(models.Model):

    class Estado(models.TextChoices):
        PROGRAMADO = "programado", "Programado"
        EMBARCANDO = "embarcando", "Embarcando"
        DESPEGADO = "despegado", "Despegado"
        ATERRIZADO = "aterrizado", "Aterrizado"
        CANCELADO = "cancelado", "Cancelado"
        RETRASADO = "retrasado", "Retrasado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aerolinea = models.ForeignKey(
        Aerolinea, on_delete=models.CASCADE, related_name="vuelos"
    )
    aeronave = models.ForeignKey(
        Aeronave, on_delete=models.SET_NULL, null=True, related_name="vuelos"
    )
    origen = models.ForeignKey(
        Aeropuerto, on_delete=models.CASCADE, related_name="vuelos_salida"
    )
    destino = models.ForeignKey(
        Aeropuerto, on_delete=models.CASCADE, related_name="vuelos_llegada"
    )
    puerta = models.ForeignKey(
        Puerta, on_delete=models.SET_NULL, null=True, blank=True, related_name="vuelos"
    )
    numero_vuelo = models.CharField(max_length=10)
    salida_programada = models.DateTimeField()
    llegada_programada = models.DateTimeField()
    salida_real = models.DateTimeField(null=True, blank=True)
    llegada_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PROGRAMADO
    )
    duracion_min = models.PositiveIntegerField(null=True, blank=True)

    # Precio y configuración de clases de cabina. El precio_base corresponde
    # a clase económica; ejecutiva/primera se calculan con un multiplicador
    # fijo (ver MULTIPLICADOR_CLASE en airport/serializers/reserva.py) y NO
    # se guardan por separado, para no tener que mantenerlos sincronizados.
    #
    # filas_primera / filas_ejecutiva definen cuántas filas al frente del
    # avión son de esa clase (ej. filas_primera=2 -> filas 1-2 son primera).
    # Las filas siguientes hasta filas_ejecutiva son ejecutiva, y el resto
    # económica. Si ambos quedan en 0 (valor por defecto, vuelos ya
    # existentes antes de este campo) no hay restricción de clase por
    # asiento: cualquier asiento libre se puede elegir en cualquier clase.
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    filas_primera = models.PositiveIntegerField(default=0, blank=True)
    filas_ejecutiva = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        db_table = "vuelo"
        verbose_name = "Vuelo"
        verbose_name_plural = "Vuelos"
        ordering = ["salida_programada"]
        unique_together = ["aerolinea", "numero_vuelo", "salida_programada"]

    def __str__(self):
        return f"{self.numero_vuelo} | {self.origen.codigo_iata} → {self.destino.codigo_iata} | {self.salida_programada.strftime('%d/%m/%Y %H:%M')}"
