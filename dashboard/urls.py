from dashboard.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('resumen/', resumen, name='resumen'),
    path('panel/', panel, name='panel')
]