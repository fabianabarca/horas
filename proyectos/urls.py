from proyectos.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', proyectos_request, name='proyectos'),
    path('crear_proyecto', crear_proyecto, name='crear_proyecto'),

]