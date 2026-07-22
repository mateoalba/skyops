import uuid
from django.db import models
from django.utils import timezone
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
    # asientos_primera / asientos_ejecutiva guardan la lista exacta de
    # códigos de asiento (ej. "1A,1B,2A,2B") que el admin asignó a cada
    # clase desde el mapa de asientos al crear/editar el vuelo. Cualquier
    # asiento que no aparezca en ninguna de las dos listas es económica.
    # Si ambas quedan vacías (valor por defecto, vuelos ya existentes antes
    # de este campo) no hay restricción de clase por asiento: cualquier
    # asiento libre se puede elegir en cualquier clase.
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    asientos_primera = models.TextField(default="", blank=True)
    asientos_ejecutiva = models.TextField(default="", blank=True)

    class Meta:
        db_table = "vuelo"
        verbose_name = "Vuelo"
        verbose_name_plural = "Vuelos"
        ordering = ["salida_programada"]
        unique_together = ["aerolinea", "numero_vuelo", "salida_programada"]

    def __str__(self):
        return f"{self.numero_vuelo} | {self.origen.codigo_iata} → {self.destino.codigo_iata} | {self.salida_programada.strftime('%d/%m/%Y %H:%M')}"

    def estado_efectivo(self):
        """
        Estado real según la hora actual, sin necesitar que nadie lo cambie
        a mano: Programado hasta 1 hora antes de la salida, Embarcando en
        esa última hora, Despegado entre la salida y la llegada programadas,
        y Aterrizado después de la llegada programada. Cancelado y Retrasado
        son overrides manuales (los pone un operador desde el panel cuando
        de verdad pasa algo fuera de lo programado) y nunca se pisan solos
        acá, sin importar la hora.
        """
        if self.estado in (self.Estado.CANCELADO, self.Estado.RETRASADO):
            return self.estado
        ahora = timezone.now()
        una_hora_antes_salida = self.salida_programada - timezone.timedelta(hours=1)
        if ahora < una_hora_antes_salida:
            return self.Estado.PROGRAMADO
        if ahora < self.salida_programada:
            return self.Estado.EMBARCANDO
        if ahora < self.llegada_programada:
            return self.Estado.DESPEGADO
        return self.Estado.ATERRIZADO
