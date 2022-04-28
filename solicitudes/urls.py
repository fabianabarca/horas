from solicitudes.views import *
from django.contrib.auth import views
from django.urls import path
from django.conf import settings # Adjuntar archivo
from django.conf.urls.static import static # Adjuntar archivo

urlpatterns = [
    path('', solicitudes_request, name='solicitudes'),
    path('crear_solicitud', crear_solicitud, name='crear_solicitud'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adjuntar archivo
