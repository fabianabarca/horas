from objetivos.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', objetivos_request, name='objetivos'),
    path('crear_objetivo', crear_objetivo, name='crear_objetivo'),
    path('editar_objetivo/<int:id>', editar_objetivo, name='editar_objetivo'),

]