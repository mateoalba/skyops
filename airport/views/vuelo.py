from django.utils import timezone
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from airport.models import Vuelo
from airport.serializers import VueloSerializer
from airport.permissions import EsOperador
from airport.filters import VueloFilter


def _sincronizar_estados_pendientes():
    """
    Antes de cualquier lectura, pone al día en la base los vuelos cuyo
    estado ya no corresponde a la hora actual (ver Vuelo.estado_efectivo) —
    así el filtro `?estado=despegado` también encuentra los que recién
    "despegaron" según el reloj, no solo los que alguien marcó a mano a
    tiempo. No hay un cron/job en segundo plano en este proyecto: se
    recalcula "perezosamente" justo antes de servir cualquier respuesta.
    Cancelado, Retrasado y Aterrizado nunca entran acá: los dos primeros son
    overrides manuales que no se tocan solos, y Aterrizado ya es un estado
    final que no vuelve a cambiar.
    """
    pendientes = Vuelo.objects.exclude(
        estado__in=[Vuelo.Estado.CANCELADO, Vuelo.Estado.RETRASADO, Vuelo.Estado.ATERRIZADO]
    )
    a_actualizar = []
    for vuelo in pendientes:
        nuevo_estado = vuelo.estado_efectivo()
        if nuevo_estado != vuelo.estado:
            vuelo.estado = nuevo_estado
            a_actualizar.append(vuelo)
    if a_actualizar:
        Vuelo.objects.bulk_update(a_actualizar, ["estado"])


class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.select_related(
        "aerolinea", "aeronave", "origen", "destino", "puerta"
    ).all()
    serializer_class = VueloSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VueloFilter
    search_fields = ["numero_vuelo", "origen__codigo_iata", "destino__codigo_iata"]
    ordering_fields = ["salida_programada", "llegada_programada", "numero_vuelo", "duracion_min"]
    ordering = ["salida_programada"]

    def get_queryset(self):
        _sincronizar_estados_pendientes()
        queryset = super().get_queryset()
        # El listado público (buscador de vuelos, "Ofertas desde") no debe
        # mostrar vuelos que ya pasaron: no tiene sentido "reservar" algo que
        # ya salió. No se borran de la base de datos (las reservas ya hechas
        # sobre ellos siguen intactas en /reservas/ y en "Mis reservas", que
        # consultan Reserva por su propia FK y nunca pasan por este listado)
        # — solo se ocultan del listado. El panel admin (/admin/vuelos) sí
        # necesita ver el historial completo para poder gestionarlo, así que
        # manda `incluir_pasados=true` para saltarse este filtro.
        if self.action == "list":
            incluir_pasados = self.request.query_params.get("incluir_pasados", "").lower() in (
                "1", "true", "si", "sí", "yes",
            )
            if not incluir_pasados:
                queryset = queryset.filter(salida_programada__gte=timezone.now())
        return queryset

    def get_permissions(self):
        # Buscar y ver vuelos es público a propósito (como en cualquier
        # buscador de aerolíneas): un visitante sin cuenta debe poder ver
        # los resultados. Solo reservar/editar/eliminar exige rol Operador.
        if self.action in ["list", "retrieve", "por_ruta", "asientos_ocupados"]:
            return [permissions.AllowAny()]
        return [EsOperador()]

    @action(detail=True, methods=["get"], url_path="asientos-ocupados")
    def asientos_ocupados(self, request, pk=None):
        """
        GET /api/vuelos/{id}/asientos-ocupados/
        Devuelve solo los números de asiento ya reservados (no cancelados)
        de este vuelo, sin exponer a quién pertenecen — así cualquier
        pasajero puede pintar el mapa de asientos sin ver datos de otros.
        """
        vuelo = self.get_object()
        # Cada reserva puede cubrir varios asientos a la vez (CSV en
        # numero_asiento, ej. "12A,12B"), así que hay que separarlos antes
        # de devolver la lista plana de asientos ocupados.
        crudos = vuelo.reservas.exclude(estado="cancelada").values_list("numero_asiento", flat=True)
        asientos = set()
        for valor in crudos:
            asientos.update(s.strip().upper() for s in (valor or "").split(",") if s.strip())
        return Response({"asientos_ocupados": sorted(asientos)})

    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        """PATCH /api/vuelos/{id}/cambiar-estado/"""
        vuelo = self.get_object()
        nuevo_estado = request.data.get("estado")
        estados_validos = [e[0] for e in Vuelo.Estado.choices]
        if nuevo_estado not in estados_validos:
            return Response(
                {"error": f"Estado inválido. Opciones: {estados_validos}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vuelo.estado = nuevo_estado
        vuelo.save()
        return Response(self.get_serializer(vuelo).data)

    @action(detail=False, methods=["get"], url_path="por-ruta")
    def por_ruta(self, request):
        """GET /api/vuelos/por-ruta/?origen=UIO&destino=GYE"""
        origen = request.query_params.get("origen")
        destino = request.query_params.get("destino")
        if not origen or not destino:
            return Response(
                {"error": "Se requieren los parámetros 'origen' y 'destino'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vuelos = self.get_queryset().filter(
            origen__codigo_iata=origen.upper(),
            destino__codigo_iata=destino.upper(),
        )
        return Response(self.get_serializer(vuelos, many=True).data)