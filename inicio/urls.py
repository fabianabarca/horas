#from inicio.views import *
#from django.contrib.auth import views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/<int:id>', views.index, name='index'),

]