from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import CategoriasForm, FiltrosProyectoForm, ProyectosForm
from proyectos.models import Proyecto
from proyectos.models import Categoria
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
            if form.cleaned_data.get('categoria'):
                proyectos_list =  proyectos_list.filter(categoria= form.cleaned_data.get('categoria'))
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
    categorias_noborrados = Categoria.objects.all()
    categorias_noborrados=categorias_noborrados.filter(enPapelera= False)
    form.fields["categoria"].queryset  = categorias_noborrados

    creacionOedicion = 1
    return render (request=request, template_name="../templates/crear_proyecto.html", context={"tipoAccion":creacionOedicion,"proyecto_form":form})
 
@login_required(login_url='/cuentas/login/')
def crear_categoria(request):

    if request.method == "POST":
        form = CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)#para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/proyectos")
	
    
    form = CategoriasForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()



    return render (request=request, template_name="../templates/crear_categoria.html", context={"categoria_form":form})


@login_required(login_url='/cuentas/login/')
def editar_proyecto(request, id):

    obj = get_object_or_404(Proyecto, id = id) 

    form = ProyectosForm(request.POST or None, instance = obj)
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    #para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    categorias_noborrados = Categoria.objects.all()
    categorias_noborrados=categorias_noborrados.filter(enPapelera= False)
    form.fields["categoria"].queryset  = categorias_noborrados
    
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
    
    listametas = []
    for objetivo in objetivos:
        metas = objetivo.meta_set.filter(enPapelera=False)
        for meta in metas:
            listametas.append(meta.nombre)

    return render(request=request,  template_name="../templates/proyectoIndividual.html", context={"proyecto":proyecto[0],
    "proyectoHoras":proyectoHoras, "objetivos":objetivos, "metas":listametas})