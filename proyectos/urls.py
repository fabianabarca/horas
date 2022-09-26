from proyectos.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', proyectos_request, name='proyectos'),
    path('crear_proyecto', crear_proyecto, name='crear_proyecto'),
    path('crear_area', crear_area, name='crear_area'),
    path('editar_proyecto/<int:id>', editar_proyecto, name='editar_proyecto'),
    path('proyectosInfo', proyectosInfo, name='proyectosInfo'),
    path('proyectoIndividual/<int:id>', proyectoIndividual, name='proyectoIndividual'),

]