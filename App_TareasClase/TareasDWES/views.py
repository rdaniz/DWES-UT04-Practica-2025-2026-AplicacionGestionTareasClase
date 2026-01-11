from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from .forms import UsuarioForm

from .models import Tarea, Usuario



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


# VISTA MIS TAREAS

class MisTareasView(ListView):
    model = Tarea
    template_name = 'mis_tareas_alumno.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        self.usuario = Usuario.objects.filter(pk=pk).first()

        if not self.usuario:
            # Devuelve none si el usuario no existe
            return Tarea.objects.none()

        # Tareas individuales creadas por el usuario
        tareas_creadas = Tarea.objects.filter(creada_por=self.usuario)

        # Tareas grupales en las que el usuario es colaborador
        tareas_grupales = Tarea.objects.filter(
            detalle_grupal__colaboradores=self.usuario
        )

        # Unión y orden por tipo y fecha de creación
        return tareas_creadas.union(tareas_grupales).order_by('tipo', 'fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.usuario
        return context
    

# VISTA TAREAS VALIDAR PROFESOR

class TareasValidarView(ListView):
    model = Tarea
    template_name = 'tareas_validar_profesor.html'
    context_object_name = 'validar_tareas'

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        # Obtener profesor por pk
        self.profesor = Usuario.objects.filter(pk=pk, rol=Usuario.PROFESOR).first()

        # Si no existe o no es profesor muestro none
        if not self.profesor:
            return Tarea.objects.none()

        # Tareas pendientes de validar el profesor
        return Tarea.objects.filter(
            requiere_validacion=True,
            validada=False,
            profesor_validador=self.profesor
        ).order_by('fecha_entrega')

    def get_context_data(self, **kwargs):

        # super() llama al método original de ListView
        # Ese método ya crea un diccionario con:
        # validar_tareas (tu context_object_name), object_list, view, etc.
        context = super().get_context_data(**kwargs)

        # Variable profesor para usar en template
        context['profesor'] = self.profesor
        return context
    
    
# FORMULARIO CREAR USUARIO

def crear_usuario(request):
    form = UsuarioForm(request.POST or None)

    if form.is_valid():
        usuario = form.save()  # Guarda el usuario en la BD
        return redirect('mis_datos', pk=usuario.pk) # Redirige a la vista mis_datos del nuevo usuario
        
    return render(request, 'usuario_form.html', {'form': form})