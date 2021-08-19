from django.db import models
from .models import Actividad 
from django.contrib import admin

# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(Actividad)
