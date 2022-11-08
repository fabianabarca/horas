from cuentas.models import Estudiante, Profesor, Carrera
from solicitudes.models import Solicitud, SolicitudArchivo
from actividades.models import Actividad
from areas.models import Area
from proyectos.models import *
from tareas.models import Tarea
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.forms import ClearableFileInput

# Create your forms here.


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    carreras = Carrera.objects.all()
    carrera = forms.ModelChoiceField(queryset=carreras)
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'style': 'width: 200px;', 'class': 'form-control'}))
    fecha_final = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'style': 'width: 200px;', 'class': 'form-control'}))

    class Meta:
        model = User

        #fields = ("username", "first_name", "last_name", "email", "carrera","password1", "password2")
        fields = UserCreationForm.Meta.fields + \
            ('first_name', 'last_name', 'email', 'carrera',
             'is_staff', 'fecha_inicio', 'fecha_final')

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].label = 'ID (carné)'

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.carrera = self.cleaned_data['carrera']
        user.fecha_inicio = self.cleaned_data['fecha_inicio']
        user.fecha_final = self.cleaned_data['fecha_final']

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
    descripcion = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all(
    ), required=False, widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.filter(
        enPapelera=False), required=False, widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    tarea = forms.ModelChoiceField(queryset=Tarea.objects.filter(
        enPapelera=False), required=False, widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'style': 'width: 200px;', 'class': 'form-control'}))
    fecha_final = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'style': 'width: 200px;', 'class': 'form-control'}))
    estado = forms.ChoiceField(required=False, choices=ESTADOS, widget=forms.Select(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))


class FiltrosTareaForm(forms.Form):

    nombre = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all(
    ), required=False, widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    tareaSuperior = forms.ModelChoiceField(queryset=Tarea.objects.filter(
        enPapelera=False), required=False, widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    objetivo = forms.ModelChoiceField(queryset=Objetivo.objects.filter(
        enPapelera=False), required=False, widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    descripcion = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    area = forms.ModelChoiceField(queryset=Area.objects.filter(enPapelera=False), required=False, widget=forms.Select(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))


class FiltrosProyectoForm(forms.Form):
    ESTADOS = (
        ('', '----'),
        ('P', 'En Revisión'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    )
    nombre = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    descripcion = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    profesor = forms.ModelChoiceField(queryset=Profesor.objects.all(
    ), required=False, widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    area = forms.ModelChoiceField(queryset=Area.objects.filter(enPapelera=False), required=False, widget=forms.Select(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    ubicacion = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))


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
    motivo = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all(
    ), required=False, widget=forms.Select(attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    tipo = forms.ChoiceField(required=False, choices=TIPOS, widget=forms.Select(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'style': 'width: 200px;', 'class': 'form-control'}))
    fecha_final = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'style': 'width: 200px;', 'class': 'form-control'}))
    estado = forms.ChoiceField(required=False, choices=ESTADOS, widget=forms.Select(
        attrs={'style': 'width: 200px;', 'class': 'form-control'}))


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Identificación',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class ActividadesForm(forms.ModelForm):
    '''Crea formulario para registro de actividades.'''

    #Se crean los campos para area, proyecto, objetivo
    area = forms.ModelChoiceField(queryset=Area.objects.all())
    proyecto = forms.ChoiceField()
    objetivo = forms.ChoiceField()

    field_order = ['area', 'proyecto', 'objetivo', 'tarea', 'descripcion', 'horas', 'fecha']

    # Carga todos los campos del modelo de actividades
    class Meta:
        model = Actividad
        fields = '__all__'
        widgets = {
            'fecha': DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'}
            ),
        }

    # Parte de implementación de restringir seleccion de tarea por proyecto
    def __init__(self, *args, **kwargs):
        
        super(ActividadesForm, self).__init__(*args, **kwargs)

        self.fields['estudiante'].initial = Estudiante.objects.get(
            user=User.objects.get(id=42))
        self.fields['estado'].initial = "P"

        #Inicializar, proyectos, objetivos y tareas en blanco.
        self.fields['proyecto'].queryset = Proyecto.objects.none()
        self.fields['objetivo'].queryset = Objetivo.objects.none()
        self.fields['tarea'].choices = []





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

    # archivo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})) # Adjuntar archivos

    def __init__(self, *args, **kwargs):
        super(SolicitudesForm, self).__init__(*args, **kwargs)
        self.fields['estudiante'].initial = Estudiante.objects.get(
            user=User.objects.get(id=42))
        self.fields['estado'].initial = "P"


class SolicitudesArchivoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArchivo
        fields = ['archivo']
        widgets = {
            'archivo': ClearableFileInput(attrs={'multiple': True}),
        }


class AreasForm(forms.ModelForm):
    class Meta:
        model = Area
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['objetivo'].queryset = Objetivo.objects.none()

        # for value in self.data.keys():
        # print(value)
        if 'tareasuperior' in self.data:
            try:
                tareasuperior_id = int(self.data.get('tareasuperior'))
                #print("forms: " + Objetivo.objects.filter(tarea__id=tareasuperior_id).order_by('name'))
                self.fields['objetivo'].queryset = Objetivo.objects.filter(
                    tarea__id=tareasuperior_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            #self.fields['objetivo'].queryset = Objetivo.objects.filter(tarea=self.instance)
            self.fields['objetivo'].queryset = Objetivo.objects.filter(
                enPapelera=False)


class EstudiantesForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = "__all__"
