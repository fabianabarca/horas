from solicitudes.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', solicitudes_request, name='solicitudes'),

]