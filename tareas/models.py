from proyectos.models import Objetivo
from cuentas.models import Estudiante
from inicio.models import Registro
from django.contrib.auth.models import User
from django.db import models
from datetime import date

# Create your models here.

class Tarea(Registro):
    ESTADOS = (
        ('A', 'Activa'),
        ('V', 'Vencida'),
        ('F', 'Finalizada'),
    )
    PRIORIDADES = (
        ('B', 'Baja'),
        ('M', 'Media'),
        ('A', 'Alta'),
    )
    nombre = models.CharField(max_length=500, blank=False)
    descripcion = models.TextField(blank=True, null=True)
    estudiante = models.ManyToManyField(Estudiante)
    objetivo = models.ForeignKey(Objetivo, on_delete=models.SET_NULL, null=True)
    tareaSuperior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateField(auto_now_add=True, blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)
    prioridad = models.CharField(choices=PRIORIDADES, max_length=1, default='B', blank=True, null=True)
    estado = models.CharField(choices=ESTADOS, max_length=1, default='A', blank=True, null=True)

    def __str__(self):
        if self.nombre==None:
            return 'Hay un problema aquí'
        return self.nombre


class AsignacionesEnviadas(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.SET_NULL,null=True)
    tarea = models.ForeignKey(Tarea, on_delete=models.SET_NULL,null=True)

