from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

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

    def get_queryset(self):
        return Usuario.objects.all().order_by('username')  # Ordenar por nombre de usuario



# VISTA MIS DATOS

# def mis_datos(request, pk):
#    try:
#        usuario = Usuario.objects.get(pk=pk)
#    except Usuario.DoesNotExist:
#        return render(request, 'mis_datos.html', {
#            'error': "Usuario incorrecto"
#        })

#   return render(request, 'mis_datos.html', {
#        'usuario': usuario
#    })

class DetalleUsuarioView(DetailView):
    model = Usuario
    template_name = 'mis_datos.html'
    context_object_name = 'datos_usuario'

    def get_object(self, queryset=None):
        # Devuelve el usuario si existe, si no None
        return Usuario.objects.filter(pk=self.kwargs.get('pk')).first()

