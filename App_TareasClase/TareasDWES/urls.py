from django.urls import path

from .views import index

urlpatterns = [
     path('', index, name='index'),  # Página principal de TareasDWES
]
