from django.urls import path

from .views import DetalleUsuarioView, ListadoUsuariosView, MisTareasView, TareasValidarView, index
# listado_usuarios

urlpatterns = [
      path('', index, name='index'),  # Página principal de TareasDWES
      # path('usuarios/', listado_usuarios, name='listado_usuarios'),  # Listado de usuarios
      path('usuarios/', ListadoUsuariosView.as_view(), name='listado_usuarios'),  # Listado de usuarios ListView
      #path('mis-datos/<int:pk>/', mis_datos, name='mis_datos'),  # Mis datos (los obtengo por pk id)
      path('mis-datos/<int:pk>/', DetalleUsuarioView.as_view(), name='mis_datos'),  # Mis datos (los obtengo por pk id) DetailView
      path('tareas/<int:pk>/', MisTareasView.as_view(), name='mis_tareas'), # Mis tareas que he creado o colaboro
      path('tareas-validar/<int:pk>/', TareasValidarView.as_view(), name='validar_tareas'), # Tareas a validar por un profesor
]
