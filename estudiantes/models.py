from django.db import models
from cuentas.models import Estudiante
from proyectos.models import Proyecto

# Create your models here.


class Equipo(models.Model):
    '''Modelo de un equipo de estudiantes.

    Contiene el nombre, participantes y otras
    informaciones de cada equipo.
    '''
    ESTADOS = (
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('F', 'Finalizado'),
    )
    nombre = models.CharField(max_length=64, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    estudiantes = models.ManyToManyField(Estudiante, blank=True, null=True)
    proyectos = models.ManyToManyField(Proyecto, blank=True, null=True)
    contacto = models.CharField(max_length=128, blank=True, null=True)
    estado = models.CharField(choices=ESTADOS, max_length=1, default='A', blank=False, null=True)

    def __str__(self):
        return self.nombre
