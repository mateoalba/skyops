from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth.models import User
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from airport.models.perfil_usuario import PerfilUsuario
from airport.serializers.auth import (
    CustomTokenObtainPairSerializer,
    RegistroUsuarioSerializer,
    PerfilUsuarioSerializer,
    CambiarPasswordSerializer,
)


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Body: { "email": "...", "password": "..." }
    Retorna: access token, refresh token y datos del usuario.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RefreshTokenView(TokenRefreshView):
    """
    POST /api/auth/refresh/
    Body: { "refresh": "..." }
    Retorna: nuevo access token.
    """
    permission_classes = [AllowAny]


class RegistroView(generics.CreateAPIView):
    """
    POST /api/auth/registro/
    Crea un nuevo usuario en el sistema.
    """
    queryset = User.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generar tokens automáticamente al registrarse
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "mensaje": "Usuario creado exitosamente.",
                "usuario": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request):
    """
    POST /api/auth/google/
    Body: { "id_token": "<token entregado por el SDK de Google Sign-In>" }

    Verifica el ID token contra Google, y si el correo ya existe crea una
    sesión para ese usuario; si no existe, crea la cuenta automáticamente
    (con PerfilUsuario cargo='usuario') y devuelve el JWT igual que /login/.

    Requiere la variable de entorno GOOGLE_OAUTH_CLIENT_ID (Client ID de tipo
    "Web application" creado en Google Cloud Console > APIs & Services >
    Credentials). Sin esa variable configurada, el endpoint responde 503.
    """
    client_id = getattr(settings, "GOOGLE_OAUTH_CLIENT_ID", "")
    if not client_id:
        return Response(
            {"error": "Login con Google no está configurado en el servidor."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    token = request.data.get("id_token")
    if not token:
        return Response(
            {"error": "Se requiere 'id_token'."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        payload = google_id_token.verify_oauth2_token(
            token, google_requests.Request(), client_id
        )
    except ValueError:
        return Response(
            {"error": "Token de Google inválido o expirado."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    email = payload.get("email")
    if not email:
        return Response(
            {"error": "El token de Google no incluye un correo."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.filter(email=email).first()
    creado = False
    if user is None:
        base_username = email.split("@")[0]
        username = base_username
        contador = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{contador}"
            contador += 1
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=payload.get("given_name", ""),
            last_name=payload.get("family_name", ""),
        )
        user.set_unusable_password()
        user.save()
        PerfilUsuario.objects.create(usuario=user, cargo=PerfilUsuario.Cargo.USUARIO)
        creado = True

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "mensaje": "Cuenta creada e inicio de sesión con Google." if creado else "Inicio de sesión con Google exitoso.",
            "creado": creado,
            "usuario": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "es_staff": user.is_staff,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=status.HTTP_201_CREATED if creado else status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    POST /api/auth/logout/
    Body: { "refresh": "..." }
    Invalida el refresh token (blacklist).
    """
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Se requiere el refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"mensaje": "Sesión cerrada exitosamente."})
    except Exception:
        return Response(
            {"error": "Token inválido o ya expirado."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PerfilView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/auth/perfil/  → ver mi perfil
    PUT  /api/auth/perfil/  → actualizar mi perfil
    """
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cambiar_password(request):
    """
    POST /api/auth/cambiar-password/
    Body: { "password_actual": "...", "password_nuevo": "...", "password_nuevo2": "..." }
    """
    serializer = CambiarPasswordSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data["password_nuevo"])
        user.save()
        return Response({"mensaje": "Contraseña actualizada exitosamente."})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
