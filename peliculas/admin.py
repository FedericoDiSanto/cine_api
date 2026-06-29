from django.contrib import admin
from .models import Pelicula

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "categoria", "anio_creacion", "estado"]
