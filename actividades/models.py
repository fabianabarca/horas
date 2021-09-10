from django.contrib.auth.models import User
from proyectos.models import Proyecto
from cuentas.models import Estudiante
from django.db import models



# Create your models here.

class Actividad(models.Model):
    ESTADOS = (
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
        ('P', 'En Revisión'),
    )
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=500)
    fecha = models.DateField()
    horas = models.IntegerField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default= "En Revisión")

    def __str__(self):
        return self.descripcion

