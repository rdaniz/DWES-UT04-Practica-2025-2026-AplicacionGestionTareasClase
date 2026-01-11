from django.urls import path

from .views import DetalleUsuarioView, ListadoUsuariosView, index
# listado_usuarios

urlpatterns = [
      path('', index, name='index'),  # Página principal de TareasDWES
      # path('usuarios/', listado_usuarios, name='listado_usuarios'),  # Listado de usuarios
      path('usuarios/', ListadoUsuariosView.as_view(), name='listado_usuarios'),  # Listado de usuarios ListView
      #path('mis-datos/<int:pk>/', mis_datos, name='mis_datos'),  # Mis datos (los obtengo por pk id)
      path('mis-datos/<int:pk>/', DetalleUsuarioView.as_view(), name='mis_datos'),  # Mis datos (los obtengo por pk id) DetailView
]
