from django.shortcuts import render
from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from dashboard.models import *
from django.contrib.auth.decorators import login_required
import time

# Create your views here.
@login_required(login_url='/cuentas/login/')
def dashboard_request(request):
    #dashboard_list = Tarea.objects.all()
    #if request.method == "POST":
       # if request.POST.get('deleteButton'):
              #  deleteButtonItemValue=request.POST.getlist('deleteButton')
               # obj = Tarea( id = deleteButtonItemValue[0]) 
                #Tarea.objects.filter(id = deleteButtonItemValue[0]).update(enPapelera='True')

    return render (request=request, template_name="../templates/dashboard.html", context={})