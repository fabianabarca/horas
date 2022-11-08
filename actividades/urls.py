from actividades.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', actividades, name='actividades'),
    path('crear_actividad', crear_actividad, name='crear_actividad'),
    path('editar_actividad/<int:id>', editar_actividad, name='editar_actividad'),

    path('load-proyectosActividades/', load_proyectos, name='load-proyectosActividades'), # AJAX
    path('load-objetivosActividades/', load_objetivos, name='load-objetivosActividades'), # AJAX
    path('load-tareasActividades/', load_tareas, name='load-tareasActividades'), # AJAX

]