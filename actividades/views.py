from django.shortcuts import render, redirect

# Create your views here.
def actividades_request(request):
    return render (request=request, template_name="../templates/actividades.html")