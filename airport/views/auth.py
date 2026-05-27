from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from airport.serializers.auth import (
    CustomTokenObtainPairSerializer,
    RegistroUsuarioSerializer,
    PerfilUsuarioSerializer,
    CambiarPasswordSerializer,
)


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Body: { "username": "...", "password": "..." }
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
        serializer.save()
        return Response({"mensaje": "Contraseña actualizada exitosamente."})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)