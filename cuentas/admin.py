from .models import Estudiante, Profesor
from django.contrib import admin

# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(Estudiante)
admin.site.register(Profesor)