from metas.views import *
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('', metas_request, name='metas'),
    path('crear_meta', crear_meta, name='crear_meta'),
    path('editar_meta/<int:id>', editar_meta, name='editar_meta'),

]