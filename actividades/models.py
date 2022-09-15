from django.contrib.auth.models import User
from proyectos.models import Proyecto
from tareas.models import Tarea
from cuentas.models import Estudiante
from django.db import models
from django.conf import settings
from inicio.models import Registro

# Create your models here.

class Actividad(Registro):
    ESTADOS = (
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
        ('P', 'En Revisión'),
    )
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    #proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL,null=True)
    tarea = models.ForeignKey(Tarea, on_delete=models.SET_NULL,null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    horas = models.IntegerField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default= "En Revisión")
    
    def __str__(self):
        return self.descripcion

