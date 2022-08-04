from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase


from inicio.views import *
from actividades.views import *
from tareas.views import *
from objetivos.views import *
from proyectos.views import *
from areas.views import *
from solicitudes.views import *
from cuentas.views import *
from dashboard.views import *
from estudiantes.views import *
from papelera.views import *
#Prueba para ver que vistas de pagina funcionen basado en documentación de django en 
#https://docs.djangoproject.com/en/4.0/topics/testing/advanced/#the-request-factory

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='a232323', email='tt2936082@gmail.com', password='admin2323')
        estudiante = Estudiante.objects.get(user=self.user)
        
        estudiante.fechaInicioTCU ='2022-08-10'
        estudiante.fechaFinTCU='2023-08-17'
        estudiante.save()

    def test_All_Views_UsuarioEstudianteRegular(self):
        #Probando pagina inicio__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/inicio/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        
        self.assertEqual(response.status_code, 200)

        #Probando pagina actividades__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/actividades/')
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user
        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        #request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = actividades_request(request)

        self.assertEqual(response.status_code, 200)


        #Probando pagina tareas__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/tareas/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = tareas_request(request)
        
        self.assertEqual(response.status_code, 200)

        #Probando pagina objetivos__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/objetivos/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = objetivos_request(request)
        
        self.assertEqual(response.status_code, 200)

        #Probando pagina proyectos__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/proyectos/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = proyectos_request(request)
        
        self.assertEqual(response.status_code, 200)

        #Probando pagina areas__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/areas/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = areas_request(request)
        
        self.assertEqual(response.status_code, 200)

        #Probando pagina solicitudes__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/solicitudes/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = solicitudes_request(request)
        
        self.assertEqual(response.status_code, 200)

        #Probando pagina dashboard__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/dashboard/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = dashboard_request(request)
        
        self.assertEqual(response.status_code, 200)


        #Probando pagina papelera__________________________________________________

        # Create an instance of a GET request.
        request = self.factory.get('/papelera/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = papelera_request(request)
        
        self.assertEqual(response.status_code, 200)

