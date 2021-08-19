from cuentas.models import Estudiante
from horas.forms import *
from django.contrib.auth.models import User
from actividades.models import Actividad
from django.shortcuts import render, redirect

# Create your views here.
def actividades_request(request):

    actividades_list = Actividad.objects.all()
    
    return render (request=request, template_name="../templates/actividades.html", context={"actividades":actividades_list})

def crear_actividad(request):

    if request.method == "POST":
        form = ActividadesForm(request.POST)
        if form.is_valid():
            form.save()
		
    form = ActividadesForm()
    
    return render (request=request, template_name="../templates/crear_actividad.html", context={"actividad_form":form})
 