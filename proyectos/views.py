from horas.forms import ProyectosForm
from proyectos.models import Proyecto
from django.shortcuts import render

# Create your views here.
def proyectos_request(request):
    proyectos_list = Proyecto.objects.all()
    return render (request=request, template_name="../templates/proyectos.html", context={"proyectos":proyectos_list})


def crear_proyecto(request):

    if request.method == "POST":
        form = ProyectosForm(request.POST)
        if form.is_valid():
            form.save()
		
    form = ProyectosForm()
    
    return render (request=request, template_name="../templates/crear_proyecto.html", context={"proyecto_form":form})
 