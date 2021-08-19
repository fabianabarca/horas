from horas.forms import SolicitudesForm
from django.shortcuts import render
from .models import *

# Create your views here.
def solicitudes_request(request):
    solicitudes_list = Solicitud.objects.all()
    return render (request=request, template_name="../templates/solicitudes.html",context={"solicitudes":solicitudes_list})


def crear_solicitud(request):

    if request.method == "POST":
        form = SolicitudesForm(request.POST)
        if form.is_valid():
            form.save()
		
    form = SolicitudesForm()
    
    return render (request=request, template_name="../templates/crear_solicitud.html", context={"solicitud_form":form})
 