from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # TODAS LAS RUTAS DE LA APP
    path("", include("gestion_vehiculos.urls")),
]
