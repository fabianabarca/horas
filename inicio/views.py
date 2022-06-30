from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/cuentas/login/')
def index(request):
    return render(request, 'index.html')