from django import forms
from horas.forms import SolicitudesForm
from django.shortcuts import render
from .models import *

# Create your views here.
def solicitudes_request(request):
    estudiante_actual = Estudiante.objects.get(user = request.user)
    solicitudes_list = Solicitud.objects.filter(estudiante = estudiante_actual)
    return render (request=request, template_name="../templates/solicitudes.html",context={"solicitudes":solicitudes_list})


def crear_solicitud(request):

    estudiante_actual = Estudiante.objects.get(user = request.user)

    if request.method == "POST":
        form = SolicitudesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.estudiante = estudiante_actual
            post.save()
		
		
    form = SolicitudesForm()
    form.fields['estado'].widget = forms.HiddenInput()
    form.fields['estudiante'].widget = forms.HiddenInput()
    
    return render (request=request, template_name="../templates/crear_solicitud.html", context={"solicitud_form":form})
 

