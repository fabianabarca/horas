from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import AreasForm, AreasForm
from proyectos.models import Area
from proyectos.models import Proyecto
from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time

# Create your views here.


@login_required(login_url='/cuentas/ingreso/')
def areas_request(request):
    areas_list = Area.objects.all()
    if request.method == "POST":
        if request.POST.get('deleteButton'):
            deleteButtonItemValue = request.POST.getlist('deleteButton')
            obj = Area(id=deleteButtonItemValue[0])
            Area.objects.filter(id=deleteButtonItemValue[0]).update(
                enPapelera='True')

        return HttpResponseRedirect("/areas")

    return render(request=request, template_name="../templates/areas.html", context={"areas": areas_list})


@login_required(login_url='/cuentas/ingreso/')
def crear_area(request):

    if request.method == "POST":
        form = AreasForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/areas")

    form = AreasForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()
    
    # Acción: editar
    crear = True

    # Contexto
    context = {
        "crear": crear, 
        "area_form": form,
    }

    return render(request, "crear_area.html", context)


@login_required(login_url='/cuentas/ingreso/')
def editar_area(request, id):

    area = get_object_or_404(Area, id=id)

    form = AreasForm(request.POST or None, instance=area)

    # Acción cuando el formulario es válido
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/areas")

    # Ocultar la información de papelera
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # Acción: editar
    crear = False

    # Contexto
    context = {
        "crear": crear, 
        "area_form": form,
        "area": area,
    }

    return render(request, "crear_area.html", context)
