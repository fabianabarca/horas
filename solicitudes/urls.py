from solicitudes.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', solicitudes_request, name='solicitudes'),
    path('crear_solicitud', crear_solicitud, name='crear_solicitud'),

]