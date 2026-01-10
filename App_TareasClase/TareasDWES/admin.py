from django.contrib import admin
from .models import Usuario, Tarea, TareaGrupal

# Register your models here.
from django.contrib import admin

admin.site.register(Usuario)
admin.site.register(Tarea)
admin.site.register(TareaGrupal)
