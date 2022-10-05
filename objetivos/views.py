from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import ObjetivosForm, ObjetivosForm
from proyectos.models import Objetivo
from proyectos.models import Proyecto
from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time

# Create your views here.
@login_required(login_url='/cuentas/login/')
def objetivos_request(request):
    objetivos_list = Objetivo.objects.all()
    if request.method == "POST":
        if request.POST.get('deleteButton'):
                deleteButtonItemValue=request.POST.getlist('deleteButton')
                obj = Objetivo( id = deleteButtonItemValue[0]) 
                Objetivo.objects.filter(id = deleteButtonItemValue[0]).update(enPapelera='True')
        
        return HttpResponseRedirect("/objetivos")  

    return render (request, "objetivos.html", context={"objetivos":objetivos_list})

@login_required(login_url='/cuentas/login/')
def crear_objetivo(request):

    if request.method == "POST":
        form = ObjetivosForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)#para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/objetivos")
		
    form = ObjetivosForm()
    form.fields['general'].widget = forms.HiddenInput()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    #para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    proyectos_noborrados = Proyecto.objects.all()
    proyectos_noborrados=proyectos_noborrados.filter(enPapelera= False)
    form.fields["proyecto"].queryset  = proyectos_noborrados

    creacionOedicion = 1
    return render (request=request, template_name="../templates/crear_objetivo.html", context={"tipoAccion":creacionOedicion,"objetivo_form":form})
 

@login_required(login_url='/cuentas/login/')
def editar_objetivo(request, id):

    obj = get_object_or_404(Objetivo, id = id) 

    form = ObjetivosForm(request.POST or None, instance = obj)
    
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/objetivos")
        
    form.fields['general'].widget = forms.HiddenInput()        
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    #para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    proyectos_noborrados = Proyecto.objects.all()
    proyectos_noborrados=proyectos_noborrados.filter(enPapelera= False)
    form.fields["proyecto"].queryset  = proyectos_noborrados

    creacionOedicion = 0
    return render(request, "crear_objetivo.html", context={"tipoAccion":creacionOedicion,"objetivo_form":form})
