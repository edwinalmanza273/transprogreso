from django.core.management.base import BaseCommand
from gestion_vehiculos.models import Vehiculo

class Command(BaseCommand):
    help = 'Carga datos iniciales de prueba en la base de datos'

    def handle(self, *args, **kwargs):
        Vehiculo.objects.create(
            placa="ABC123",
            modelo="Chevrolet NQR",
            soat="2026-09-28",
            licencia_conduccion="2027-01-01"
        )
        self.stdout.write(self.style.SUCCESS("Vehículo de prueba agregado correctamente"))
