from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Usuario

# Create your views here.

# VISTA INDEX

# def index(request):
#     return HttpResponse("Bienvenido a la aplicación de gestión de tareas.")

def index(request):
    return render(request, 'index.html')



# VISTA LISTADO DE USUARIOS

# def listado_usuarios(request):
#     usuarios = Usuario.objects.all()  # Trae todos los usuarios
#     return render(request, 'listado_usuarios.html', {'usuarios': usuarios})

class ListadoUsuariosView(ListView):
    model = Usuario
    template_name = 'listado_usuarios.html'  # Template
    context_object_name = 'usuarios'        # Nombre de la variable en el template