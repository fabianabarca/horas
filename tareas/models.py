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
    nombre = models.CharField(max_length=500)
    descripcion = models.TextField(blank=True, null=True)
    estudiante = models.ManyToManyField(Estudiante)
    objetivo = models.ForeignKey(Objetivo, on_delete=models.SET_NULL, null=True)
    tareaSuperior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateField(auto_now_add=True, blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)
    urgente = models.BooleanField(default=False)
    estado = models.CharField(blank=True, null=True, choices=ESTADOS, max_length=1, default='A')

    def __str__(self):
        return self.nombre


class AsignacionesEnviadas(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.SET_NULL,null=True)
    tarea = models.ForeignKey(Tarea, on_delete=models.SET_NULL,null=True)

