from django.db import models

# Importar AbstractUser para extender el modelo de usuario predeterminado
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Crear modelo usuario extendido de AbstractUser
# creando los roles de alumno y profesor

class Usuario(AbstractUser):
    ALUMNO = 'alumno'
    PROFESOR = 'profesor'

    ROL_CHOICES = [
        (ALUMNO, 'Alumno'),
        (PROFESOR, 'Profesor'),
    ]

    # En default el rol es PROFESOR porque al crear el superusuario desde consola
    # no me pide el campo rol y si el default fuera ALUMNO,
    # un Alumno no puede ser superusuario

    rol = models.CharField(max_length=10,choices=ROL_CHOICES, default=PROFESOR)

    def __str__(self):
        return f"{self.username} ({self.rol})"
