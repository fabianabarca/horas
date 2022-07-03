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
    if request.method == "POST":
        if request.POST.get('deleteButton'):
                deleteButtonItemValue=request.POST.getlist('deleteButton')
                obj = Tarea( id = deleteButtonItemValue[0]) 
                Tarea.objects.filter(id = deleteButtonItemValue[0]).update(enPapelera='True')

    return render (request=request, template_name="../templates/tareas.html", context={"tareas":tareas_list})

@login_required(login_url='/cuentas/login/')
def crear_tarea(request):

    if request.method == "POST":
        form = TareasForm(request.POST)
        if form.is_valid():
            form.save()
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