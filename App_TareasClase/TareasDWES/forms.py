from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Tarea, Usuario

# FORMULARIO CREAR USUARIO
class UsuarioForm(UserCreationForm):
    # Campo extra para confirmar email
    confirmar_email = forms.EmailField(
        label="Confirmar email",
        widget=forms.EmailInput(attrs={'placeholder': 'usuario@fpvirtualaragon.es'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'confirmar_email', 'rol', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'placeholder': 'usuario@fpvirtualaragon.es'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        confirmar_email = cleaned_data.get('confirmar_email')
        rol = cleaned_data.get('rol')

        # Username único (case-insensitive)
        if username and Usuario.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'Ya existe un usuario con este nombre de usuario')

        # Confirmar_email coincida con email
        if email and confirmar_email and email != confirmar_email:
            self.add_error('confirmar_email', 'Los emails no coinciden')

        # Rol válido
        if rol not in [Usuario.ALUMNO, Usuario.PROFESOR]:
            self.add_error('rol', 'Rol inválido')

        return cleaned_data


# FORMULARIO CREAR TAREA INDIVIDUAL

class TareaIndividualForm(forms.ModelForm):

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_entrega', 'requiere_validacion', 'profesor_validador', 'creada_por']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título de la tarea'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción de la tarea'}),
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
            'profesor_validador': forms.Select(attrs={'class': 'form-select'}),

            # Como no estoy utilizando login, muestro todos los usuarios en creada_por
            # para poder seleccionar quién crea la tarea
            'creada_por': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar profesores en el campo profesor_validador
        self.fields['profesor_validador'].queryset = Usuario.objects.filter(rol=Usuario.PROFESOR)
        self.fields['profesor_validador'].required = False  # Solo obligatorio si requiere_validacion=True

        # Campo creada_por: todos los usuarios (alumnos y profesores)
        self.fields['creada_por'].queryset = Usuario.objects.all()
        self.fields['creada_por'].required = True

    def clean(self):
        cleaned_data = super().clean()
        fecha_entrega = cleaned_data.get('fecha_entrega')
        requiere_validacion = cleaned_data.get('requiere_validacion')
        profesor_validador = cleaned_data.get('profesor_validador')
        creada_por = cleaned_data.get('creada_por')

        # Validar que la fecha de entrega no sea anterior a hoy
        if fecha_entrega and fecha_entrega < date.today():
            self.add_error('fecha_entrega', 'La fecha de entrega no puede ser anterior a hoy')

        # Validar que si requiere validación, haya un profesor asignado
        if requiere_validacion and not profesor_validador:
            self.add_error('profesor_validador', 'Debe seleccionar un profesor validador si requiere validación')

        # Validar que creada_por no sea None
        if not creada_por:
            self.add_error('creada_por', 'Debes seleccionar un usuario que crea la tarea')

        return cleaned_data

    def save(self, commit=True):
        tarea = super().save(commit=False)
        tarea.tipo = Tarea.INDIVIDUAL  # Fuerza que sea individual
        if commit:
            tarea.save()
        return tarea
