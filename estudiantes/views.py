from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from cuentas.models import *
from horas.forms import EstudiantesForm
from actividades.models import Actividad


from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/cuentas/login/')
def estudiantes_request(request):
    estudiantes_list = Estudiante.objects.all()
    if request.user.is_staff:
        actividades_list = Actividad.objects.all()
    Actividad.objects.raw('SELECT id, horas FROM myapp_actividad ')
    horasEstudianteslist = []
    porcentajeEstudianteslist = []
    porcentajeWidthEstudianteslist = []

    horasTotalesPorEstudiante=0
    for estudiante in estudiantes_list:
       

        horasTotalesPorEstudiante=0
        for actividad in actividades_list:
            
            if actividad.estudiante.user.username == estudiante.user.username:
                horasTotalesPorEstudiante+= actividad.horas

        horasEstudianteslist.append(horasTotalesPorEstudiante)
        porcentaje= (100 / 300) * horasTotalesPorEstudiante
        porcentajeEstudianteslist.append(porcentaje)
        porcentajeWidthEstudianteslist.append(int(porcentaje))

    zipHoras= zip(estudiantes_list,horasEstudianteslist,porcentajeEstudianteslist,porcentajeWidthEstudianteslist)    
    
    return render (request=request, template_name="../templates/estudiantes.html", context={"zipHoras":zipHoras,"horaslist":horasEstudianteslist,
    "estudiantes":estudiantes_list,"actividades":actividades_list,
    "porcentajeList":porcentajeEstudianteslist,"porcentajeWidthList":porcentajeWidthEstudianteslist})

@login_required(login_url='/cuentas/login/')
def editar_estudiante(request, id):

    obj = get_object_or_404(Estudiante, id = id) 

    form = EstudiantesForm(request.POST or None, instance = obj)
    form.fields['user'].widget = forms.HiddenInput()
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/estudiantes")

 
    return render(request, "editar_estudiante.html", context={"estudiante_form":form})