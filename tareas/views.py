from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from tareas.models import *
from proyectos.models import *
from cuentas.models import Estudiante
from horas.forms import TareasForm, FiltrosTareaForm
from django.contrib.auth.decorators import login_required
import time
from django.core.mail import send_mail

# Create your views here.


@login_required(login_url='/cuentas/ingreso/')
def tareas(request):
    '''Despliega una lista de tareas con su información.

    Si el usuario es estudiante, separa las tareas en dos 
    tablas: una con las tareas asignadas, y otra con todas
    las tareas disponibles.
    '''

    lista_tareas = Tarea.objects.filter(enPapelera=False)

    # Creación de tabla de tareas asignadas a estudiante actual
    if request.user.is_staff == False:
        estudiante_actual = Estudiante.objects.get(user=request.user)
        mis_tareas = lista_tareas.filter(estudiante=estudiante_actual)
        tareas = lista_tareas.exclude(estudiante=estudiante_actual)
    else:
        tareas = lista_tareas

    # Configura el filtrado de la tabla
    if request.method == "POST":
        form = FiltrosTareaForm(request.POST or None)
        if request.POST.get('deleteButton'):
            deleteButtonItemValue = request.POST.getlist('deleteButton')
            obj = Tarea(id=deleteButtonItemValue[0])
            Tarea.objects.filter(id=deleteButtonItemValue[0]).update(
                enPapelera='True')

        # Parte de implementación de asignación de tareas por boton
        if request.POST.get('assignButton'):
            asignButtonItemValue = request.POST.getlist('assignButton')
            obj = Tarea(id=asignButtonItemValue[0])
            tareaAsignar = Tarea.objects.filter(id=asignButtonItemValue[0])

            estudiantesAsignadosATareaActual = tareaAsignar[0].estudiante.all()
            for estudiante in estudiantesAsignadosATareaActual:
                asignaciones_list = AsignacionesEnviadas.objects.all()
                boolYaFueAsignadoAntes = False
                print("estudiante: " + estudiante.user.first_name)
                for asignacion in asignaciones_list:

                    if (asignacion.estudiante == estudiante):
                        # print(asignacion.estudiante)
                        print("tarea ya asignada: "+asignacion.tarea.nombre)
                        if (asignacion.tarea == tareaAsignar[0]):
                            boolYaFueAsignadoAntes = True
                            print("no se le envió correo a " +
                                  estudiante.user.first_name)

                if (not boolYaFueAsignadoAntes):
                    ae = AsignacionesEnviadas(
                        estudiante=estudiante, tarea=tareaAsignar[0])
                    ae.save()
                    # print(AsignacionesEnviadas.objects.all())

                    # aqui se manda el correo

                    send_mail(
                        'Asignación de tarea',
                        'Se te asigno la tarea: ' +
                        tareaAsignar[0].nombre + '\n\n'
                        + 'Descripción: ' +
                        tareaAsignar[0].descripcion + '\n\n'
                        + 'Del proyecto: ' +
                        tareaAsignar[0].objetivo.proyecto.nombre + '\n\n',
                        'testertesrter3@gmail.com',
                        [estudiante.user.email],
                        fail_silently=False,
                    )
                    print("Se envió correo a " + estudiante.user.first_name)
                    print(estudiante.user.email)

        if form.is_valid():
            if form.cleaned_data.get('nombre'):
                lista_tareas = lista_tareas.filter(
                    nombre__contains=form.cleaned_data.get('nombre'))
            if form.cleaned_data.get('estudiante'):
                lista_tareas = lista_tareas.filter(
                    estudiante=form.cleaned_data.get('estudiante'))
            if form.cleaned_data.get('descripcion'):
                lista_tareas = lista_tareas.filter(
                    descripcion__contains=form.cleaned_data.get('descripcion'))
            if form.cleaned_data.get('objetivo'):
                lista_tareas = lista_tareas.filter(
                    objetivo=form.cleaned_data.get('objetivo'))
            if form.cleaned_data.get('area'):
                lista_tareas = lista_tareas.filter(
                    objetivo__proyecto__area=form.cleaned_data.get('area'))

        # return HttpResponseRedirect("/tareas")

    form = FiltrosTareaForm()

    context = {
        "mis_tareas": mis_tareas if request.user.is_staff == False else '',
        "tareas": tareas,
        "filtros_form": form
    }

    return render(request, "tareas.html", context)


@login_required(login_url='/cuentas/ingreso/')
def crear_tarea(request):

    if request.method == "POST":
        form = TareasForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/tareas")

    form = TareasForm()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    tareas_noborradas = Tarea.objects.filter(enPapelera=False)
    form.fields["tareaSuperior"].queryset = tareas_noborradas

    # para filtrar usuarios y que solo se puedan asignar estudiantes a tareas
    estudiantes_nostaff = Estudiante.objects.filter(user__is_staff=False)
    form.fields["estudiante"].queryset = estudiantes_nostaff

    crear = True
    context = {
        "crear": crear,
        "tarea_form": form
    }

    return render(request, "crear_tarea.html", context)


@login_required(login_url='/cuentas/ingreso/')
def editar_tarea(request, id):

    tarea = get_object_or_404(Tarea, id=id)

    form = TareasForm(request.POST or None, instance=tarea)
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    # para filtrar edicion y que no aparezcan en seleccion lo que esta en la papelera
    tareas_noborradas = Tarea.objects.filter(enPapelera=False)
    form.fields["tareaSuperior"].queryset = tareas_noborradas

    if form.is_valid():

        # Para enviar correos a estudiantes nuevamente asignados
        lista_tareas = Tarea.objects.all()
        tareaAEditar = lista_tareas.filter(id=id)

        estudiantesActualesEnTarea = tareaAEditar[0].estudiante.all()

        # Parte de código que al asignar estudiante nuevo al crear o editar una tarea
        # manda correo de asignación para los estudiantes nuevos y evita mandar a estudiantes ya asignados
        # previamente a la tarea, con ayuda del modelo creado en la base de datos AsignacionesEnviadas
        '''
        for estudianteForm in form.cleaned_data.get('estudiante'):
            mandarCorreo=True
            for estudiante in estudiantesActualesEnTarea:
                #print(estudiante)
                if(estudianteForm == estudiante):
                    #print("se encontro   "+ estudianteForm.user.first_name)
                    mandarCorreo=False
                    
                #else:
                    #print("no se encontro: "+ estudianteForm.user.first_name)
                    
            if (mandarCorreo):
                    asignaciones_list = AsignacionesEnviadas.objects.all()
                    boolYaFueAsignadoAntes=False
                    for asignacion in asignaciones_list:
                        if(asignacion.estudiante==estudianteForm):
                                 boolYaFueAsignadoAntes=True
                                 #print("no se le envió correo a "+ estudianteForm.user.first_name)

                           
                    if (not boolYaFueAsignadoAntes):
                        ae = AsignacionesEnviadas(estudiante=estudianteForm,tarea=tareaAEditar[0])
                        ae.save()
                        #print(AsignacionesEnviadas.objects.all())
                        #print("se envió correo a "+ estudianteForm.user.first_name)

                    
                        send_mail(
                                            'Asignación de tarea',
                                            'Se te asigno la tarea: ' + tareaAEditar[0].nombre +'\n\n'
                                            + 'Descripción: '+ tareaAEditar[0].descripcion  +'\n\n'
                                            + 'Del proyecto: '+ tareaAEditar[0].proyecto.nombre  +'\n\n'
                                            ,
                                            'testertesrter3@gmail.com',
                                            [estudianteForm.user.email],
                                            fail_silently=False,
                                )
        '''
        # para cambio de objetivos de tareas subordinadas si tarea las tiene
        tareasSubordinadas = tareaAEditar[0].tarea_set.all()

        # para asignar objetivo de tarea superior a tareas subordinadas
        if tareasSubordinadas:
            cambio_objetivos_tareasrecursivas(form, tareaAEditar[0])

        form.save()
        return HttpResponseRedirect("/tareas")

    # para no incluir en opciones de tareas superiores a subordinas o a si mismo
    tareaAEditar = Tarea.objects.filter(id=id)
    listaTareasNoSubordinadas = []
    listaTareasNoSubordinadas = seleccion_tarea_superior_tareasrecursivas(
        form, tareaAEditar[0], listaTareasNoSubordinadas)

    querysetTareasNoSubordinadas = Tarea.objects.all().exclude(
        id__in=listaTareasNoSubordinadas)
    querysetTareasNoSubordinadas = querysetTareasNoSubordinadas.exclude(id=id)
    form.fields["tareaSuperior"].queryset = querysetTareasNoSubordinadas

    crear = True
    context = {
        "crear": crear,
        "tarea_form": form,
        "tarea": tarea,
    }

    return render(request, "crear_tarea.html", context)

# para cambio de objetivos de tareas subordinadas si tarea las tiene


def cambio_objetivos_tareasrecursivas(form, tareaAEditar):
    tareasSubordinadas = tareaAEditar.tarea_set.all()
    # print("nivel")
    # print(tareasSubordinadas)

    if tareasSubordinadas:
        for tarea in tareasSubordinadas.all():
            # print("nivelrec")
            # print(tareaAEditar.objetivo)
            tarea.objetivo = form.cleaned_data.get('objetivo')
            tarea.save()
            cambio_objetivos_tareasrecursivas(form, tarea)

# para solo seleccion de tareas no subordinadas como tarea superior


def seleccion_tarea_superior_tareasrecursivas(form, tareaAEditar, listaTareasNoSubordinadas):
    tareasSubordinadas = tareaAEditar.tarea_set.all()
    # print("nivel")
    # print(tareasSubordinadas)

    if tareasSubordinadas:
        for tarea in tareasSubordinadas.all():
            listaTareasNoSubordinadas.append(tarea.id)
            # print("nivelrec")
            # print(tarea.nombre)

            listaTareasNoSubordinadas = seleccion_tarea_superior_tareasrecursivas(
                form, tarea, listaTareasNoSubordinadas)
    return listaTareasNoSubordinadas

# AJAX


def load_objetivos(request):
    tarea_id = request.GET.get('tarea_id')
    # print(tarea_id)

    if (tarea_id == ''):
        objetivos = Objetivo.objects.filter(enPapelera=False)
    else:
        objetivos = Objetivo.objects.filter(tarea__id=tarea_id)
    # print(objetivos)
    return render(request, '../templates/objetivo_dropdown_list_options.html', {'objetivos': objetivos})
    # return JsonResponse(list(objetivos.values('id', 'nombre')), safe=False)
