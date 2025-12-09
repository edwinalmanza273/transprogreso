# gestion_vehiculos/utils.py
from datetime import date, timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import Documento, Fuec, Convenio, RevisionPreventiva


def generar_fuec_pdf(fuec: Fuec):
    """Genera y guarda PDF simple para el FUEC."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"FUEC - {fuec.numero_contrato}")

    c.setFont("Helvetica", 11)
    y = 770
    line = 20
    c.drawString(50, y, f"Empresa:        {fuec.empresa.nombre}"); y -= line
    c.drawString(50, y, f"Conductor:      {fuec.conductor.nombre}"); y -= line
    c.drawString(50, y, f"Vehículo:       {fuec.vehiculo.placa}"); y -= line
    c.drawString(50, y, f"Fecha inicio:   {fuec.fecha_inicio}"); y -= line
    c.drawString(50, y, f"Fecha fin:      {fuec.fecha_fin}")
    c.showPage()
    c.save()

    fuec.archivo_pdf.save(
        f"FUEC_{fuec.numero_contrato}.pdf",
        ContentFile(buffer.getvalue()),
        save=True
    )
    buffer.close()


# --- CONSULTAS PARA ALERTAS ---------------------------------------------------
def documentos_por_vencer(dias=30):
    limite = date.today() + timedelta(days=dias)
    return (Documento.objects
            .select_related('vehiculo', 'conductor', 'vehiculo__empresa')
            .filter(fecha_vencimiento__lte=limite)
            .order_by('fecha_vencimiento'))


def fuec_por_vencer(dias=30):
    from .models import Fuec
    limite = date.today() + timedelta(days=dias)
    return (Fuec.objects
            .select_related('empresa', 'conductor', 'vehiculo')
            .filter(fecha_fin__lte=limite)
            .order_by('fecha_fin'))


def convenios_por_vencer(dias=30):
    limite = date.today() + timedelta(days=dias)
    return (Convenio.objects
            .select_related('empresa', 'conductor', 'vehiculo')
            .filter(fecha_fin__lte=limite)
            .order_by('fecha_fin'))


def revisiones_por_vencer(dias=30):
    limite = date.today() + timedelta(days=dias)
    return (RevisionPreventiva.objects
            .select_related('vehiculo')
            .filter(proxima_fecha__lte=limite)
            .order_by('proxima_fecha'))


# --- ESTADO DOCUMENTAL --------------------------------------------------------
def estado_documentos_por_vehiculo(vehiculo, dias_aviso=30):
    """Lista dicts: [{'tipo', 'estado', 'vence'}] para chips en /vehiculos"""
    hoy = date.today()
    limite = hoy + timedelta(days=dias_aviso)

    docs = (Documento.objects
            .filter(vehiculo=vehiculo)
            .order_by('tipo', '-fecha_vencimiento'))
    ultimos = {}
    for d in docs:
        if d.tipo not in ultimos:
            ultimos[d.tipo] = d

    resultados = []
    for tipo, d in ultimos.items():
        if d.fecha_vencimiento < hoy:
            estado = 'vencido'
        elif d.fecha_vencimiento <= limite:
            estado = 'por_vencer'
        else:
            estado = 'vigente'
        resultados.append({'tipo': tipo, 'estado': estado, 'vence': d.fecha_vencimiento})
    return resultados


def vehiculo_habilitado(vehiculo):
    """
    Habilitado si TODOS los últimos documentos del vehículo están:
      - Vigentes (no vencidos)
      - Validados (estado_validacion=True)
    """
    hoy = date.today()
    docs = (Documento.objects
            .filter(vehiculo=vehiculo)
            .order_by('tipo', '-fecha_vencimiento'))
    ultimos = {}
    for d in docs:
        if d.tipo not in ultimos:
            ultimos[d.tipo] = d
    if not ultimos:
        return False
    for d in ultimos.values():
        if d.fecha_vencimiento < hoy or not d.estado_validacion:
            return False
    return True
