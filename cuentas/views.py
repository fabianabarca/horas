from django.shortcuts import render, redirect
from horas.forms import *
from django.contrib import messages
from actividades.views import *
from inicio.views import *
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from cuentas.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail


@staff_member_required(login_url='/cuentas/ingreso/')
def register_request(request):
    form = NewUserForm(request.POST or None)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            carrera = form.cleaned_data.get('carrera')

            if (not Carrera.objects.filter(nombre__contains=carrera).exists()):

                c = Carrera(nombre=carrera)
                c.save()

            # Actualmente en la base de datos crear usuario significa crearlo como estudiante
            # aqui diferencia entre asignar valores al estudiante creado o asignar estudiante como profesor tambien
            estudiante = Estudiante.objects.get(id=user.id)
            estudiante.carrera_id = Carrera.objects.get(
                nombre__contains=carrera)
            # estudiante.save()
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            fecha_final = form.cleaned_data.get('fecha_final')
            estudiante.fecha_inicio = fecha_inicio
            estudiante.fecha_final = fecha_final

            estudiante.save()

            is_staff = form.cleaned_data.get('is_staff')

            if (is_staff):
                user.is_staff = is_staff
                user.is_superuser = is_staff
                user.save()

                profesor = Profesor(user_id=user.id)
                profesor.save()

            #login(request, user)
            messages.success(request, "Registro de " +
                             user.username+" exitoso.")
            return redirect(register_request)
        else:
            messages.error(request, "Falló el registro. Información inválida.")
    #form = NewUserForm()

    context = {
        "register_form": form,
    }

    return render(request, "registro.html", context)


def login_request(request):

    form = CustomAuthenticationForm(request.POST or None)
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        
        if request.POST.get("recuperar"):
            carnet = request.POST["carnet"]
            messages.error(request, "Si el carnet fue registrado anteriormente, usted recibirá un mensaje al correo electrónico asociado.")
            #setear setting.py
            try:
                estudiante = Estudiante.objects.get(user__username = carnet)
                send_mail(
                    'Cambio de contraseña en Sistema de Horas',
                    'Here is the message.',
                    [estudiante.email],
                    fail_silently=False,
)
            except:
                print('Estudiante no existe')
            
        else:
           
            print(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    #messages.info(request, "You are now logged in as {username}.")

                    return redirect(index)
                else:

                    messages.error(request, "Usuario o contraseña inválido.")
            else:
                messages.error(request, "Usuario o contraseña inválido.")
    form = CustomAuthenticationForm()
    return render(request, "ingreso.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "La sesión ha terminado exitosamente.")
    return redirect(login_request)


@login_required(login_url='/cuentas/ingreso/')
def perfil(request):

    # Datos de estudiante actual
    estudiante_actual = Estudiante.objects.get(user=request.user)

    # Cambio de contraseña
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'La contraseña ha sido cambiada exitosamente',
                             extra_tags='alert-success')
        return redirect('perfil')

    else:
        form = PasswordChangeForm(request.user)

    context = {
        'estudiante': estudiante_actual,
        'form': form,
    }
    return render(request, 'perfil.html', context)
