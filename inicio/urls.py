#from inicio.views import *
#from django.contrib.auth import views
from django.urls import path

from . import views

urlpatterns = [
    path('inicio', views.index, name='inicio'),
    path('', views.sitio, name='sitio'),


]