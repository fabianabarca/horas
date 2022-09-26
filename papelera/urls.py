from papelera.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', papelera_request, name='papelera'),

]