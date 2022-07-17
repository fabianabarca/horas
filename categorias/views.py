from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import CategoriasForm, CategoriasForm
from proyectos.models import Categoria
from proyectos.models import Proyecto
from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time

# Create your views here.
@login_required(login_url='/cuentas/login/')
def categorias_request(request):
    categorias_list = Categoria.objects.all()
    if request.method == "POST":
        if request.POST.get('deleteButton'):
                deleteButtonItemValue=request.POST.getlist('deleteButton')
                obj = Categoria( id = deleteButtonItemValue[0]) 
                Categoria.objects.filter(id = deleteButtonItemValue[0]).update(enPapelera='True')
        
        return HttpResponseRedirect("/categorias")  

    return render (request=request, template_name="../templates/categorias.html", context={"categorias":categorias_list})

@login_required(login_url='/cuentas/login/')
def crear_categoria(request):

    if request.method == "POST":
        form = CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)#para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/categorias")
		
    form = CategoriasForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()
    creacionOedicion = 1
    return render (request=request, template_name="../templates/crear_categoria.html", context={"tipoAccion":creacionOedicion,"categoria_form":form})
 

@login_required(login_url='/cuentas/login/')
def editar_categoria(request, id):

    obj = get_object_or_404(Categoria, id = id) 

    form = CategoriasForm(request.POST or None, instance = obj)
    
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/categorias")
        
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()
    creacionOedicion = 0
    return render(request, "crear_categoria.html", context={"tipoAccion":creacionOedicion,"categoria_form":form})
