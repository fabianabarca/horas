from django.shortcuts import render
from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from dashboard.models import *
from django.contrib.auth.decorators import login_required
import time
from cuentas.models import *
from actividades.models import Actividad
from proyectos.models import Proyecto
from tareas.models import Tarea
import datetime


# Create your views here.

@login_required(login_url='/cuentas/login/')
def resumen(request):
    '''Recopilación de información y creación de gráficas
    para el resumen de actividades de estudiantes.
    '''
    estudiante_actual = Estudiante.objects.get(user=request.user)

    # Desde aqui se procesa la barra de progreso de horas por estudiante
    my_actividades_list = Actividad.objects.raw(
        'SELECT id, estudiante_id, horas, enPapelera FROM actividades_actividad where estudiante_id == ' + str(estudiante_actual.id)+" AND enPapelera==false")
    horasTotalesPorEstudiante = 0

    for actividad in my_actividades_list:

        if actividad.estado == "A":
            horasTotalesPorEstudiante += actividad.horas

    # horasTotalesPorEstudiante=30  #para pruebas
    porcentaje = (100 / 300) * horasTotalesPorEstudiante
    porcentajeWidth = int(porcentaje)

    # Desde aqui se procesa la barra de progreso de dias del TCU por estudiante
    current_datetime = datetime.date.today()
    inicioTCU = estudiante_actual.fechaInicioTCU
    finalTCU = estudiante_actual.fechaFinTCU

    diasRestantesDelTCU = finalTCU - current_datetime

    diasDesdeInicioTCU = current_datetime - inicioTCU
    diasTCU = diasDesdeInicioTCU.days

    totalDiasTCU = 365

    porcentajeDaysYear = (100 / totalDiasTCU) * diasTCU
    porcentajeWidthDaysYear = int(porcentajeDaysYear)

    # Datos para pie chart y horizontal bar chart con relación proyectos y actividades
    labels = []
    data = []
    dictCantidadActividadesHoras = {}
    querysetProyectos = Proyecto.objects.filter(enPapelera=False)

    for proyecto in querysetProyectos:

        totalActividadesHorasPorProyecto = 0
        querysetObjetivos = proyecto.objetivo_set.filter(enPapelera=False)

        for objetivo in querysetObjetivos:
            querysetTareas = objetivo.tarea_set.filter(enPapelera=False)
            # cambioMetasATareas
            for tarea in querysetTareas:
                querysetActividades = tarea.actividad_set.filter(
                    enPapelera=False)

                for actividad in querysetActividades:
                    totalActividadesHorasPorProyecto = totalActividadesHorasPorProyecto + actividad.horas

        # labels.append(proyecto.nombre)
        # tquery=Tarea.objects.filter(proyecto=proyecto)
        # data.append(tquery.count)

        dictCantidadActividadesHoras[proyecto.nombre] = totalActividadesHorasPorProyecto

    sorteddictCantidadActividades = sorted(
        dictCantidadActividadesHoras.items(), key=lambda x: x[1], reverse=True)

    for element in sorteddictCantidadActividades:
        labels.append(element[0])
        data.append(element[1])

    # Listas con los colores para los graficos desplegados
    colorList = color_list(dictCantidadActividadesHoras)

    # A partir de aquí datos para grafico de barras ranking de estudiantes por actividades
    labelsRankingEstudiante = []
    dataRankingEstudiante = []
    mapEstudianteCantidadActividades = {}
    rankingEstudiantesList = Estudiante.objects.filter(user__is_staff=False)

    for estudiante in rankingEstudiantesList:
        horasActividades = Actividad.objects.filter(
            estudiante=estudiante, enPapelera=False)
        horasEstudiante = 0
        for actividad in horasActividades:
            horasEstudiante = horasEstudiante + actividad.horas
        mapEstudianteCantidadActividades[estudiante.user.username] = horasEstudiante

    sortedmapEstudianteCantidadActividades = sorted(
        mapEstudianteCantidadActividades.items(), key=lambda x: x[1], reverse=True)

    for element in sortedmapEstudianteCantidadActividades:
        labelsRankingEstudiante.append(element[0])
        dataRankingEstudiante.append(element[1])

    colorListRankingEstudiante = color_list(mapEstudianteCantidadActividades)

    context = {
        "progreso": horasTotalesPorEstudiante,
        "porcentaje": porcentaje,
        "width": porcentajeWidth,
        "diasTCU": diasTCU,
        "inicioTCU": inicioTCU,
        "finalTCU": finalTCU,
        "totalDiasTCU": totalDiasTCU,
        "porcentajeDaysYear": porcentajeDaysYear,
        "porcentajeWidthDaysYear": porcentajeWidthDaysYear,
        'labels': labels, 'data': data,
        'colorList': colorList,
        'labelsRankingEstudiante': labelsRankingEstudiante,
        'dataRankingEstudiante': dataRankingEstudiante,
        'colorListRankingEstudiante': colorListRankingEstudiante,
    }

    return render(request, 'resumen.html', context)


@login_required(login_url='/cuentas/login/')
def panel(request):

    estudiantes_list = Estudiante.objects.all()

    context = {
        "estudiantes": estudiantes_list,
    }

    return render(request, 'panel.html', context)


def color_list(listaCantidadMiembros):
    colorList = []

    alphaInitial = 1
    opasityDecreaseRange = 0.2
    r = str(159)
    g = str(90)
    b = str(253)

    alpha = alphaInitial
    count = 0
    for i in listaCantidadMiembros:
        alpha = alpha - (count)
        color = 'rgba(' + r + ',' + g + ',' + b + ',' + str(alpha) + ')'
        colorList.append(color)
        count = count + opasityDecreaseRange

    return colorList
