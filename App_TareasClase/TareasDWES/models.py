import uuid
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    creada_por = models.ForeignKey(
        # Usuario, on_delete=models.CASCADE, related_name='tareas_creadas')

        # Modifico on_delete=models.CASCADE porque si borro al creador de una tarea se borrará la tarea
        # pero si es grupal, los colaboradores seguirán, por lo que quiero que se mantenga la tarea.
        Usuario, null=True, on_delete=models.SET_NULL, related_name='tareas_creadas')
    requiere_validacion = models.BooleanField(default=False)
    validada = models.BooleanField(default=False)
    profesor_validador = models.ForeignKey(
        Usuario, null=True, on_delete=models.SET_NULL, related_name='tareas_a_validar')

    # Además del título muestro el id para poder añadirlo a la url y buscar la tarea
    def __str__(self):
        return f"{self.titulo} - {self.id}"

# Crear modelo Tarea Grupal

# La tabla Tarea es común a todas las tareas.
# TareaGrupal solo existe si Tarea.tipo es grupal.

# OneToOneField con Tarea:
# Cada tarea grupal corresponde a una tarea.
# Una tarea solo puede tener un detalle grupal.

# on_delete=models.CASCADE
# Si se elimina la tarea principal, se elimina su información grupal.

# ManyToManyField
# Una tarea grupal puede tener muchos usuarios.
# Un usuario puede estar en muchas tareas grupales.

    # Django crea automáticamente una tabla intermedia con dos FK: tareagrupal_id y usuario_id.

class TareaGrupal(models.Model):
    tarea = models.OneToOneField(Tarea, on_delete=models.CASCADE, related_name='detalle_grupal')
    colaboradores = models.ManyToManyField(Usuario, related_name='tareas_grupales')

    def __str__(self):
        return f"Tarea grupal: {self.tarea.titulo}"