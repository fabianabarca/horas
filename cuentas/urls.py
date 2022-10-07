from cuentas.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('perfil/', perfil, name='perfil'),
    path('ingreso/', login_request, name='ingreso'),
    path('salir/', logout_request, name= 'salir'),
    path('registro/', register_request, name='registro')
]