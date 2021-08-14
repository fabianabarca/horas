from django.shortcuts import render

# Create your views here.
def solicitudes_request(request):
   return render (request=request, template_name="../templates/solicitudes.html")