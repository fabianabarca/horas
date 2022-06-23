from proyectos.models import Proyecto
from cuentas.models import Estudiante
from actividades.models import Actividad

from django.db import models



# Create your models here.

class Tarea(models.Model):
    nombre = models.CharField(max_length=500)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE,blank=True, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=500)
    
    def __str__(self):
        return self.nombre

