from proyectos.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', proyectos_request, name='proyectos'),
    path('crear_proyecto', crear_proyecto, name='crear_proyecto'),
    path('crear_categoria', crear_categoria, name='crear_categoria'),
    path('editar_proyecto/<int:id>', editar_proyecto, name='editar_proyecto'),

]