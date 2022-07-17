from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from tareas.models import *
from proyectos.models import *
from horas.forms import TareasForm ,FiltrosTareaForm
from django.contrib.auth.decorators import login_required
import time
from django.core.mail import send_mail

# Create your views here.
@login_required(login_url='/cuentas/login/')
def tareas_request(request):
    tareas_list = Tarea.objects.all()
    if request.method == "POST":
           
        form = FiltrosTareaForm(request.POST or None)
        if request.POST.get('deleteButton'):
                print("activado delete")
                deleteButtonItemValue=request.POST.getlist('deleteButton')
                obj = Tarea( id = deleteButtonItemValue[0]) 
                Tarea.objects.filter(id = deleteButtonItemValue[0]).update(enPapelera='True')
                
        
        if request.POST.get('assignButton'):
                print("activado assign")
                asignButtonItemValue=request.POST.getlist('assignButton')
                obj = Tarea( id = asignButtonItemValue[0]) 
                tareaAsignar=Tarea.objects.filter(id = asignButtonItemValue[0])
                for userAssign in tareaAsignar[0].estudiante.all():
                    send_mail(
                                'Asignación de tarea',
                                'Se te asigno la tarea: ' + tareaAsignar[0].nombre +'\n\n'
                                + 'Descripción: '+ tareaAsignar[0].descripcion  +'\n\n'
                                + 'Del proyecto: '+ tareaAsignar[0].proyecto.nombre  +'\n\n'
                                ,
                                'testertesrter3@gmail.com',
                                [userAssign.user.email],
                                fail_silently=False,
                    )
                
        
        if form.is_valid():
            if form.cleaned_data.get('nombre'):
                tareas_list =  tareas_list.filter(nombre__contains = form.cleaned_data.get('nombre'))
            if form.cleaned_data.get('estudiante'):
                tareas_list =  tareas_list.filter(estudiante = form.cleaned_data.get('estudiante'))
            if form.cleaned_data.get('descripcion'):
                tareas_list =  tareas_list.filter(descripcion__contains = form.cleaned_data.get('descripcion'))
            if form.cleaned_data.get('proyecto'):
                tareas_list =  tareas_list.filter(proyecto = form.cleaned_data.get('proyecto'))

            if form.cleaned_data.get('categoria'):
                tareas_list =  tareas_list.filter(proyecto__categoria= form.cleaned_data.get('categoria'))
           
        return HttpResponseRedirect("/tareas")
        
    form = FiltrosTareaForm()

    return render (request=request, template_name="../templates/tareas.html", context={"tareas":tareas_list,"filtros_form":form})

@login_required(login_url='/cuentas/login/')
def crear_tarea(request):

    if request.method == "POST":
        form = TareasForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)#para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/tareas")
            
    form = TareasForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()
    creacionOedicion = 1

    return render (request=request, template_name="../templates/crear_tarea.html", context={"tipoAccion":creacionOedicion,"tarea_form":form})

@login_required(login_url='/cuentas/login/')
def editar_tarea(request, id):

    obj = get_object_or_404(Tarea, id = id) 

    form = TareasForm(request.POST or None, instance = obj)
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()
   # form.fields['proyecto'].widget = forms.HiddenInput()
   # form.fields['nombre'].widget = forms.HiddenInput()
   # form.fields['descripcion'].widget = forms.HiddenInput()
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/tareas")

    creacionOedicion = 0
    return render(request, "crear_tarea.html", context={"tipoAccion":creacionOedicion,"tarea_form":form})