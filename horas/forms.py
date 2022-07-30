from cuentas.models import Estudiante, Profesor
from solicitudes.models import Solicitud, SolicitudArchivo
from actividades.models import Actividad
from proyectos.models import *
from tareas.models import Tarea
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.forms import ClearableFileInput

# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    carrera = forms.CharField(required=False)
    fechaInicioTCU = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date','style': 'width: 200px;', 'class': 'form-control'}))
    fechaFinTCU = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date','style': 'width: 200px;', 'class': 'form-control'}))

    class Meta:
        model = User
         
        #fields = ("username", "first_name", "last_name", "email", "carrera","password1", "password2")
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email','carrera','is_staff','fechaInicioTCU','fechaFinTCU')

        
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].label = 'Carne'

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.carrera = self.cleaned_data['carrera']
        user.fechaInicioTCU = self.cleaned_data['fechaInicioTCU']
        user.fechaFinTCU = self.cleaned_data['fechaFinTCU']
        
        if commit:
            user.save()
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class FiltrosForm(forms.Form):
    ESTADOS = (
        ('', '----'),
        ('P', 'En Revisión'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    )
    descripcion = forms.CharField(required=False,widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    tarea = forms.ModelChoiceField(queryset=Tarea.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    fecha_inicio= forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date','style': 'width: 200px;', 'class': 'form-control'}))
    fecha_final= forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date','style': 'width: 200px;', 'class': 'form-control'}))
    estado = forms.ChoiceField(required=False, choices= ESTADOS,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))

class FiltrosTareaForm(forms.Form):
    
    nombre = forms.CharField(required=False,widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    tareaSuperior = forms.ModelChoiceField(queryset=Tarea.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    objetivo = forms.ModelChoiceField(queryset=Objetivo.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    descripcion = forms.CharField(required=False,widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))



class FiltrosProyectoForm(forms.Form):
    ESTADOS = (
        ('', '----'),
        ('P', 'En Revisión'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    )
    nombre = forms.CharField(required=False,widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    descripcion = forms.CharField(required=False,widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    profesor = forms.ModelChoiceField(queryset=Profesor.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    ubicacion = forms.CharField(required=False,widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}))

class FiltrosGestionForm(forms.Form):
    ESTADOS = (
        ('', '----'),
        ('P', 'En Revisión'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    )
    TIPOS = (
        ('', '----'),
        ('F', 'Finalización'),
        ('M', 'Prórroga'),
        ('C', 'Corrección'),
    )
    motivo = forms.CharField(required=False,widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all(), required=False,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    tipo = forms.ChoiceField(required=False, choices= TIPOS ,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    fecha_inicio= forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date','style': 'width: 200px;', 'class': 'form-control'}))
    fecha_final= forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date','style': 'width: 200px;', 'class': 'form-control'}))
    estado = forms.ChoiceField(required=False, choices= ESTADOS,widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    
class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='ID/Carne',
        widget=forms.TextInput(attrs={'autofocus': True})
    )



class ActividadesForm(forms.ModelForm):

    class Meta:
        model = Actividad
        fields = "__all__"
        widgets = {
            'fecha': DateInput(
                                 format=('%Y-%m-%d'),
                                 attrs={'class': 'form-control', 
                                        'placeholder': 'Select a date',
                                        'type': 'date'}
                               ),

        }

        
    def __init__(self, *args, **kwargs):
        super(ActividadesForm, self).__init__(*args, **kwargs)
        self.fields['estudiante'].initial = Estudiante.objects.get(user = User.objects.get(id = 1))
        self.fields['estado'].initial = "P"






class SolicitudesForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = "__all__"
        widgets = {
            'fecha': DateInput(
        format=('%Y-%m-%d'),
        attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
           
        }
    
    #archivo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})) # Adjuntar archivos

    def __init__(self, *args, **kwargs):
        super(SolicitudesForm, self).__init__(*args, **kwargs)
        self.fields['estudiante'].initial = Estudiante.objects.get(user = User.objects.get(id = 1))
        self.fields['estado'].initial = "P"

class SolicitudesArchivoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArchivo
        fields = ['archivo']
        widgets = {
            'archivo': ClearableFileInput(attrs={'multiple': True}),
        }

class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"

class ProyectosForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = "__all__"
        
class ObjetivosForm(forms.ModelForm):
    class Meta:
        model = Objetivo
        fields = "__all__"


class TareasForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = "__all__"


       
class EstudiantesForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = "__all__"
