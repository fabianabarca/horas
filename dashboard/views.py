from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from dashboard.models import *
from horas.forms import TareasForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from dashboard.models import Order
from django.core import serializers

# Create your views here.
@login_required(login_url='/cuentas/login/')
def dashboard_with_pivot(request):
    

    return render (request=request, template_name="../templates/dashboard_with_pivot.html", context={})



def pivot_data(request):
    dataset = Order.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)