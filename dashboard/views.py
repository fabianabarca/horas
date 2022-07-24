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



    #pie chart
    labels = []
    data = []

    listaCantidadActividades = {}
    querysetTareas = Tarea.objects.all()
    for tarea in querysetTareas:
       
        listaCantidadActividades[tarea.nombre]=tarea.actividad_set.all().count()
        #labels.append(proyecto.nombre)
        #tquery=Tarea.objects.filter(proyecto=proyecto)
        #data.append(tquery.count)
   
    sorted(listaCantidadActividades.items(), key=lambda x: x[1], reverse=True)

    for element in listaCantidadActividades.values():
        data.append(element)
        
    print(len(data))
    for element2 in listaCantidadActividades.keys():
        labels.append(element2)
        
    print(len(labels))
    print(listaCantidadActividades)
    return render (request=request, template_name="../templates/dashboard.html", context={"progreso":horasTotalesPorEstudiante,
    "porcentaje":porcentaje,"width":porcentajeWidth,"diasTCU":diasTCU,"inicioTCU":inicioTCU,"finalTCU":finalTCU,"totalDiasTCU":totalDiasTCU,
    "porcentajeDaysYear":porcentajeDaysYear,"porcentajeWidthDaysYear":porcentajeWidthDaysYear,'labels': labels,'data': data,})



    