from actividades.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', actividades_request, name='actividades'),

]