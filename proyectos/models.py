from cuentas.models import Profesor
from inicio.models import Registro
from django.db import models
class Categoria(Registro):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
class Proyecto(Registro):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    categoria = models.ManyToManyField(Categoria)
    ubicacion = models.CharField(max_length=500)
 
    def __str__(self):
        return self.nombre


    def __unicode__(self):
        return self.nombre