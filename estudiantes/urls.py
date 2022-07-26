from estudiantes.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', estudiantes_request, name='estudiantes'),
    path('editar_estudiante/<int:id>', editar_estudiante, name='editar_estudiante'),
]