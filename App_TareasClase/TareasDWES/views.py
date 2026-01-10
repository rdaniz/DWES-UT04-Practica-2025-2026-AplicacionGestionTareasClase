from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Bienvenido a la aplicación de gestión de tareas.")