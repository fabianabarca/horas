"""horas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Ver los archivos desde admin
from django.conf.urls.static import static # Ver los archivos desde admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('actividades.urls')),
    path('actividades/', include('actividades.urls'), name="actividades"),
    path('tareas/', include('tareas.urls'), name="tareas"),
    path('proyectos/', include('proyectos.urls'), name="proyectos"),
    path('solicitudes/', include('solicitudes.urls'), name="solicitudes"),
    path('estudiantes/', include('estudiantes.urls'), name="estudiantes"),
    path('categorias/', include('categorias.urls'), name="categorias"),
    path('cuentas/', include('cuentas.urls'), name="cuentas"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Ver los archivos desde admin
