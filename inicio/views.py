from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.http.response import HttpResponseRedirect
from dashboard.models import *
import time
from cuentas.models import *
from actividades.models import Actividad
import datetime

# Create your views here.

@login_required(login_url='/cuentas/login/')
def index(request):
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


    factorDeAvance =  porcentaje / porcentajeDaysYear
    redondeadoFactorDeAvance = int(factorDeAvance)


    return render (request=request, template_name="../templates/index.html", context={"progreso":horasTotalesPorEstudiante,
    "porcentaje":porcentaje,"width":porcentajeWidth,"diasTCU":diasTCU,"inicioTCU":inicioTCU,"finalTCU":finalTCU,"totalDiasTCU":totalDiasTCU,
    "porcentajeDaysYear":porcentajeDaysYear,"porcentajeWidthDaysYear":porcentajeWidthDaysYear,"factorDeAvance":factorDeAvance,})