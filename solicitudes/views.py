from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from horas.forms import FiltrosGestionForm, SolicitudesArchivoForm, SolicitudesForm
from django.shortcuts import render
from .models import *
from .models import SolicitudArchivo
from django.contrib.auth.decorators import login_required
import time

'''
# Adjuntar archivo
from django.views.generic.edit import FormView

class FileFieldFormView(FormView):
    form_class = SolicitudesForm
    template_name = 'crear_solicitud.html'  # Replace with your template.
    success_url = '/solicitudes'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('archivo')
        if form.is_valid():
            for f in files:
                #...  # Do something with each file.
                #form.save()
                #obj = self.model.objects.create(file=f)
                f.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
'''
# Create your views here.


@login_required(login_url='/cuentas/ingreso/')
def solicitudes(request):

    list_of_inputs = request.POST.getlist('inputs')

    # Obtener solicitudes según sea docente (todas)
    # o estudiante (las propias)
    if request.user.is_staff:
        solicitudes_list = Solicitud.objects.all().exclude(enPapelera=True)
    else:
        estudiante_actual = Estudiante.objects.get(user=request.user)
        solicitudes_list = Solicitud.objects.filter(
            estudiante=estudiante_actual).exclude(enPapelera=True)

    # Clasificación de solicitudes por tipo
    solicitudes_F = solicitudes_list.filter(tipo='F')
    solicitudes_P = solicitudes_list.filter(tipo='P')
    solicitudes_A = solicitudes_list.filter(tipo='A')
    solicitudes_O = solicitudes_list.filter(tipo='O')

    # Formulario de filtros
    if request.method == "POST" and request.user.is_staff:
        form = FiltrosGestionForm(request.POST or None)
        list_of_inputs = request.POST.getlist('inputs')

        if request.POST.get('aprobar'):
            for input in list_of_inputs:
                Solicitud.objects.filter(
                    id=input.replace('/', '')).update(estado='A')

        if request.POST.get('rechazar'):
            for input in list_of_inputs:
                Solicitud.objects.filter(
                    id=input.replace('/', '')).update(estado='R')

        if request.POST.get('deleteButton'):
            deleteButtonItemValue = request.POST.getlist('deleteButton')
            obj = Solicitud(id=deleteButtonItemValue[0])
            Solicitud.objects.filter(
                id=deleteButtonItemValue[0]).update(enPapelera='True')

        if form.is_valid():
            if form.cleaned_data.get('estudiante'):
                solicitudes_list = solicitudes_list.filter(
                    estudiante=form.cleaned_data.get('estudiante'))
            if form.cleaned_data.get('tipo'):
                solicitudes_list = solicitudes_list.filter(
                    tipo=form.cleaned_data.get('tipo'))
            if form.cleaned_data.get('estado'):
                solicitudes_list = solicitudes_list.filter(
                    estado=form.cleaned_data.get('estado'))
            if form.cleaned_data.get('motivo'):
                solicitudes_list = solicitudes_list.filter(
                    motivo__contains=form.cleaned_data.get('motivo'))
            if form.cleaned_data.get('fecha_inicio') or form.cleaned_data.get('fecha_final'):
                solicitudes_list = solicitudes_list.filter(fecha__range=[form.cleaned_data.get(
                    'fecha_inicio'), form.cleaned_data.get('fecha_final')])

        # return HttpResponseRedirect("/solicitudes")

    archivos_list = SolicitudArchivo.objects.all()

    form = FiltrosGestionForm()

    context = { 
        "solicitudes_F": solicitudes_F,
        "solicitudes_P": solicitudes_P,
        "solicitudes_A": solicitudes_A,
        "solicitudes_O": solicitudes_O,
        "archivos": archivos_list, 
        "filtros_form": form,
    }

    return render(request, "solicitudes.html", context)


@login_required(login_url='/cuentas/ingreso/')
def crear_solicitud(request):

    estudiante_actual = Estudiante.objects.get(user=request.user)

    if request.method == "POST":
        form = SolicitudesForm(request.POST)
        form_archivo = SolicitudesArchivoForm(
            request.POST, request.FILES)  # Adjuntar archivo
        archivos = request.FILES.getlist('archivo')  # field name in model
        if form.is_valid() and form_archivo.is_valid():
            post = form.save(commit=False)
            post.estudiante = estudiante_actual
            # form.save() # Adjuntar archivo
            post.save()
            for f in archivos:
                instancia_archivo = SolicitudArchivo(archivo=f, solicitud=post)
                instancia_archivo.save()
            time.sleep(1)  # para que mensaje de que se creo pueda verse
            return HttpResponseRedirect("/solicitudes")
        else:
            print(form._errors)  # Adjuntar archivo, el cual no debe estar vacio
    else:
        form = SolicitudesForm()
        form_archivo = SolicitudesArchivoForm()

    form.fields['estudiante'].widget = forms.HiddenInput()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()
    if not request.user.is_staff:  # Si el usuario no es admin se quita el campo de Estado
        form.fields['estado'].widget = forms.HiddenInput()

    # Acción: editar
    crear = True

    # Contexto
    context = {
        "crear": crear,
        "solicitud_form": form,
        "solicitudArchivo_form": form_archivo
    }

    return render(request, "crear_solicitud.html", context)


@login_required(login_url='/cuentas/ingreso/')
def editar_solicitud(request, id):

    solicitud = get_object_or_404(Solicitud, id=id)

    form = SolicitudesForm(request.POST or None, instance=solicitud)
    form_archivo = SolicitudesArchivoForm(
        request.POST or None, request.FILES)  # Adjuntar archivo
    archivos = request.FILES.getlist('archivo')  # field name in model

    form.fields['estado'].widget = forms.HiddenInput()
    form.fields['enPapelera'].widget = forms.HiddenInput()
    form.fields['fechaPapelera'].widget = forms.HiddenInput()

    if form.is_valid() and form_archivo.is_valid():
        post = form.save(commit=False)
        for f in archivos:
            instancia_archivo = SolicitudArchivo(archivo=f, solicitud=post)
            instancia_archivo.save()
        form.save()
        return HttpResponseRedirect("/solicitudes")

    # Acción: editar
    crear = False

    # Contexto
    context = {
        "crear": crear,
        "solicitud_form": form,
        "solicitudArchivo_form": form_archivo,
        "solicitud": solicitud,
    }

    return render(request, "crear_solicitud.html", context)
