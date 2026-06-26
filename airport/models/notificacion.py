from django.db import models


class Notificacion(models.Model):
    """
    Alerta o notificación enviada a un pasajero relacionada con un vuelo
    (retraso, cambio de puerta, cancelación, etc.).
    """

    TIPO_CHOICES = [
        ("retraso", "Retraso de vuelo"),
        ("cancelacion", "Cancelación de vuelo"),
        ("cambio_puerta", "Cambio de puerta"),
        ("embarque", "Llamado a embarque"),
        ("confirmacion", "Confirmación de reserva"),
        ("recordatorio", "Recordatorio de vuelo"),
        ("equipaje", "Estado de equipaje"),
        ("otro", "Otro"),
    ]

    CANAL_CHOICES = [
        ("email", "Correo electrónico"),
        ("sms", "SMS"),
        ("push", "Notificación push"),
        ("sistema", "Sistema interno"),
    ]

    ESTADO_CHOICES = [
        ("pendiente", "Pendiente de envío"),
        ("enviada", "Enviada"),
        ("leida", "Leída"),
        ("fallida", "Fallo en el envío"),
    ]

    pasajero = models.ForeignKey(
        "airport.Pasajero",
        on_delete=models.CASCADE,
        related_name="notificaciones",
    )
    vuelo = models.ForeignKey(
        "airport.Vuelo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notificaciones",
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    canal = models.CharField(max_length=10, choices=CANAL_CHOICES, default="email")
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default="pendiente")
    fecha_envio = models.DateTimeField(null=True, blank=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ["-creada_en"]

    def __str__(self):
        return f"[{self.get_tipo_display()}] → {self.pasajero} ({self.estado})"
