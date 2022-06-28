from django.shortcuts import  render, redirect
from horas.forms import *
from django.contrib import messages
from actividades.views import *
from django.contrib.auth import login, authenticate, logout #add this
from cuentas.models import *
from django.core.exceptions import ValidationError

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			carrera = form.cleaned_data.get('carrera')

			
			if(not Carrera.objects.filter(nombre__contains=carrera).exists()):
				
				c = Carrera(nombre=carrera)
				c.save()
			
			estudiante = Estudiante.objects.get(id=user.id)
			estudiante.carrera_id = Carrera.objects.get(nombre__contains=carrera)
			estudiante.save()
			
			

			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect(actividades_request)
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="../templates/register.html", context={"register_form":form})


def login_request(request):


	if request.method == "POST":
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				#messages.info(request, "You are now logged in as {username}.")
				
				return redirect(actividades_request)
			else:
				
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = CustomAuthenticationForm()
	return render(request=request, template_name="../templates/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect(login_request)