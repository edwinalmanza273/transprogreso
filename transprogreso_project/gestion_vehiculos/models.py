from django.db import models
from django.contrib.auth.models import User

# ============================
#   VEHÍCULO
# ============================
class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    capacidad = models.IntegerField(null=True, blank=True)

    # Fechas de documentos
    soat_fecha = models.DateField(null=True, blank=True)
    tecnomecanica_fecha = models.DateField(null=True, blank=True)
    poliza_fecha = models.DateField(null=True, blank=True)
    extrajudicial_fecha = models.DateField(null=True, blank=True)

    # Archivos
    soat_archivo = models.FileField(upload_to="documentos/soat/", null=True, blank=True)
    tecnomecanica_archivo = models.FileField(upload_to="documentos/tecnomecanica/", null=True, blank=True)
    poliza_archivo = models.FileField(upload_to="documentos/polizas/", null=True, blank=True)

    def __str__(self):
        return self.placa


# ============================
#   CONDUCTOR
# ============================
class Conductor(models.Model):
    cedula = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=100)
    licencia = models.CharField(max_length=20)
    categoria = models.CharField(max_length=10)
    licencia_vencimiento = models.DateField(null=True, blank=True)

    licencia_archivo = models.FileField(upload_to="documentos/licencias/", null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"


# ============================
#   CLIENTE
# ============================
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.identificacion})"


# ============================
#   FUEC
# ============================
class FUEC(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    ruta = models.CharField(max_length=200)
    objeto_contrato = models.CharField(max_length=200, default="Transporte Especial de Pasajeros")

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FUEC {self.numero}"


# ============================
#   ASIGNACIÓN
# ============================
class Asignacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.vehiculo.placa} asignado a {self.conductor.nombre}"


# ============================
#   PERFIL DE USUARIO
# ============================
class Perfil(models.Model):
    ROL_CHOICES = [
        ("ADMIN", "Administrador"),
        ("OPERADOR", "Operador"),
        ("INSPECTOR", "Inspector"),
        ("CONDUCTOR", "Conductor"),
        ("CLIENTE", "Cliente"),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="OPERADOR")

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"

