from cuentas.models import Estudiante
from django.db import models

# Create your models here.
class Solicitud(models.Model):
    TIPOS = (
        ('F', 'Finalización'),
        ('M', 'Prórroga'),
        ('C', 'Corrección'),
    )
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPOS)
    motivo = models.CharField(max_length=100)
    fecha = models.DateTimeField()


    def __str__(self):
        return self.motivo