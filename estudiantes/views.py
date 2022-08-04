from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from cuentas.models import *
from horas.forms import EstudiantesForm
from actividades.models import Actividad
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/cuentas/login/')
def estudiantes_request(request):

    staffBotonVistaEstudiante= False

    if request.method == "POST":
        list_of_inputs=request.POST.getlist('inputs')
        if request.POST.get('studentButton'):
                studentButtonItemValue=request.POST.getlist('studentButton')
                estudianteAVer = Estudiante.objects.filter(id = studentButtonItemValue[0])
                staffBotonVistaEstudiante = True
                response = HttpResponseRedirect("/")
                response.headers["estudiante"] = estudianteAVer[0].id
                user = estudianteAVer[0].user
                return response
                #return render (request=request, template_name="../../inicio/templates/index.html", context={"estudianteID":estudianteAVer[0].id,})


    estudiantes_list = Estudiante.objects.all().filter(user__is_staff=False)
    if request.user.is_staff:
        actividades_list = Actividad.objects.all()
    #Actividad.objects.raw('SELECT id, horas FROM myapp_actividad ')
    horasEstudianteslist = []
    porcentajeEstudianteslist = []
    porcentajeWidthEstudianteslist = []

    horasTotalesPorEstudiante=0
    for estudiante in estudiantes_list:
       

        horasTotalesPorEstudiante=0
        for actividad in actividades_list:
            
            if actividad.estudiante.user.username == estudiante.user.username:
                if actividad.estado == "A":
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
    form.fields['carrera'].widget = forms.HiddenInput()
    form.fields['fechaInicioTCU'].widget = forms.HiddenInput()
    form.fields['fechaFinTCU'].widget = forms.HiddenInput()

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/estudiantes")

 
    return render(request, "editar_estudiante.html", context={"estudiante_form":form})


