from categorias.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', categorias_request, name='categorias'),
    path('crear_categoria', crear_categoria, name='crear_categoria'),
    path('editar_categoria/<int:id>', editar_categoria, name='editar_categoria'),

]