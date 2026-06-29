from django.contrib import admin
from .models import Comentario

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ["usuario", "pelicula", "fecha_mensaje", "estado"]
