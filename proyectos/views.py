from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import AreasForm, ProyectosForm, ObjetivosForm, FiltrosProyectoForm
from proyectos.models import Area
from proyectos.models import Proyecto
from proyectos.models import Objetivo
from django.contrib.auth.decorators import login_required
from django import forms
import time

# Create your views here.

'''Menú de funciones

- Lista de proyectos (def proyectos --> proyectos.html)
- Crear proyecto (def crear_proyecto --> crear_proyecto.html)
- Editar proyecto (def editar_proyecto --> crear_proyecto.html, con datos)

- Crear objetivo (def crear_objetivo --> crear_objetivo.html)
- Editar objetivo (def crear_objetivo --> crear_objetivo.html, con datos)

'''


@login_required(login_url='/cuentas/ingreso/')
def proyectos(request):
    '''
    Recopila todos los proyectos para desplegarlos
    en una tabla con la lista de proyectos (que no
    están en papelera). Además, crea un formulario 
    para filtrar los proyectos según categorías.
    '''

    # Obtiene la lista de proyectos
    proyectos = Proyecto.objects.all().filter(enPapelera=False)

    # Obtiene lista de areas que no estan la papelera
    areas = Area.objects.all().filter(enPapelera=False)

    # Obtiene lista de objetivos que no estan la papelera
    objetivos = Objetivo.objects.all().filter(enPapelera=False)

    # Formulario para los filtros
    if request.method == "POST":

        # Crea el filtro para la tabla de proyectos
        form = FiltrosProyectoForm(request.POST or None)

        if form.is_valid():
            if form.cleaned_data.get('nombre'):
                proyectos = proyectos.filter(
                    nombre__contains=form.cleaned_data.get('nombre'))
            if form.cleaned_data.get('descripcion'):
                proyectos = proyectos.filter(
                    descripcion__contains=form.cleaned_data.get('descripcion'))
            if form.cleaned_data.get('profesor'):
                proyectos = proyectos.filter(
                    profesor=form.cleaned_data.get('profesor'))
            if form.cleaned_data.get('area'):
                proyectos = proyectos.filter(
                    area=form.cleaned_data.get('area'))
            if form.cleaned_data.get('ubicacion'):
                proyectos = proyectos.filter(
                    ubicacion__contains=form.cleaned_data.get('ubicacion'))

        # Crea el botón de enviar a papelera
        if request.POST.get('deleteButton'):
            deleteButtonItemValue = request.POST.getlist('deleteButton')
            obj = Proyecto(id=deleteButtonItemValue[0])
            Proyecto.objects.filter(
                id=deleteButtonItemValue[0]).update(enPapelera='True')

        # return HttpResponseRedirect("/proyectos")

    # Crea el objeto para enviar
    form = FiltrosProyectoForm()

    context = {
        "areas": areas,
        "objetivos": objetivos,
        "proyectos": proyectos,
        "filtros_form": form
    }

    return render(request, "proyectos.html", context)


@login_required(login_url='/cuentas/ingreso/')
def crear_proyecto(request):
    '''
    Crea formulario para recopilar los datos
    de un nuevo proyecto.
    '''

    # Crea formulario con todos los campos de información
    if request.method == "POST":
        form = ProyectosForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/proyectos")

    # Utiliza el formulario de proyectos
    form = ProyectosForm()

    # Ocula los campos de papelera
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # Quita del formulario las áreas borradas
    areas_noborrados = Area.objects.all()
    areas_noborrados = areas_noborrados.filter(enPapelera=False)
    form.fields["area"].queryset = areas_noborrados

    # Crear o editar
    crear = True

    context = {
        "crear": crear,
        "proyecto_form": form
    }

    return render(request, "crear_proyecto.html", context)


@login_required(login_url='/cuentas/ingreso/')
def editar_proyecto(request, id):
    '''
    Carga un formulario con los datos de un 
    proyecto ya registrado para edición.
    '''

    # Recupera la información del proyecto seleccionado
    proyecto = get_object_or_404(Proyecto, id=id)

    # Carga el formulario con la instancia del proyecto
    form = ProyectosForm(request.POST or None, instance=proyecto)

    # Oculta los campos de papelera
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # Quita del formulario los proyectos asociados con
    # las áreas que están en papelera
    areas_noborrados = Area.objects.all()
    areas_noborrados = areas_noborrados.filter(enPapelera=False)
    form.fields["area"].queryset = areas_noborrados

    # Valida el formulario y lo guarda
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/proyectos")

    # Crear o editar
    crear = False

    context = {
        "crear": crear,
        "proyecto_form": form,
        "proyecto": proyecto,
    }

    return render(request, "crear_proyecto.html", context)


@login_required(login_url='/cuentas/ingreso/')
def crear_objetivo(request):

    if request.method == "POST":
        form = ObjetivosForm(request.POST)
        if form.is_valid():
            form.save()
            time.sleep(1)  # para que mensaje de que se creo pueda verse

            return HttpResponseRedirect("/proyectos")

    form = ObjetivosForm()
    form.fields['general'].widget = forms.HiddenInput()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    proyectos_noborrados = Proyecto.objects.all()
    proyectos_noborrados = proyectos_noborrados.filter(enPapelera=False)
    form.fields["proyecto"].queryset = proyectos_noborrados

    crear = True

    context = {
        "tipoAccion": crear,
        "objetivo_form": form
    }

    return render(request, "crear_objetivo.html", context)


@login_required(login_url='/cuentas/ingreso/')
def editar_objetivo(request, id):

    obj = get_object_or_404(Objetivo, id=id)

    form = ObjetivosForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/objetivos")

    form.fields['general'].widget = forms.HiddenInput()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    proyectos_noborrados = Proyecto.objects.all()
    proyectos_noborrados = proyectos_noborrados.filter(enPapelera=False)
    form.fields["proyecto"].queryset = proyectos_noborrados

    creacionOedicion = 0
    return render(request, "crear_objetivo.html", context={"tipoAccion": creacionOedicion, "objetivo_form": form})


def proyectosInfo(request):
    listaProyectos = Proyecto.objects.all()

    return render(request=request,  template_name="../templates/proyectosInfo.html", context={"listaProyectos": listaProyectos})


def proyecto(request, id):
    proyecto = Proyecto.objects.filter(id=id)
    proyectoHoras = 1
    objetivos = proyecto[0].objetivo_set.filter(enPapelera=False)

    listatareas = []
    for objetivo in objetivos:
        tareas = objetivo.tarea_set.filter(enPapelera=False)
        for tarea in tareas:
            listatareas.append(tarea.nombre)

    return render(request, "proyecto.html", context={"proyecto": proyecto[0],
                                                     "proyectoHoras": proyectoHoras, "objetivos": objetivos, "tareas": listatareas})
