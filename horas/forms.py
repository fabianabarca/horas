from cuentas.models import Estudiante
from solicitudes.models import Solicitud
from actividades.models import Actividad
from proyectos.models import Proyecto
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name","email", "password1", "password2")


        
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].label = 'Carne'

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
    
        
        if commit:
            user.save()
        return user



class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='ID/Carne',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class DateInput(forms.DateInput):
    input_type = 'date'
class ActividadesForm(forms.ModelForm):

    class Meta:
        model = Actividad
        fields = "__all__"
        widgets = {
            'fecha': DateInput(),
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
            'fecha': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudesForm, self).__init__(*args, **kwargs)
        self.fields['estudiante'].initial = Estudiante.objects.get(user = User.objects.get(id = 1))
        self.fields['estado'].initial = "P"

class ProyectosForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = "__all__"
       