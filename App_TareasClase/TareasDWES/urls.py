from django import views
from django.urls import path

from .views import DetalleUsuarioView, ListadoUsuariosView, MisTareasView, TareasValidarView, crear_tarea_individual, crear_tarea_grupal, index, crear_usuario
# listado_usuarios

urlpatterns = [
      path('', index, name='index'),  # Página principal de TareasDWES
      # path('usuarios/', listado_usuarios, name='listado_usuarios'),  # Listado de usuarios
      path('usuarios/', ListadoUsuariosView.as_view(), name='listado_usuarios'),  # Listado de usuarios ListView
      #path('mis-datos/<int:pk>/', mis_datos, name='mis_datos'),  # Mis datos (los obtengo por pk id)
      path('mis-datos/<int:pk>/', DetalleUsuarioView.as_view(), name='mis_datos'),  # Mis datos (los obtengo por pk id) DetailView
      path('tareas/<int:pk>/', MisTareasView.as_view(), name='mis_tareas'), # Mis tareas que he creado o colaboro
      path('tareas-validar/<int:pk>/', TareasValidarView.as_view(), name='validar_tareas'), # Tareas a validar por un profesor
      path('crear-usuario/', crear_usuario, name='crear_usuario'),  # Formulario crear usuario
      path('crear-tarea-individual/', crear_tarea_individual, name='crear_tarea_individual'),  # Formulario crear tarea individual
      path('crear-tarea-grupal/', crear_tarea_grupal, name='crear_tarea_grupal'),  # Formulario crear tarea grupal
]
