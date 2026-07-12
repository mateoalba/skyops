from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API principal
    path("api/", include("airport.urls")),

    # Documentación OpenAPI / Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Sirve las fotos de perfil (y cualquier otro archivo subido). Lo ideal en
# producción sería que Nginx sirva MEDIA_URL directamente desde MEDIA_ROOT,
# pero como ese servidor no tiene ese alias configurado, Django se encarga
# de servirlas siempre (también con DEBUG=False) para que las imágenes no
# den 404.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
