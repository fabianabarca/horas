from cuentas.models import Estudiante
from horas.forms import *
from django.contrib.auth.models import User
from actividades.models import Actividad
from django.shortcuts import render, redirect

# Create your views here.
def actividades_request(request):

    estudiante_actual = Estudiante.objects.get(user = request.user)
    actividades_list = Actividad.objects.filter(estudiante = estudiante_actual)
    
    return render (request=request, template_name="../templates/actividades.html", context={"actividades":actividades_list})



def crear_actividad(request):

    estudiante_actual = Estudiante.objects.get(user = request.user)

    if request.method == "POST":
        form = ActividadesForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.estudiante = estudiante_actual
            post.save()
		
    form = ActividadesForm()
    form.fields['estado'].widget = forms.HiddenInput()
    form.fields['estudiante'].widget = forms.HiddenInput()
    
    return render (request=request, template_name="../templates/crear_actividad.html", context={"actividad_form":form})
 