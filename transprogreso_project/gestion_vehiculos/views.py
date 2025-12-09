from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

from .models import Vehiculo, Conductor, Cliente, FUEC, Asignacion
from .forms import VehiculoForm, ConductorForm, ClienteForm, FUECForm


# ============================================
#               DASHBOARD
# ============================================
@login_required
def dashboard(request):
    return render(request, "dashboard.html", {
        "total_vehiculos": Vehiculo.objects.count(),
        "total_conductores": Conductor.objects.count(),
        "total_clientes": Cliente.objects.count(),
        "total_fuec": FUEC.objects.count(),
    })


# ============================================
#               VEHÍCULOS
# ============================================
@login_required
def vehiculos(request):
    return render(request, "vehiculos/lista.html", {
        "vehiculos": Vehiculo.objects.all()
    })


@login_required
def vehiculo_nuevo(request):
    if request.method == "POST":
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("vehiculos")
    else:
        form = VehiculoForm()

    return render(request, "vehiculos/form.html", {"form": form})


@login_required
def vehiculo_editar(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    if request.method == "POST":
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect("vehiculos")
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, "vehiculos/form.html", {"form": form})


@login_required
def vehiculo_eliminar(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    if request.method == "POST":
        vehiculo.delete()
        return redirect("vehiculos")

    return render(request, "vehiculos/eliminar.html", {"vehiculo": vehiculo})


# ============================================
#               CONDUCTORES
# ============================================
@login_required
def conductores(request):
    return render(request, "conductores/lista.html", {
        "conductores": Conductor.objects.all()
    })


@login_required
def conductor_nuevo(request):
    if request.method == "POST":
        form = ConductorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("conductores")
    else:
        form = ConductorForm()

    return render(request, "conductores/form.html", {"form": form})


@login_required
def conductor_editar(request, id):
    conductor = get_object_or_404(Conductor, id=id)
    if request.method == "POST":
        form = ConductorForm(request.POST, request.FILES, instance=conductor)
        if form.is_valid():
            form.save()
            return redirect("conductores")
    else:
        form = ConductorForm(instance=conductor)

    return render(request, "conductores/form.html", {"form": form})


@login_required
def conductor_eliminar(request, id):
    conductor = get_object_or_404(Conductor, id=id)
    if request.method == "POST":
        conductor.delete()
        return redirect("conductores")

    return render(request, "conductores/eliminar.html", {"conductor": conductor})


@login_required
def conductor_detalle(request, id):
    conductor = get_object_or_404(Conductor, id=id)
    return render(request, "conductores/detalle.html", {"conductor": conductor})


# ============================================
#               CLIENTES
# ============================================
@login_required
def clientes(request):
    return render(request, "clientes/lista.html", {
        "clientes": Cliente.objects.all()
    })


@login_required
def cliente_nuevo(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clientes")
    else:
        form = ClienteForm()

    return render(request, "clientes/form.html", {"form": form})


@login_required
def cliente_editar(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("clientes")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "clientes/form.html", {"form": form})


@login_required
def cliente_eliminar(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == "POST":
        cliente.delete()
        return redirect("clientes")

    return render(request, "clientes/eliminar.html", {"cliente": cliente})


@login_required
def cliente_detalle(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, "clientes/detalle.html", {"cliente": cliente})


# ============================================
#                    FUEC
# ============================================
@login_required
def fuec(request):
    fuecs = FUEC.objects.select_related("vehiculo", "conductor", "cliente").all()
    return render(request, "fuec/lista.html", {"fuecs": fuecs})


@login_required
def fuec_nuevo(request):
    if request.method == "POST":
        form = FUECForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fuec")
    else:
        form = FUECForm()

    return render(request, "fuec/form.html", {"form": form})


@login_required
def fuec_detalle(request, id):
    fuec_obj = get_object_or_404(FUEC, id=id)
    return render(request, "fuec/detalle.html", {"fuec": fuec_obj})


@login_required
def fuec_eliminar(request, id):
    fuec = get_object_or_404(FUEC, id=id)
    if request.method == "POST":
        fuec.delete()
        return redirect("fuec")

    return render(request, "fuec/eliminar.html", {"fuec": fuec})


@login_required
def fuec_editar(request, id):
    fuec = get_object_or_404(FUEC, id=id)
    if request.method == "POST":
        form = FUECForm(request.POST, instance=fuec)
        if form.is_valid():
            form.save()
            return redirect("fuec")
    else:
        form = FUECForm(instance=fuec)

    return render(request, "fuec/form.html", {"form": form})


@login_required
def fuec_crear(request):
    if request.method == "POST":
        form = FUECForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fuec")
    else:
        form = FUECForm()

    return render(request, "fuec/crear.html", {"form": form})


# ============================================
#           GENERAR PDF DEL FUEC
# ============================================
@login_required
@login_required
@login_required
@login_required
def fuec_pdf(request, id):
    from django.contrib.staticfiles import finders
    fuec = get_object_or_404(FUEC, id=id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="FUEC_{fuec.numero}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    # Buscar la imagen con STATICFILES FINDER (la forma correcta)
    template_path = finders.find("img/fuec_plantilla.png")

    if not template_path:
        return HttpResponse("ERROR: No se encontró la plantilla FUEC.", status=500)

    # Dibujar imagen
    pdf.drawImage(template_path, 0, 0, width=600, height=780)

    # Datos del FUEC
    pdf.setFont("Helvetica", 10)
    pdf.drawString(150, 680, fuec.cliente.nombre)
    pdf.drawString(150, 650, fuec.vehiculo.placa)
    pdf.drawString(150, 630, fuec.conductor.nombre)
    pdf.drawString(150, 610, str(fuec.fecha_inicio))
    pdf.drawString(150, 590, str(fuec.fecha_fin))
    pdf.drawString(150, 570, fuec.ruta)

    pdf.showPage()
    pdf.save()
    return response





# ============================================
#               ALERTAS
# ============================================
@login_required
def alertas(request):
    from datetime import date, timedelta

    hoy = date.today()
    proximos_30 = hoy + timedelta(days=30)
    vehiculos = Vehiculo.objects.all()
    alertas = []

    for v in vehiculos:
        if v.soat_fecha and v.soat_fecha <= proximos_30:
            alertas.append({"vehiculo": v.placa, "tipo": "SOAT", "fecha": v.soat_fecha})

        if v.tecnomecanica_fecha and v.tecnomecanica_fecha <= proximos_30:
            alertas.append({"vehiculo": v.placa, "tipo": "Tecnomecánica", "fecha": v.tecnomecanica_fecha})

        if v.poliza_fecha and v.poliza_fecha <= proximos_30:
            alertas.append({"vehiculo": v.placa, "tipo": "Póliza", "fecha": v.poliza_fecha})

        if v.extrajudicial_fecha and v.extrajudicial_fecha <= proximos_30:
            alertas.append({"vehiculo": v.placa, "tipo": "Extrajudicial", "fecha": v.extrajudicial_fecha})

    return render(request, "alertas/lista.html", {"alertas": alertas})


# ============================================
#          ASIGNACIONES
# ============================================
@login_required
def asignaciones(request):
    return render(request, "asignaciones/lista.html", {
        "asignaciones": Asignacion.objects.all()
    })


@login_required
def asignar_conductor(request):
    if request.method == "POST":
        Asignacion.objects.create(
            vehiculo_id=request.POST.get("vehiculo"),
            conductor_id=request.POST.get("conductor"),
            fecha=request.POST.get("fecha")
        )
        return redirect("asignaciones")

    return render(request, "asignaciones/nueva.html", {
        "vehiculos": Vehiculo.objects.all(),
        "conductores": Conductor.objects.all()
    })


@login_required
def vehiculo_detalle(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    return render(request, "vehiculos/detalle.html", {"vehiculo": vehiculo})


# ============================================
#               REPORTES
# ============================================
@login_required
def reporte_vehiculos(request):
    vehiculos = Vehiculo.objects.all().order_by("placa")
    return render(request, "reportes/reporte_vehiculos.html", {"vehiculos": vehiculos})


@login_required
def reporte_conductores(request):
    conductores = Conductor.objects.all().order_by("nombre")
    return render(request, "reportes/reporte_conductores.html", {"conductores": conductores})


@login_required
def reporte_clientes(request):
    clientes = Cliente.objects.all().order_by("nombre")
    return render(request, "reportes/reporte_clientes.html", {"clientes": clientes})


@login_required
def reporte_fuec(request):
    fuecs = FUEC.objects.all().order_by("-id")
    return render(request, "reportes/reporte_fuec.html", {"fuecs": fuecs})


@login_required
def reporte_alertas(request):
    alertas = []
    return render(request, "reportes/reporte_alertas.html", {"alertas": alertas})
