from django.http.response import HttpResponseRedirect
from cuentas.models import Estudiante
from horas.forms import *
from django.contrib.auth.models import User
from actividades.models import Actividad
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/cuentas/login/')
def actividades_request(request):


    list_of_inputs=request.POST.getlist('inputs')

    is_staff = request.user.is_staff

    # Put the logging info within your django view

    if request.user.is_staff:
        actividades_list = Actividad.objects.all()

    else: 
        estudiante_actual = Estudiante.objects.get(user = request.user)
        actividades_list = Actividad.objects.filter(estudiante = estudiante_actual)


    if request.method == "POST":
        form = FiltrosForm(request.POST or None)
        list_of_inputs=request.POST.getlist('inputs')

        if request.POST.get('aprobar'):
            for input in list_of_inputs:
               Actividad.objects.filter(id = input.replace('/','')).update(estado='A')
      
        if request.POST.get('rechazar'):
            for input in list_of_inputs:
               Actividad.objects.filter(id = input.replace('/','')).update(estado='R')
                                                
        if form.is_valid():
            if form.cleaned_data.get('estudiante'):
                actividades_list =  actividades_list.filter(estudiante = form.cleaned_data.get('estudiante'))
            if form.cleaned_data.get('proyecto'):
                actividades_list =  actividades_list.filter(proyecto = form.cleaned_data.get('proyecto'))
            if form.cleaned_data.get('estado'):
                actividades_list =  actividades_list.filter(estado = form.cleaned_data.get('estado'))
            if form.cleaned_data.get('descripcion'):
                actividades_list =  actividades_list.filter(descripcion__contains= form.cleaned_data.get('descripcion'))
            if form.cleaned_data.get('fecha_inicio') or form.cleaned_data.get('fecha_final'):
                actividades_list =  actividades_list.filter(fecha__range=[form.cleaned_data.get('fecha_inicio'), form.cleaned_data.get('fecha_final')])
        
    form = FiltrosForm()

    return render (request=request, template_name="../templates/actividades.html", context={"actividades":actividades_list, "filtros_form":form})


@login_required(login_url='/cuentas/login/')
def crear_actividad(request):

    estudiante_actual = Estudiante.objects.get(user = request.user)

    if request.method == "POST":
        form = ActividadesForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.estudiante = estudiante_actual
            post.save()
            return HttpResponseRedirect("/")
		
    form = ActividadesForm()
    form.fields['estado'].widget = forms.HiddenInput()
    form.fields['estudiante'].widget = forms.HiddenInput()
    
    return render (request=request, template_name="../templates/crear_actividad.html", context={"actividad_form":form})
 