from django.shortcuts import render

# Create your views here.
def proyectos_request(request):
   return render (request=request, template_name="../templates/proyectos.html")