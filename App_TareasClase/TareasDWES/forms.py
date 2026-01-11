from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

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

