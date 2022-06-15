from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from tareas.models import *
from horas.forms import TareasForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/cuentas/login/')
def tareas_request(request):
    tareas_list = Tarea.objects.all()

    return render (request=request, template_name="../templates/tareas.html", context={"tareas":tareas_list})

@login_required(login_url='/cuentas/login/')
def crear_tarea(request):

    if request.method == "POST":
        form = TareasForm(request.POST)
        if form.is_valid():
            form.save()
		
    form = TareasForm()
    
    return render (request=request, template_name="../templates/crear_tarea.html", context={"tarea_form":form})

@login_required(login_url='/cuentas/login/')
def editar_tarea(request, id):

    obj = get_object_or_404(Tarea, id = id) 

    form = TareasForm(request.POST or None, instance = obj)
   # form.fields['proyecto'].widget = forms.HiddenInput()
   # form.fields['nombre'].widget = forms.HiddenInput()
   # form.fields['descripcion'].widget = forms.HiddenInput()
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/tareas")

 
    return render(request, "editar_tarea.html", context={"tarea_form":form})