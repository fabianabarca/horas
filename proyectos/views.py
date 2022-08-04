from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import AreasForm, FiltrosProyectoForm, ProyectosForm
from proyectos.models import Proyecto
from proyectos.models import Area
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
import time

# Create your views here.
@login_required(login_url='/cuentas/login/')
def proyectos_request(request):
    proyectos_list = Proyecto.objects.all()


    if request.method == "POST":
        form = FiltrosProyectoForm(request.POST or None)
     

        if form.is_valid():
            if form.cleaned_data.get('nombre'):
                proyectos_list =  proyectos_list.filter(nombre__contains = form.cleaned_data.get('nombre'))
            if form.cleaned_data.get('descripcion'):
                proyectos_list =  proyectos_list.filter(descripcion__contains= form.cleaned_data.get('descripcion'))
            if form.cleaned_data.get('profesor'):
                proyectos_list =  proyectos_list.filter(profesor = form.cleaned_data.get('profesor'))
            if form.cleaned_data.get('area'):
                proyectos_list =  proyectos_list.filter(area= form.cleaned_data.get('area'))
            if form.cleaned_data.get('ubicacion'):
                proyectos_list =  proyectos_list.filter(ubicacion__contains= form.cleaned_data.get('ubicacion'))

    
        if request.POST.get('deleteButton'):
                deleteButtonItemValue=request.POST.getlist('deleteButton')
                obj = Proyecto( id = deleteButtonItemValue[0]) 
                Proyecto.objects.filter(id = deleteButtonItemValue[0]).update(enPapelera='True')
        
        #return HttpResponseRedirect("/proyectos")  
        
    form = FiltrosProyectoForm()

    return render (request=request, template_name="../templates/proyectos.html", context={"proyectos":proyectos_list,"filtros_form":form})

@login_required(login_url='/cuentas/login/')
def crear_proyecto(request):

    if request.method == "POST":
        form = ProyectosForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)#para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/proyectos")
	
    
    form = ProyectosForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    #para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    areas_noborrados = Area.objects.all()
    areas_noborrados=areas_noborrados.filter(enPapelera= False)
    form.fields["area"].queryset  = areas_noborrados

    creacionOedicion = 1
    return render (request=request, template_name="../templates/crear_proyecto.html", context={"tipoAccion":creacionOedicion,"proyecto_form":form})
 
@login_required(login_url='/cuentas/login/')
def crear_area(request):

    if request.method == "POST":
        form = AreasForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)#para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/proyectos")
	
    
    form = AreasForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()



    return render (request=request, template_name="../templates/crear_area.html", context={"area_form":form})


@login_required(login_url='/cuentas/login/')
def editar_proyecto(request, id):

    obj = get_object_or_404(Proyecto, id = id) 

    form = ProyectosForm(request.POST or None, instance = obj)
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    #para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    areas_noborrados = Area.objects.all()
    areas_noborrados=areas_noborrados.filter(enPapelera= False)
    form.fields["area"].queryset  = areas_noborrados
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/proyectos")

    creacionOedicion = 0
    return render(request, "crear_proyecto.html", context={"tipoAccion":creacionOedicion,"proyecto_form":form})


def proyectosInfo(request):
    listaProyectos = Proyecto.objects.all()
   
    return render(request=request,  template_name="../templates/proyectosInfo.html", context={"listaProyectos":listaProyectos})

def proyectoIndividual(request,id):
    proyecto = Proyecto.objects.filter(id=id)
    proyectoHoras=1
    objetivos = proyecto[0].objetivo_set.filter(enPapelera=False)
    
    listatareas = []
    for objetivo in objetivos:
        tareas = objetivo.tarea_set.filter(enPapelera=False)
        for tarea in tareas:
            listatareas.append(tarea.nombre)

    return render(request=request,  template_name="../templates/proyectoIndividual.html", context={"proyecto":proyecto[0],
    "proyectoHoras":proyectoHoras, "objetivos":objetivos, "tareas":listatareas})