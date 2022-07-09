from dashboard.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', dashboard_request, name='dashboard')
]