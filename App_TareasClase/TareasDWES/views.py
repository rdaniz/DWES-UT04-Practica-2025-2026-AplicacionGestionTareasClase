from django.http import HttpResponse
from django.shortcuts import render

from .models import Usuario

# Create your views here.
def index(request):
    return HttpResponse("Bienvenido a la aplicación de gestión de tareas.")

# Vista listado de usuarios
def listado_usuarios(request):
    usuarios = Usuario.objects.all()  # Trae todos los usuarios
    return render(request, 'listado_usuarios.html', {'usuarios': usuarios})
   