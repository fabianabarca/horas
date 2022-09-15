from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Estudiante.objects.create(user=instance)


class Estudiante(models.Model):
    ESTADOS = (
        ('A', 'Activo'),
        ('F', 'Finalizado'),
        ('P', 'Prórroga'),
        ('R', 'Retirado'),
        ('I', 'Incompleto'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Profesor, blank=True, null=True, on_delete=models.SET_NULL)
    carrera = models.ForeignKey(Carrera, blank=True, null=True, on_delete=models.SET_NULL)
    fechaInicioTCU = models.DateField(blank=True, null=True)
    fechaFinTCU = models.DateField(blank=True, null=True)
    estado = models.CharField(blank=False, null=True, choices=ESTADOS, max_length=1, default='A')

    def __str__(self):
        return self.user.first_name
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.Estudiante.save()