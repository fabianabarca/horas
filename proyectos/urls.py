from proyectos.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', proyectos, name='proyectos'),
    path('crear_area', crear_area, name='crear_area'),
    path('crear_proyecto', crear_proyecto, name='crear_proyecto'),
    path('crear_objetivo', crear_objetivo, name='crear_objetivo'),
    #path('editar_area/<int:id>', editar_area, name='editar_area'),
    path('editar_proyecto/<int:id>', editar_proyecto, name='editar_proyecto'),
    path('editar_objetivo/<int:id>', editar_objetivo, name='editar_objetivo'),
    path('proyectosInfo', proyectosInfo, name='proyectosInfo'),
    path('<int:id>/', proyecto, name='proyectoIndividual'),

]