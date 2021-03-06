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
        ('P', 'En Revisión'),
    )
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPOS)
    motivo = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default= "En Revisión")
    #archivo = models.FileField(upload_to='documents/', blank=True) # Adjuntar archivo

class SolicitudArchivo(models.Model):
    archivo = models.FileField(upload_to='documents/', blank=True) # Adjuntar archivo
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
