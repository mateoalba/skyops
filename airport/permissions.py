from rest_framework.permissions import BasePermission, SAFE_METHODS


class EsAdmin(BasePermission):
    """
    Solo usuarios con is_staff=True tienen acceso total.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class EsOperador(BasePermission):
    """
    Usuarios del grupo 'Operadores' pueden leer, crear y editar.
    No pueden eliminar.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if request.method == "DELETE":
            return False
        return request.user.groups.filter(name="Operadores").exists()


class EsUsuarioOAdmin(BasePermission):
    """
    Cualquier usuario autenticado puede leer.
    Solo admin puede escribir.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class EsPasajeroOOperador(BasePermission):
    """
    Cualquier usuario autenticado puede crear/editar una reserva, siempre que
    sea SU PROPIA reserva (el 'pasajero' de la reserva debe tener el mismo
    email que su cuenta). Operador/Admin pueden reservar en nombre de
    cualquier pasajero. La validación de "es mi propio pasajero" se hace en
    el serializer (ReservaSerializer.validate), porque en create() todavía
    no existe el objeto para has_object_permission.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == "DELETE":
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user.groups.filter(name="Operadores").exists():
            return True
        return obj.pasajero.email == request.user.email


class EsPropietarioOAdmin(BasePermission):
    """
    El usuario solo puede ver y editar sus propias reservas.
    El admin puede ver y editar todo.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # Para reservas: verificar que el pasajero coincida con el usuario
        if hasattr(obj, "pasajero"):
            return obj.pasajero.email == request.user.email
        return False


class SoloLectura(BasePermission):
    """
    Lectura pública (GET, HEAD, OPTIONS) para cualquiera, con o sin sesión.
    Se usa en catálogos de referencia (aerolíneas, aeropuertos, aeronaves,
    puertas) que un visitante debe poder ver para buscar vuelos sin crear
    cuenta primero — igual que en cualquier buscador de aerolíneas real.
    Escribir (POST/PUT/PATCH/DELETE) sigue exigiendo el permiso que cada
    ViewSet use aparte para esos métodos (normalmente EsOperador).
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
# Aliases para compatibilidad
IsOwnerOrAdmin = EsPropietarioOAdmin
IsAdminUser = EsAdmin
IsOperator = EsOperador
IsAuthenticatedOrReadOnly = EsUsuarioOAdmin
ReadOnly = SoloLectura