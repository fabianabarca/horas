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
        if request.POST.get('deleteButtonActividad'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonActividad')
                obj = Tarea( id = deleteButtonItemValueList[0]) 
                obj.delete()
        if request.POST.get('deleteButtonTarea'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonTarea')
                obj = Tarea( id = deleteButtonItemValueList[0]) 
                obj.delete()
        if request.POST.get('deleteButtonProyecto'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonProyecto')
                obj = Proyecto( id = deleteButtonItemValueList[0]) 
                obj.delete()
        if request.POST.get('deleteButtonCategoria'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonCategoria')
                obj = Categoria( id = deleteButtonItemValueList[0]) 
                obj.delete()
        if request.POST.get('deleteButtonSolicitud'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonSolicitud')
                obj = Solicitud( id = deleteButtonItemValueList[0]) 
                obj.delete()

    return render (request=request, template_name="../templates/papelera.html", context={"actividades":actividades_list,"tareas":tareas_list,"proyectos":proyectos_list,"categorias":categorias_list,"solicitudes":solicitudes_list})

