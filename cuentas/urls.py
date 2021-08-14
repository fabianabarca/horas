from cuentas.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name= 'logout'),
    path('register/', register_request, name='register')
]