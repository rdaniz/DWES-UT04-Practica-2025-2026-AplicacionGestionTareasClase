from django.urls import path

from .views import index, listado_usuarios

urlpatterns = [
      path('', index, name='index'),  # Página principal de TareasDWES
      path('usuarios/', listado_usuarios, name='listado_usuarios'),  # Listado de usuarios
]
