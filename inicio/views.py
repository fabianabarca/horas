import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.http.response import HttpResponseRedirect
import time
from cuentas.models import *
from actividades.models import Actividad
from cuentas.models import Estudiante
from proyectos.models import Proyecto
import datetime

# Create your views here.

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

@login_required(login_url='/cuentas/ingreso/')
def index(request, id=9999):
    # En caso de que NO se redirige de página Estudiantes, uso el numero 9999 como default al llegar a
    # página Inicio desde login o desde menu de navegación
    if id == 9999:
        id = request.user.id

    # AQUÍ TODO LO QUE HAY QUE PONER EN EL PANEL DE PROFESOR
    if request.user.is_staff:
        estudiantes_list = Estudiante.objects.all()
        numeroEstudiantes=estudiantes_list.filter(user__is_staff=False).count
        proyectos_list = Proyecto.objects.all()
        numeroProyectos=proyectos_list.count

        # Datos para horizontal bar chart con relación proyectos y actividades
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
        rankingIndiceAvance = []
        mapEstudianteCantidadActividades = {}
        rankingEstudiantesList = Estudiante.objects.filter(user__is_staff=False)

        for estudiante in rankingEstudiantesList:
            horasActividades = Actividad.objects.filter(
                estudiante=estudiante, enPapelera=False)
            horasEstudiante = 0
            for actividad in horasActividades:
                horasEstudiante = horasEstudiante + actividad.horas
            mapEstudianteCantidadActividades[estudiante] = horasEstudiante

        sortedmapEstudianteCantidadActividades = sorted(
            mapEstudianteCantidadActividades.items(), key=lambda x: x[1], reverse=True)

        for element in sortedmapEstudianteCantidadActividades:
            labelsRankingEstudiante.append(element[0].user.username)
            dataRankingEstudiante.append(element[1])
            if(element[0].fecha_inicio != None):
                rankingIndiceAvance.append(((100 / 300) * element[1]) / 
                ((100 / 365) * (datetime.date.today()-element[0].fecha_inicio).days))

        colorListRankingEstudiante = color_list(mapEstudianteCantidadActividades)

        inicio = 'panel.html'
        context = {
            "numeroEstudiantes": numeroEstudiantes,
            "numeroProyectos": numeroProyectos,
            "labelsRankingEstudiante": labelsRankingEstudiante,
            "dataRankingEstudiante": dataRankingEstudiante,
            "colorListRankingEstudiante": colorListRankingEstudiante,
            "rankingIndiceAvance":rankingIndiceAvance,
            "labels": labels,
            "data": data,
            "colorList": colorList,
        }
    
    # AQUÍ TODO LO QUE HAY QUE PONER EN EL PANEL DE ESTUDIANTE
    else:
        estudiante_actual = Estudiante.objects.get(user=request.user)

        # Desde aqui se procesa la barra de progreso de dias del TCU por estudiante
        current_datetime = datetime.date.today()
        inicioTCU = estudiante_actual.fecha_inicio
        diasDesdeInicioTCU = current_datetime - inicioTCU
        diasTCU = diasDesdeInicioTCU.days
        totalDiasTCU = 365
        porcentajeDaysYear = (100 / totalDiasTCU) * diasTCU
        porcentajeWidthDaysYear = int(porcentajeDaysYear)

        # Desde aqui se procesa la barra de progreso de horas por estudiante
        my_actividades_list = Actividad.objects.raw(
            'SELECT id, estudiante_id, horas, enPapelera FROM actividades_actividad where estudiante_id == ' + str(estudiante_actual.id)+" AND enPapelera==false")
        horasTotalesPorEstudiante = 0

        for actividad in my_actividades_list:
            if actividad.estado == "A":
                horasTotalesPorEstudiante += actividad.horas

        porcentaje = (100 / 300) * horasTotalesPorEstudiante
        porcentajeWidth = int(porcentaje)
        indiceAvance = round(porcentaje/porcentajeDaysYear,2)
        indiceAvanceW = int(50/1*indiceAvance)

        #Fechas, Horas Calendario
        actividades_calendario= Actividad.objects.raw('SELECT id, estudiante_id, horas, fecha, enPapelera FROM actividades_actividad where estudiante_id == '+ str(estudiante_actual.id)+" AND enPapelera==false AND estado == 'A'")
        horasPorDia = [[0 for i in range(4)] for actividad in actividades_calendario]
        numeroActividades = 0
        for actividad in actividades_calendario:
            if actividad.estado == "A":
                horasPorDia[numeroActividades][0]=actividad.fecha.year
                horasPorDia[numeroActividades][1]=actividad.fecha.month
                horasPorDia[numeroActividades][2]=actividad.fecha.day
                horasPorDia[numeroActividades][3]=actividad.horas
                numeroActividades+=1

        inicio = 'resumen.html'
        context = {
            "progreso": horasTotalesPorEstudiante,
            "width": porcentajeWidth,
            "porcentajeWidthDaysYear": porcentajeWidthDaysYear,
            "indiceAvance":indiceAvance,
            "indiceAvanceW":indiceAvanceW,
            "horasPorDia":json.dumps(horasPorDia),
            "numeroActividades":numeroActividades,
        }

    return render(request, inicio, context)

def sitio(request):
    return render(request, "sitio.html")
