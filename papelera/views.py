from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from actividades.models import Actividad
from proyectos.models import *
from tareas.models import Tarea
from solicitudes.models import Solicitud

# Create your views here.
@login_required(login_url='/cuentas/login/')
def papelera_request(request):
    actividades_list = Actividad.objects.all()
    tareas_list = Tarea.objects.all()
    proyectos_list = Proyecto.objects.all()
    categorias_list = Categoria.objects.all()
    solicitudes_list = Solicitud.objects.all()
    if request.method == "POST":
        if request.POST.get('deleteButton'):
                deleteButtonItemValue=request.POST.getlist('deleteButton')
                obj = Tarea( id = deleteButtonItemValue[0]) 
                obj.delete()

    return render (request=request, template_name="../templates/papelera.html", context={"actividades":actividades_list,"tareas":tareas_list,"proyectos":proyectos_list,"categorias":categorias_list,"solicitudes":solicitudes_list})

