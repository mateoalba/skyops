"""
Helper para registrar automáticamente cada intento de login (exitoso o
fallido) y cada logout en la tabla SesionUsuario, en vez de depender de que
un administrador la llene a mano.
"""


def _obtener_ip(request):
    if request is None:
        return "0.0.0.0"
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # Puede venir como "cliente, proxy1, proxy2"; el primero es el real.
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR") or "0.0.0.0"


def _obtener_user_agent(request):
    if request is None:
        return ""
    return request.META.get("HTTP_USER_AGENT", "")


def registrar_sesion(request, usuario, resultado, token_jti=""):
    """
    Crea un registro de SesionUsuario con la IP y el User-Agent tomados de
    la request actual. `usuario` puede ser None (ej. login fallido con un
    correo que no existe). Se importa el modelo aquí adentro para evitar
    imports circulares con los serializers/views de auth.
    """
    from airport.models.sesion_usuario import SesionUsuario

    return SesionUsuario.objects.create(
        usuario=usuario,
        ip_address=_obtener_ip(request),
        user_agent=_obtener_user_agent(request),
        resultado=resultado,
        token_jti=token_jti or "",
    )
