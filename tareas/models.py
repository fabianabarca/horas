from proyectos.models import Proyecto
from cuentas.models import Estudiante
from inicio.models import Registro
from django.db import models



# Create your models here.

class Tarea(Registro):
    nombre = models.CharField(max_length=500)
    estudiante = models.ManyToManyField(Estudiante)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL,null=True)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre

