from django.shortcuts import  render, redirect
from horas.forms import *
from django.contrib import messages
from actividades.views import *
from inicio.views import *
from django.contrib.auth import login, authenticate, logout #add this
from cuentas.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='/cuentas/ingreso/')
def register_request(request):
	form = NewUserForm(request.POST or None)
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			carrera = form.cleaned_data.get('carrera')
			
			if(not Carrera.objects.filter(nombre__contains=carrera).exists()):
				
				c = Carrera(nombre=carrera)
				c.save()

			
			#Actualmente en la base de datos crear usuario significa crearlo como estudiante
			#aqui diferencia entre asignar valores al estudiante creado o asignar estudiante como profesor tambien
			estudiante = Estudiante.objects.get(id=user.id)
			estudiante.carrera_id = Carrera.objects.get(nombre__contains=carrera)
			#estudiante.save()
			fecha_inicio = form.cleaned_data.get('fecha_inicio')
			fecha_final	= form.cleaned_data.get('fecha_final')
			estudiante.fecha_inicio=fecha_inicio
			estudiante.fecha_final=fecha_final
			
			estudiante.save()


			is_staff = form.cleaned_data.get('is_staff')
			
			if ( is_staff):
				user.is_staff=is_staff
				user.is_superuser=is_staff
				user.save()

				profesor = Profesor(user_id=user.id)
				profesor.save()

			#login(request, user)
			messages.success(request, "Registro de " +user.username+" exitoso." )
			return redirect(register_request)
		else:
			messages.error(request, "Falló el registro. Información inválida.")
	#form = NewUserForm()

	context = {
		"register_form":form,
	}

	return render (request, "registro.html", context)


def login_request(request):

	form = CustomAuthenticationForm(request.POST or None)
	if request.method == "POST":
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				#messages.info(request, "You are now logged in as {username}.")
				
				return redirect(index)
			else:
				
				messages.error(request,"Usuario o contraseña inválido.")
		else:
			messages.error(request,"Usuario o contraseña inválido.")
	form = CustomAuthenticationForm()
	return render(request, "ingreso.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "La sesión ha terminado exitosamente.") 
	return redirect(login_request)


@login_required(login_url='/cuentas/ingreso/')
def perfil(request):

    estudiante_actual = Estudiante.objects.get(user=request.user)

    context = {
		'estudiante': estudiante_actual
	}
    return render(request, 'perfil.html', context)