from estudiantes.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', estudiantes, name='estudiantes'),
    path('equipos', equipos, name='equipos'),
    path('<id_ucr>', estudiante, name='estudiante'),
    path('editar_estudiante/<int:id>', editar_estudiante, name='editar_estudiante'),
    path('profesores/', profesores, name='profesores') 
]