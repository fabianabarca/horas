from django.contrib import admin
from .models import *

class SolicitudArchivoInline(admin.TabularInline):
    model = SolicitudArchivo


class SolicitudAdmin(admin.ModelAdmin):
    inlines = [
        SolicitudArchivoInline,
    ]

# Register your models here.
admin.site.register(Solicitud)
admin.site.register(SolicitudArchivo)