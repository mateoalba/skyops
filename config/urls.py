from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
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
# de servirlas.
#
# OJO: el helper django.conf.urls.static.static() NO sirve para esto en
# producción — internamente hace "if not settings.DEBUG: return []", así
# que con DEBUG=False no agrega ninguna ruta pase lo que pase (esa fue la
# causa real del 404 anterior, aunque el código se viera bien). Por eso
# acá se registra la ruta a mano con re_path()+serve, que no tiene ese
# candado.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
