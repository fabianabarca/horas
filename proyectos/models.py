from email.policy import default
from cuentas.models import Profesor
from inicio.models import Registro
from django.db import models

# Create your models here.


class Area(Registro):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Proyecto(Registro):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    profesor = models.ManyToManyField(Profesor)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    ubicacion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre


class Objetivo(Registro):
    descripcion = models.TextField(blank=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)
    general = models.BooleanField('¿Es objetivo general?', default=False)

    def __str__(self):
        return self.descripcion
