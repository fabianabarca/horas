from solicitudes.views import *
from django.contrib.auth import views
from django.urls import path
from django.conf import settings #
from django.conf.urls.static import static #

urlpatterns = [
    path('', solicitudes_request, name='solicitudes'),
    path('crear_solicitud', crear_solicitud, name='crear_solicitud'),

]

#
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
