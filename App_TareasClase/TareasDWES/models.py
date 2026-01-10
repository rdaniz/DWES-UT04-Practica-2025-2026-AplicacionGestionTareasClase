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


# Crear modelo Tarea
class Tarea(models.Model):
    INDIVIDUAL = 'individual'
    GRUPAL = 'grupal'

    TIPO_CHOICES = [
        (INDIVIDUAL, 'Individual'),
        (GRUPAL, 'Grupal'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    creada_por = models.ForeignKey(
        'TareasDWES.Usuario', on_delete=models.CASCADE, related_name='tareas_creadas')
    requiere_validacion = models.BooleanField(default=False)
    validada = models.BooleanField(default=False)
    profesor_validador = models.ForeignKey(
        'TareasDWES.Usuario', null=True, blank=True, on_delete=models.SET_NULL, related_name='tareas_a_validar')

    # Además del título muestro el id para poder añadirlo a la url y buscar la tarea
    def __str__(self):
        return f"{self.titulo} - {self.id}"
