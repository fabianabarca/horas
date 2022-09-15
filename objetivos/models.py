from proyectos.models import Proyecto
from inicio.models import Registro
from django.db import models

# Create your models here.

class ObjetivoX(Registro):
    descripcion = models.TextField(blank=True, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True)
    general = models.BooleanField(False)

    def __str__(self):
        return self.descripcion
