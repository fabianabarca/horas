from django.http.response import HttpResponseRedirect
from horas.forms import CategoriasForm, FiltrosProyectoForm, ProyectosForm
from proyectos.models import Proyecto
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



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
        
    form = FiltrosProyectoForm()

    return render (request=request, template_name="../templates/proyectos.html", context={"proyectos":proyectos_list,"filtros_form":form})

@login_required(login_url='/cuentas/login/')
def crear_proyecto(request):

    if request.method == "POST":
        form = ProyectosForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/proyectos")
		
    form = ProyectosForm()
    
    return render (request=request, template_name="../templates/crear_proyecto.html", context={"proyecto_form":form})
 
@login_required(login_url='/cuentas/login/')
def crear_categoria(request):

    if request.method == "POST":
        form = CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/proyectos")
		
    form = CategoriasForm()
    
    return render (request=request, template_name="../templates/crear_categoria.html", context={"categoria_form":form})