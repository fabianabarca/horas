from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from actividades.models import Actividad
from proyectos.models import *
from tareas.models import Tarea
from solicitudes.models import Solicitud

# Create your views here.
@login_required(login_url='/cuentas/ingreso/')
def papelera_request(request):
    actividades_list = Actividad.objects.all()
    tareas_list = Tarea.objects.all()
    
    objetivos_list = Objetivo.objects.all()
    proyectos_list = Proyecto.objects.all()
    areas_list = Area.objects.all()
    solicitudes_list = Solicitud.objects.all()
    if request.method == "POST":
        #Implementación de boton de borrado de la base de datos de los registros
        if request.POST.get('deleteButtonActividad'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonActividad')
                obj = Actividad( id = deleteButtonItemValueList[0]) 
                obj.delete()
        if request.POST.get('deleteButtonTarea'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonTarea')
                obj = Tarea( id = deleteButtonItemValueList[0]) 
                obj.delete()
        #cambio meta tareas
        if request.POST.get('deleteButtonObjetivo'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonObjetivo')
                obj = Objetivo( id = deleteButtonItemValueList[0]) 
                obj.delete()
        if request.POST.get('deleteButtonProyecto'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonProyecto')
                obj = Proyecto( id = deleteButtonItemValueList[0]) 
                obj.delete()
        if request.POST.get('deleteButtonArea'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonArea')
                obj = Area( id = deleteButtonItemValueList[0]) 
                obj.delete()
        if request.POST.get('deleteButtonSolicitud'):
                deleteButtonItemValueList=request.POST.getlist('deleteButtonSolicitud')
                obj = Solicitud( id = deleteButtonItemValueList[0]) 
                obj.delete()


        if request.POST.get('returnButtonActividad'):
                deleteButtonItemValueList=request.POST.getlist('returnButtonActividad')
                obj = Actividad( id = deleteButtonItemValueList[0]) 
                Actividad.objects.filter(id = deleteButtonItemValueList[0]).update(enPapelera='False')
        
        if request.POST.get('returnButtonTarea'):
                deleteButtonItemValueList=request.POST.getlist('returnButtonTarea')
                obj = Tarea( id = deleteButtonItemValueList[0]) 
                Tarea.objects.filter(id = deleteButtonItemValueList[0]).update(enPapelera='False')
        
        #cambio meta tareas

        if request.POST.get('returnButtonObjetivo'):
                deleteButtonItemValueList=request.POST.getlist('returnButtonObjetivo')
                obj = Objetivo( id = deleteButtonItemValueList[0]) 
                Objetivo.objects.filter(id = deleteButtonItemValueList[0]).update(enPapelera='False')

        if request.POST.get('returnButtonProyecto'):
                deleteButtonItemValueList=request.POST.getlist('returnButtonProyecto')
                obj = Proyecto( id = deleteButtonItemValueList[0]) 
                Proyecto.objects.filter(id = deleteButtonItemValueList[0]).update(enPapelera='False')

        if request.POST.get('returnButtonArea'):
                deleteButtonItemValueList=request.POST.getlist('returnButtonArea')
                obj = Area( id = deleteButtonItemValueList[0]) 
                Area.objects.filter(id = deleteButtonItemValueList[0]).update(enPapelera='False')

        if request.POST.get('returnButtonSolicitud'):
                deleteButtonItemValueList=request.POST.getlist('returnButtonSolicitud')
                obj = Solicitud( id = deleteButtonItemValueList[0]) 
                Solicitud.objects.filter(id = deleteButtonItemValueList[0]).update(enPapelera='False')

        return HttpResponseRedirect("/papelera")

    return render (request=request, template_name="../templates/papelera.html", context={"actividades":actividades_list,"tareas":tareas_list,"objetivos":objetivos_list,"proyectos":proyectos_list,"areas":areas_list,"solicitudes":solicitudes_list})

