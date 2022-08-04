from areas.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', areas_request, name='areas'),
    path('crear_area', crear_area, name='crear_area'),
    path('editar_area/<int:id>', editar_area, name='editar_area'),

]