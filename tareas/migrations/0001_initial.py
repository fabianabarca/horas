# Generated by Django 3.1.6 on 2021-10-20 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyectos', '0003_auto_20210817_1650'),
        ('cuentas', '0005_remove_estudiante_carrera'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=500)),
                ('descripcion', models.CharField(max_length=500)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuentas.estudiante')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyecto')),
            ],
        ),
    ]