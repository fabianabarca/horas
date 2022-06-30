from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from tareas.models import *
from horas.forms import TareasForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/cuentas/login/')
def dashboard_with_pivot(request):
    

    return render (request=request, template_name="../templates/dashboard_with_pivot.html", context={})



def pivot_data(request):
    dataset = Order.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)