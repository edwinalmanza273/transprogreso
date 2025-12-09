from django import forms
from .models import Vehiculo, Conductor, Cliente, FUEC, Asignacion


# ============================
#   FORMULARIO VEHÍCULO
# ============================

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = "__all__"


# ============================
#   FORMULARIO CONDUCTOR
# ============================

class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = "__all__"


# ============================
#   FORMULARIO CLIENTE
# ============================

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"


# ============================
#   FORMULARIO FUEC
# ============================

class FUECForm(forms.ModelForm):
    class Meta:
        model = FUEC
        fields = "__all__"
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }


# ============================
#   FORMULARIO ASIGNACIÓN
# ============================

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = "__all__"
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }
