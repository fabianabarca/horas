from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from cuentas.models import Estudiante
from horas.forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from actividades.models import Actividad
from tareas.models import Tarea
from proyectos.models import Proyecto, Objetivo
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import time


# Create your views here.
@login_required(login_url='/cuentas/ingreso/')
def actividades(request):

    list_of_inputs = request.POST.getlist('inputs')
    boton_activo = 'T'
    # Obtener lista de actividades para profesores o cada estudiante
    if request.user.is_staff:
        actividades = Actividad.objects.filter(enPapelera=False)
    else:
        estudiante_actual = Estudiante.objects.get(user=request.user)
        actividades = Actividad.objects.filter(
            estudiante=estudiante_actual,
            enPapelera=False,
            )

    # Procesar el formulario de filtros
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

        #Los siguientes 3 If BLOCKS son para detectar cuándo el usuario
        #dio click a algún botón del div de la línea 47 de actividades.html,
        #los cuales son usados para separar las actividades por estados.
        if request.POST.get('aprobadas'):
            boton_activo = 'A'

        if request.POST.get('rechazadas'):
            boton_activo = 'R'

        if request.POST.get('revision'):
            boton_activo = 'P'
        
        if boton_activo is not 'T':
            actividades = actividades.filter(estado= boton_activo).order_by('-fecha')

        if form.is_valid():
            if form.cleaned_data.get('estudiante'):
                actividades = actividades.filter(
                    estudiante=form.cleaned_data.get('estudiante'))
            # if form.cleaned_data.get('proyecto'):
                #actividades =  actividades.filter(proyecto = form.cleaned_data.get('proyecto'))
            if form.cleaned_data.get('tarea'):
                actividades = actividades.filter(
                    tarea=form.cleaned_data.get('tarea'))
            if form.cleaned_data.get('estado'):
                actividades = actividades.filter(
                    estado=form.cleaned_data.get('estado'))
            if form.cleaned_data.get('descripcion'):
                actividades = actividades.filter(
                    descripcion__contains=form.cleaned_data.get('descripcion'))
            if form.cleaned_data.get('fecha_inicio') or form.cleaned_data.get('fecha_final'):
                actividades = actividades.filter(fecha__range=[form.cleaned_data.get(
                    'fecha_inicio'), form.cleaned_data.get('fecha_final')])

            # return HttpResponseRedirect("/actividades")

    # Declarar el formulario a utilizar
    form = FiltrosForm()

    # Contexto
    context = {
        "actividades": actividades,
        "filtros_form": form,
        "boton_activo": boton_activo
    }

    return render(request, "actividades.html", context)


@login_required(login_url='/cuentas/ingreso/')
def crear_actividad(request):
    '''
    Registra la información de una nueva actividad con
    N horas asociadas a una tarea.
    '''

    estudiante_actual = Estudiante.objects.get(user=request.user)

    if request.method == "POST":
        form = ActividadesForm(request.POST or None)
        
        # Se obtiene el id del proyecto, objetivo y la tarea seleccionadas por el usuario 
        # con el fin de asignarselos al form y que este se pueda validar.
        proyecto_id = request.POST.get('proyecto')
        objetivo_id = request.POST.get('objetivo')
        tarea_id = request.POST.get('tarea')
        form.fields['proyecto'].choices = [(proyecto_id, proyecto_id)]
        form.fields['objetivo'].choices = [(objetivo_id, objetivo_id)]
        form.fields['tarea'].choices = [(tarea_id, tarea_id)]
        
        if form.is_valid():
            post = form.save(commit=False)
            post.estudiante = estudiante_actual
            post.save()
            time.sleep(1)  # para que mensaje de que se creo pueda verse
            messages.success(request,"Actividad registrada exitosamente")
            return HttpResponseRedirect("/actividades")
        else:
            print(form.errors.as_data())

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

    crear = True
    context = {
        "crear": crear,
        "form": form,
    }
    return render(request, "crear_actividad.html", context)


@login_required(login_url='/cuentas/ingreso/')
def editar_actividad(request, id):

    actividad = get_object_or_404(Actividad, id=id)
    
    form = ActividadesForm(request.POST or None, instance=actividad,
                             initial={'area': actividad.tarea.objetivo.proyecto.area.id})
    
    #Setea valores originales del form en los campos proyecto, objetivo y tarea
    form.fields['proyecto'].choices = [( actividad.tarea.objetivo.proyecto.id,  actividad.tarea.objetivo.proyecto.nombre)]
    form.fields['objetivo'].choices = [(actividad.tarea.objetivo.id, actividad.tarea.objetivo.descripcion)]
    form.fields['tarea'].choices = [(actividad.tarea.id, actividad.tarea.nombre)]
    
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
    
    if request.POST:
        #Corrige fallo de form inválido.
        proyecto_id = request.POST.get('proyecto')
        objetivo_id = request.POST.get('objetivo')
        tarea_id = request.POST.get('tarea')
        form.fields['proyecto'].choices = [(proyecto_id, proyecto_id)]
        form.fields['objetivo'].choices = [(objetivo_id, objetivo_id)]
        form.fields['tarea'].choices = [(tarea_id, tarea_id)]
        
        if form.is_valid():
            form.save()
            messages.success(request,"Cambios guardados exitosamente")
            return HttpResponseRedirect("/actividades")

    crear = False
    context = {
        "crear": crear,
        "form": form,
        "actividad": actividad
    }
    return render(request, "crear_actividad.html", context)


def load_proyectos(request):
    area_id = request.GET.get('area')
    proyectos = Proyecto.objects.filter(area=area_id, enPapelera=False).order_by('nombre')
    return render(request, '../templates/proyectoActividad_dropdown_list_options.html', {'proyectos': proyectos})

# AJAX
def load_objetivos(request):
    proyecto_id = request.GET.get('proyecto')
    objetivos = Objetivo.objects.filter(proyecto=proyecto_id, enPapelera=False)
    return render(request, '../templates/objetivoActividad_dropdown_list_options.html', {'objetivos': objetivos})


# AJAX
def load_tareas(request):
    objetivo_id = request.GET.get('objetivo')
    tareas = Tarea.objects.filter(objetivo=objetivo_id, enPapelera=False).order_by('nombre')
    return render(request, '../templates/tareaActividad_dropdown_list_options.html', {'tareas': tareas})
