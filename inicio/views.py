from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.http.response import HttpResponseRedirect
from dashboard.models import *
import time
from cuentas.models import *
from actividades.models import Actividad
from cuentas.models import Estudiante
from proyectos.models import Proyecto
import datetime

# Create your views here.

@login_required(login_url='/cuentas/login/')
def index(request,id=9999):
    
    #en caso de que NO se redirige de página Estudiantes, uso el numero 9999 como default al llegar a
    #página Inicio desde login o desde menu de navegación
    if id == 9999:  
                
        id =request.user.id


    estudiantes_list = Estudiante.objects.all()
    estudiante_actual = Estudiante.objects.get(user =  User.objects.filter(id=id)[0])

    numeroEstudiantes=estudiantes_list.filter(user__is_staff=False).count

    proyectos_list = Proyecto.objects.all()
    numeroProyectos=proyectos_list.count
    

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
    "porcentajeDaysYear":porcentajeDaysYear,"porcentajeWidthDaysYear":porcentajeWidthDaysYear,"factorDeAvance":factorDeAvance,
    "numeroEstudiantes":numeroEstudiantes,"numeroProyectos":numeroProyectos,"estudiante_actual":estudiante_actual,})

'''
@login_required(login_url='/cuentas/login/')
def indexInicio(request):

    index(request,request.user.id)
    print("llegó aqui")
    return render (request=request, template_name="../templates/index.html", context={})
'''