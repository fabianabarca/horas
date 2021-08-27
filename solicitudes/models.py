from cuentas.models import Estudiante
from django.db import models

# Create your models here.
class Solicitud(models.Model):
    TIPOS = (
        ('F', 'Finalización'),
        ('M', 'Prórroga'),
        ('C', 'Corrección'),
    )
    ESTADOS = (
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
        ('P', 'En progreso'),
    )
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPOS)
    motivo = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default= "En progeso")


    def __str__(self):
        return self.motivo