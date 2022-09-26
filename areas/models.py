from cuentas.models import Profesor
from inicio.models import Registro
from django.db import models

# Create your models here.

class Area(Registro):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
