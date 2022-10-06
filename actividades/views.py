from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from cuentas.models import Estudiante
from horas.forms import *
from django.contrib.auth.models import User
from actividades.models import Actividad
from tareas.models import Tarea
from proyectos.models import Proyecto
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import time


# Create your views here.
@login_required(login_url='/cuentas/ingreso/')
def actividades_request(request):

    list_of_inputs = request.POST.getlist('inputs')

    is_staff = request.user.is_staff

    # Put the logging info within your django view

    if request.user.is_staff:
        actividades_list = Actividad.objects.all()

    else:
        estudiante_actual = Estudiante.objects.get(user=request.user)
        actividades_list = Actividad.objects.filter(
            estudiante=estudiante_actual)

    if request.method == "POST":
        form = FiltrosForm(request.POST or None)
        list_of_inputs = request.POST.getlist('inputs')

        if request.POST.get('aprobar'):
            for input in list_of_inputs:
                Actividad.objects.filter(
                    id=input.replace('/', '')).update(estado='A')

        if request.POST.get('rechazar'):
            for input in list_of_inputs:
                Actividad.objects.filter(
                    id=input.replace('/', '')).update(estado='R')

        if request.POST.get('deleteButton'):
            deleteButtonItemValue = request.POST.getlist('deleteButton')
            Actividad.objects.filter(
                id=deleteButtonItemValue[0]).update(enPapelera='True')

        if form.is_valid():
            if form.cleaned_data.get('estudiante'):
                actividades_list = actividades_list.filter(
                    estudiante=form.cleaned_data.get('estudiante'))
            # if form.cleaned_data.get('proyecto'):
                #actividades_list =  actividades_list.filter(proyecto = form.cleaned_data.get('proyecto'))
            if form.cleaned_data.get('tarea'):
                actividades_list = actividades_list.filter(
                    tarea=form.cleaned_data.get('tarea'))
            if form.cleaned_data.get('estado'):
                actividades_list = actividades_list.filter(
                    estado=form.cleaned_data.get('estado'))
            if form.cleaned_data.get('descripcion'):
                actividades_list = actividades_list.filter(
                    descripcion__contains=form.cleaned_data.get('descripcion'))
            if form.cleaned_data.get('fecha_inicio') or form.cleaned_data.get('fecha_final'):
                actividades_list = actividades_list.filter(fecha__range=[form.cleaned_data.get(
                    'fecha_inicio'), form.cleaned_data.get('fecha_final')])

            # return HttpResponseRedirect("/actividades")
    form = FiltrosForm()

    return render(request=request, template_name="../templates/actividades.html", context={"actividades": actividades_list, "filtros_form": form})


@login_required(login_url='/cuentas/ingreso/')
def crear_actividad(request):

    estudiante_actual = Estudiante.objects.get(user=request.user)

    if request.method == "POST":
        form = ActividadesForm(request.POST or None)

        if form.is_valid():
            post = form.save(commit=False)
            post.estudiante = estudiante_actual
            post.save()
            time.sleep(1)  # para que mensaje de que se creo pueda verse
            return HttpResponseRedirect("/actividades")

    form = ActividadesForm()
    form.fields['estado'].widget = forms.HiddenInput()
    form.fields['estudiante'].widget = forms.HiddenInput()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    #proyectos_noborrados = Proyecto.objects.all()
    tareas_noborradas = Tarea.objects.all()

    #proyectos_noborrados=proyectos_noborrados.filter(enPapelera= False)
    tareas_noborradas = tareas_noborradas.filter(enPapelera=False)

    #form.fields["proyecto"].queryset  = proyectos_noborrados
    form.fields["tarea"].queryset = tareas_noborradas

    creacionOedicion = 1
    return render(request=request, template_name="../templates/crear_actividad.html", context={"tipoAccion": creacionOedicion, "form": form})


@login_required(login_url='/cuentas/ingreso/')
def editar_actividad(request, id):

    obj = get_object_or_404(Actividad, id=id)

    form = ActividadesForm(request.POST or None, instance=obj)

    form.fields['estado'].widget = forms.HiddenInput()
    form.fields['estudiante'].widget = forms.HiddenInput()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    #proyectos_noborrados = Proyecto.objects.all()

    tareas_noborradas = Tarea.objects.all()

    #proyectos_noborrados=proyectos_noborrados.filter(enPapelera= False)
    tareas_noborradas = tareas_noborradas.filter(enPapelera=False)

   #form.fields["proyecto"].queryset  = proyectos_noborrados
    form.fields["tarea"].queryset = tareas_noborradas

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/actividades")

    creacionOedicion = 0
    return render(request, "crear_actividad.html", context={"tipoAccion": creacionOedicion, "form": form})


# AJAX
def load_objetivosActividades(request):
    proyecto_id = request.GET.get('proyecto_id')
    # print(proyecto_id)

    if (proyecto_id == ''):
        # print("aqui")

        objetivos = Objetivo.objects.filter(enPapelera=False)
    else:
        # print("aca")

        objetivos = Objetivo.objects.filter(
            proyecto__id=proyecto_id, enPapelera=False)
    # print(objetivos)
    return render(request, '../templates/objetivoActividad_dropdown_list_options.html', {'objetivos': objetivos})
    # return JsonResponse(list(objetivos.values('id', 'nombre')), safe=False)


# AJAX
def load_tareas(request):
    objetivo_id = request.GET.get('objetivo_id')
    # print(tarea_id)

    if (objetivo_id == ''):
        tareas = Tarea.objects.filter(enPapelera=False)
    else:
        tareas = Tarea.objects.filter(
            objetivo__id=objetivo_id, enPapelera=False)
    # print(objetivos)
    return render(request, '../templates/tarea_dropdown_list_options.html', {'tareas': tareas})
    # return JsonResponse(list(objetivos.values('id', 'nombre')), safe=False)
