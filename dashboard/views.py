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
def dashboard_request(request):

    estudiantes_list = Estudiante.objects.all()
    estudiante_actual = Estudiante.objects.get(user = request.user)

    #Desde aqui se procesa la barra de progreso de horas por estudiante
    my_actividades_list= Actividad.objects.raw('SELECT id, estudiante_id, horas, enPapelera FROM actividades_actividad where estudiante_id == '+ str(estudiante_actual.id)+" AND enPapelera==false")
    horasTotalesPorEstudiante=0    
   
    for actividad in my_actividades_list:
           
            if actividad.estado == "A":
                horasTotalesPorEstudiante+= actividad.horas

    #horasTotalesPorEstudiante=30  #para pruebas
    porcentaje= (100 / 300) * horasTotalesPorEstudiante
    porcentajeWidth = int(porcentaje)


    #Desde aqui se procesa la barra de progreso de dias del TCU por estudiante
    current_datetime = datetime.date.today()
    inicioTCU = estudiante_actual.fechaInicioTCU
    finalTCU = estudiante_actual.fechaFinTCU

    diasRestantesDelTCU =  finalTCU - current_datetime

    diasDesdeInicioTCU = current_datetime - inicioTCU
    diasTCU = diasDesdeInicioTCU.days

    totalDiasTCU = 365

    porcentajeDaysYear= (100 / totalDiasTCU) * diasTCU
    porcentajeWidthDaysYear = int(porcentajeDaysYear)



    #Datos para pie chart y horizontal bar chart con relación proyectos y actividades
    labels = []
    data = []
    dictCantidadActividades = {}
    querysetProyectos = Proyecto.objects.filter(enPapelera=False)
    
    
    for proyecto in querysetProyectos:
        if (proyecto.enPapelera==False):
            totalActividadesPorProyecto = 0
            querysetObjetivos=proyecto.objetivo_set.all()

            for objetivo in querysetObjetivos:
                if (objetivo.enPapelera==False):
                    querysetMetas=objetivo.meta_set.all()

                    for meta in querysetMetas:
                        if (meta.enPapelera==False):
                            querysetTareas=meta.tarea_set.all()

                            for tarea in querysetTareas:
                                if (tarea.enPapelera==False):
                                    totalActividadesPorProyecto = totalActividadesPorProyecto + tarea.actividad_set.filter(enPapelera=False).count()

        #labels.append(proyecto.nombre)
        #tquery=Tarea.objects.filter(proyecto=proyecto)
        #data.append(tquery.count)

            dictCantidadActividades[proyecto.nombre]=totalActividadesPorProyecto

    sorteddictCantidadActividades = sorted(dictCantidadActividades.items(), key=lambda x: x[1], reverse=True)
    
    for element in sorteddictCantidadActividades:
        labels.append(element[0])
        data.append(element[1])
    
    #Listas con los colores para los graficos desplegados
    colorList = color_list(dictCantidadActividades)

    #A partir de aquí datos para grafico de barras ranking de estudiantes por actividades
    labelsRankingEstudiante = []
    dataRankingEstudiante = []
    mapEstudianteCantidadActividades = {}
    rankingEstudiantesList = Estudiante.objects.filter(user__is_staff=False)

    for estudiante in rankingEstudiantesList:
        mapEstudianteCantidadActividades[estudiante.user.username] = Actividad.objects.filter(estudiante=estudiante,enPapelera=False).count()
    
    sortedmapEstudianteCantidadActividades=sorted(mapEstudianteCantidadActividades.items(), key=lambda x: x[1], reverse=True)

    for element in sortedmapEstudianteCantidadActividades:
        labelsRankingEstudiante.append(element[0])
        dataRankingEstudiante.append(element[1])
    

    colorListRankingEstudiante = color_list(mapEstudianteCantidadActividades)

    return render (request=request, template_name="../templates/dashboard.html", context={"progreso":horasTotalesPorEstudiante,
    "porcentaje":porcentaje,"width":porcentajeWidth,"diasTCU":diasTCU,"inicioTCU":inicioTCU,"finalTCU":finalTCU,"totalDiasTCU":totalDiasTCU,
    "porcentajeDaysYear":porcentajeDaysYear,"porcentajeWidthDaysYear":porcentajeWidthDaysYear,'labels': labels,'data': data,
    'colorList': colorList,'labelsRankingEstudiante': labelsRankingEstudiante,'dataRankingEstudiante': dataRankingEstudiante,
    'colorListRankingEstudiante': colorListRankingEstudiante,})




def color_list(listaCantidadMiembros):
    colorList = []
    
    alphaInitial= 1
    opasityDecreaseRange= 0.2
    r  = str(159)
    g  = str(90)
    b  = str(253)

    alpha = alphaInitial 
    count = 0
    for  i  in listaCantidadMiembros:
        alpha = alpha - (count)
        color = 'rgba(' + r + ','+ g + ','+ b + ','+ str(alpha) + ')'
        colorList.append(color)
        count = count + opasityDecreaseRange

    return colorList

    