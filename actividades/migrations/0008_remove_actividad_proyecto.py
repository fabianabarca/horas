# Generated by Django 3.2.7 on 2022-07-21 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0007_alter_actividad_fechapapelera'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividad',
            name='proyecto',
        ),
    ]
