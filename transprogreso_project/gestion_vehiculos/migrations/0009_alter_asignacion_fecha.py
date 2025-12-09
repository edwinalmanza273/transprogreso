from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('gestion_vehiculos', '0008_remove_asignacion_activo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacion',
            name='fecha',
            field=models.DateField(null=True, blank=True),
        ),
    ]

