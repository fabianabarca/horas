from django.shortcuts import render
from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from dashboard.models import *
from django.contrib.auth.decorators import login_required
import time
from cuentas.models import *
from actividades.models import Actividad

# Create your views here.
@login_required(login_url='/cuentas/login/')
def dashboard_request(request):
    #dashboard_list = Tarea.objects.all()
    #if request.method == "POST":
       # if request.POST.get('deleteButton'):
              #  deleteButtonItemValue=request.POST.getlist('deleteButton')
               # obj = Tarea( id = deleteButtonItemValue[0]) 
                #Tarea.objects.filter(id = deleteButtonItemValue[0]).update(enPapelera='True')

    estudiantes_list = Estudiante.objects.all()
    estudiante_actual = Estudiante.objects.get(user = request.user)

    #if request.user.is_staff:
    actividades_list = Actividad.objects.all()

    my_actividades_list= Actividad.objects.raw('SELECT id, estudiante_id, horas, enPapelera FROM actividades_actividad where estudiante_id == '+ str(estudiante_actual.id)+" AND enPapelera==false")
    horasTotalesPorEstudiante=0      
    print(str(estudiante_actual.id))
    for actividad in my_actividades_list:
            horasTotalesPorEstudiante+= actividad.horas

    #horasTotalesPorEstudiante=30  #para pruebas
    porcentaje= (100 / 300) * horasTotalesPorEstudiante
    porcentajeWidth = int(porcentaje)
    print(horasTotalesPorEstudiante)
    print(porcentaje)

    return render (request=request, template_name="../templates/dashboard.html", context={"progreso":horasTotalesPorEstudiante,"porcentaje":porcentaje,"width":porcentajeWidth,})