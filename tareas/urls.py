from tareas.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', tareas_request, name='tareas'),
    path('crear_tarea', crear_tarea, name='crear_tarea'),
    path('editar_tarea/<int:id>', editar_tarea, name='editar_tarea'),
]