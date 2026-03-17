from django.contrib import admin
from .models import Tarea

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'usuario', 'completada', 'creada')
    list_filter = ('completada', 'usuario')
    search_fields = ('descripcion',)