from solicitudes.views import *
from django.contrib.auth import views
from django.urls import path
from django.conf import settings # Adjuntar archivo
from django.conf.urls.static import static # Adjuntar archivo

urlpatterns = [
    path('', solicitudes, name='solicitudes'),
    path('crear_solicitud', crear_solicitud, name='crear_solicitud'),
    path('editar_solicitud/<int:id>', editar_solicitud, name='editar_solicitud'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adjuntar archivo
