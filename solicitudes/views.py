from django import forms
from django.http.response import HttpResponseRedirect
from horas.forms import FiltrosGestionForm, SolicitudesForm
from django.shortcuts import render
from .models import *

# Create your views here.
def solicitudes_request(request):

    list_of_inputs=request.POST.getlist('inputs')
    if request.user.is_staff:
        solicitudes_list = Solicitud.objects.all()

    else: 
        estudiante_actual = Estudiante.objects.get(user = request.user)
        solicitudes_list = Solicitud.objects.filter(estudiante = estudiante_actual)


    if request.method == "POST":
        form = FiltrosGestionForm(request.POST or None)
        list_of_inputs=request.POST.getlist('inputs')

        if request.POST.get('aprobar'):
            for input in list_of_inputs:
               Solicitud.objects.filter(id = input.replace('/','')).update(estado='A')
      
        if request.POST.get('rechazar'):
            for input in list_of_inputs:
               Solicitud.objects.filter(id = input.replace('/','')).update(estado='R')
                                                
        if form.is_valid():
            if form.cleaned_data.get('estudiante'):
                solicitudes_list =  solicitudes_list.filter(estudiante = form.cleaned_data.get('estudiante'))
            if form.cleaned_data.get('tipo'):
                solicitudes_list =  solicitudes_list.filter(tipo = form.cleaned_data.get('tipo'))
            if form.cleaned_data.get('estado'):
                solicitudes_list =  solicitudes_list.filter(estado = form.cleaned_data.get('estado'))
            if form.cleaned_data.get('motivo'):
                solicitudes_list =  solicitudes_list.filter(motivo__contains= form.cleaned_data.get('motivo'))
            if form.cleaned_data.get('fecha_inicio') or form.cleaned_data.get('fecha_final'):
                solicitudes_list =  solicitudes_list.filter(fecha__range=[form.cleaned_data.get('fecha_inicio'), form.cleaned_data.get('fecha_final')])

    
    form = FiltrosGestionForm()  

    return render (request=request, template_name="../templates/solicitudes.html",context={"solicitudes":solicitudes_list, "filtros_form":form})


def crear_solicitud(request):

    estudiante_actual = Estudiante.objects.get(user = request.user)

    if request.method == "POST":
        form = SolicitudesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.estudiante = estudiante_actual
            post.save()
            return HttpResponseRedirect("/solicitudes")
		
		
    form = SolicitudesForm()
    form.fields['estudiante'].widget = forms.HiddenInput()
    
    return render (request=request, template_name="../templates/crear_solicitud.html", context={"solicitud_form":form})
 

