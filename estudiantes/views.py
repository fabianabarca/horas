from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from cuentas.models import *
from django.contrib.auth.models import User
from horas.forms import EstudiantesForm
from actividades.models import Actividad
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@login_required(login_url='/cuentas/ingreso/')
def profesores(request):
    profesores = Estudiante.objects.all().filter(user__is_staff=True)
    print(profesores)
    context = { "profesores": profesores, }

    return render(request, "profesores.html", context)    

@login_required(login_url='/cuentas/ingreso/')
def estudiantes(request):
    '''Recopila la información de todos los estudiantes
    registrados para mostrarla en una lista.
    '''
    estudiantes = Estudiante.objects.all().filter(user__is_staff=False, estado='A')

    if request.user.is_staff:
        actividades = Actividad.objects.all()
        estudiantesFinalizados = Estudiante.objects.all().filter(user__is_staff=False, estado='F')
        estudiantesOtrosEstados = Estudiante.objects.all().filter(user__is_staff=False).exclude(estado = 'F').exclude(estado = 'A')
        horasEstudianteslist = []
        porcentajeEstudianteslist = []
        porcentajeWidthEstudianteslist = []
        
        horasTotalesPorEstudiante = 0
        for estudiante in estudiantes:

            horasTotalesPorEstudiante = 0
            for actividad in actividades:

                if actividad.estudiante.user.username == estudiante.user.username:
                    if actividad.estado == "A":
                        horasTotalesPorEstudiante += actividad.horas

            horasEstudianteslist.append(horasTotalesPorEstudiante)
            porcentaje = round((100 / 300) * horasTotalesPorEstudiante)
            porcentajeEstudianteslist.append(porcentaje)
            porcentajeWidthEstudianteslist.append(int(porcentaje))

        informacion = zip(estudiantes, horasEstudianteslist,
                    porcentajeEstudianteslist, porcentajeWidthEstudianteslist)
        context = {
            "informacion": informacion,
            "finalizados": estudiantesFinalizados,
            "otrosEstados": estudiantesOtrosEstados
        }

    else:
        horasEstudianteslist = [1] * len(estudiantes)
        porcentajeEstudianteslist = [1] * len(estudiantes)
        porcentajeWidthEstudianteslist = [1] * len(estudiantes)
        informacion = zip(estudiantes, horasEstudianteslist,
                    porcentajeEstudianteslist, porcentajeWidthEstudianteslist)
        context = {
            "informacion": informacion,
        }

    return render(request, "estudiantes.html", context)


@staff_member_required(login_url='/cuentas/ingreso/')
def editar_estudiante(request, id):

    estudiante = get_object_or_404(Estudiante, id=id)

    form = EstudiantesForm(request.POST or None, instance=estudiante)
    form.fields['user'].widget = forms.HiddenInput()
    form.fields['carrera'].widget = forms.HiddenInput()
    form.fields['fecha_inicio'].widget = forms.HiddenInput()
    form.fields['fecha_final'].widget = forms.HiddenInput()

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/estudiantes")

    # Acción: editar
    crear = False

    # Contexto
    context = {
        "crear": crear,
        "estudiante_form": form,
        "estudiante": estudiante,
    }

    return render(request, "editar_estudiante.html", context)


@login_required(login_url='/cuentas/ingreso/')
def equipos(request):
    '''Lista de equipos de estudiantes.

    Incluye información como el nombre y descripción.
    '''
    context = {
        'saludo': 'hola',
    }
    return render(request, 'equipos.html', context)

@staff_member_required(login_url='/cuentas/ingreso/')
def estudiante(request, id_ucr):
    '''Información personal de cada estudiante.

    Incluye información de las horas registradas.
    '''
    usuario = get_object_or_404(User, username=id_ucr)
    estudiante = Estudiante.objects.get(user=usuario) # Estudiante actual a trabajar
    
    fecha_hoy = datetime.date.today() # Fecha del día actual de tipo fecha
    inicio_TCU = estudiante.fecha_inicio # Fecha de inicio del TCU del estudiante actual
    dias_desde_inicio_TCU = (fecha_hoy - inicio_TCU).days # Días transcurridos desde el inicio del TCU para el estudiante
    porcentaje_tiempo = (100 / 365) * dias_desde_inicio_TCU # Porcentaje de avance del tiempo disponible, valor mínimo 0.01
    porcentaje_tiempo_width = int(porcentaje_tiempo) # Entero del porcentaje de avance del tiempo disponible para el widget

    # Desde aqui se procesa la barra de progreso de horas por estudiante #
    my_actividades_list = Actividad.objects.raw( # Lista de actividades del estudiante
        'SELECT id, estudiante_id, horas, enPapelera FROM actividades_actividad where estudiante_id == ' + str(estudiante.id)+" AND enPapelera==false")
    horas_totales_por_estudiante = 0 # Horas totales del estudiante actual

    # Calcula la sumatoria de horas entre todas las actividades del estudiante
    for actividad in my_actividades_list:
        if actividad.estado == "A":
            horas_totales_por_estudiante += actividad.horas

    # Variables para los datos de las barras de widgets horas e índice
    porcentaje_horas = (100 / 300) * horas_totales_por_estudiante # Porcentaje de avance de horas, valor mínimo 0.01
    porcentaje_horas_width = int(porcentaje_horas) # Entero del porcentaje de avance de horas
    if(porcentaje_horas == 0): # Cambia el porcentaje de horas si es 0 al mínimo para mantener el índice correcto
        porcentaje_horas = 0.01
    if(porcentaje_tiempo == 0): # Cambia el porcentaje de tiempo si es 0 al mínimo para evitar errores de cálculo
        porcentaje_tiempo = 0.01
    indice_avance_total = porcentaje_horas / porcentaje_tiempo # Índice de avance con todos los decimales
    indice_avance = round(indice_avance_total, 2) # Índice de avance redondeado a dos decimales
    indice_avance_width = int(100 * indice_avance) # Porcentaje de la barra para mostrar el índice de avance

    context = {
        'estudiante': estudiante,
        "horas_totales_por_estudiante": horas_totales_por_estudiante, # Horas totales del estudiante actual
        "dias_desde_inicio_TCU": dias_desde_inicio_TCU,
        "porcentaje_horas_width": porcentaje_horas_width, # Entero del porcentaje de avance de horas
        "porcentaje_tiempo_width": porcentaje_tiempo_width, # Entero del porcentaje de avance del tiempo disponible para el widget
        "indice_avance": indice_avance, # Índice de avance redondeado a dos decimales
        "indice_avance_width": indice_avance_width, # Porcentaje de la barra para mostrar el índice de avance
    }

    return render(request, 'estudiante.html', context)
