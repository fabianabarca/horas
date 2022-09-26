from django.db import models

# Create your models here.

class Registro(models.Model):
    enPapelera = models.BooleanField(default='False')
    fechaPapelera = models.DateField( blank=True, null=True)
    fechaCreacion = models.DateField(auto_now_add=True, null=True)

    class Meta:
        abstract = True

