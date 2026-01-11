from django.urls import path

from .views import ListadoUsuariosView, index
# listado_usuarios

urlpatterns = [
      path('', index, name='index'),  # Página principal de TareasDWES
      # path('usuarios/', listado_usuarios, name='listado_usuarios'),  # Listado de usuarios
      path('usuarios/', ListadoUsuariosView.as_view(), name='listado_usuarios'),  # Listado de usuarios ListView
]
