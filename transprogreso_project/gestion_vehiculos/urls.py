from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [

    # Dashboard como página de inicio
    path("", views.dashboard, name="inicio"),

    # Dashboard directo
    path("dashboard/", views.dashboard, name="dashboard"),

    # Vehículos
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('vehiculos/nuevo/', views.vehiculo_nuevo, name='vehiculo_nuevo'),
    path('vehiculos/<int:id>/', views.vehiculo_detalle, name='vehiculo_detalle'),
    path('vehiculos/<int:id>/editar/', views.vehiculo_editar, name='vehiculo_editar'),
    path('vehiculos/<int:id>/eliminar/', views.vehiculo_eliminar, name='vehiculo_eliminar'),

    # Conductores
    path('conductores/', views.conductores, name='conductores'),
    path('conductores/nuevo/', views.conductor_nuevo, name='conductor_nuevo'),
    path('conductores/<int:id>/', views.conductor_detalle, name='conductor_detalle'),
    path('conductores/<int:id>/editar/', views.conductor_editar, name='conductor_editar'),
    path('conductores/<int:id>/eliminar/', views.conductor_eliminar, name='conductor_eliminar'),

    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/nuevo/', views.cliente_nuevo, name='cliente_nuevo'),
    path('clientes/<int:id>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:id>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:id>/eliminar/', views.cliente_eliminar, name='cliente_eliminar'),

    # FUEC
    path("fuec/", views.fuec, name="fuec"),
    path("fuec/crear/", views.fuec_crear, name="fuec_crear"),
    path("fuec/nuevo/", views.fuec_nuevo, name="fuec_nuevo"),
    path("fuec/<int:id>/", views.fuec_detalle, name="fuec_detalle"),
    path("fuec/<int:id>/editar/", views.fuec_editar, name="fuec_editar"),
    path("fuec/<int:id>/eliminar/", views.fuec_eliminar, name="fuec_eliminar"),
    path("fuec/<int:id>/pdf/", views.fuec_pdf, name="fuec_pdf"),

    # Alertas
    path('alertas/', views.alertas, name='alertas'),

    # Logout
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),

    # Asignaciones
    path("asignaciones/", views.asignaciones, name="asignaciones"),
    path("asignaciones/nueva/", views.asignar_conductor, name="asignar_conductor"),

    # Reportes PDF
    path("reporte/vehiculos/", views.reporte_vehiculos, name="reporte_vehiculos"),
    path("reporte/conductores/", views.reporte_conductores, name="reporte_conductores"),
    path("reporte/clientes/", views.reporte_clientes, name="reporte_clientes"),
    path("reporte/fuec/", views.reporte_fuec, name="reporte_fuec"),

    path("reporte/alertas/", views.reporte_alertas, name="reporte_alertas"),


]
