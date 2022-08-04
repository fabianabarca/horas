from actividades.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', actividades_request, name='actividades'),
    path('crear_actividad', crear_actividad, name='crear_actividad'),
    path('editar_actividad/<int:id>', editar_actividad, name='editar_actividad'),
    path('load-tareas/', load_tareas, name='load_tareas'), # AJAX

]