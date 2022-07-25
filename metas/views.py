from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import MetasForm, MetasForm
from proyectos.models import Meta
from proyectos.models import *
from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time

# Create your views here.
@login_required(login_url='/cuentas/login/')
def metas_request(request):
    metas_list = Meta.objects.all()
    if request.method == "POST":
        if request.POST.get('deleteButton'):
                deleteButtonItemValue=request.POST.getlist('deleteButton')
                obj = Meta( id = deleteButtonItemValue[0]) 
                Meta.objects.filter(id = deleteButtonItemValue[0]).update(enPapelera='True')
        
        return HttpResponseRedirect("/metas")  

    return render (request=request, template_name="../templates/metas.html", context={"metas":metas_list})

@login_required(login_url='/cuentas/login/')
def crear_meta(request):

    if request.method == "POST":
        form = MetasForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)#para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/metas")
		
    form = MetasForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    #para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    objetivos_noborrados = Objetivo.objects.all()
    objetivos_noborrados=objetivos_noborrados.filter(enPapelera= False)
    form.fields["objetivo"].queryset  = objetivos_noborrados

    creacionOedicion = 1
    return render (request=request, template_name="../templates/crear_meta.html", context={"tipoAccion":creacionOedicion,"meta_form":form})
 

@login_required(login_url='/cuentas/login/')
def editar_meta(request, id):

    obj = get_object_or_404(Meta, id = id) 

    form = MetasForm(request.POST or None, instance = obj)
    
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/metas")
        
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    #para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    objetivos_noborrados = Objetivo.objects.all()
    objetivos_noborrados=objetivos_noborrados.filter(enPapelera= False)
    form.fields["objetivo"].queryset  = objetivos_noborrados

    creacionOedicion = 0
    return render(request, "crear_meta.html", context={"tipoAccion":creacionOedicion,"meta_form":form})
