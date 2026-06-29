from django.db import models
from categorias.models import Categoria
from django.db.models import SET_NULL

class Pelicula(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=SET_NULL, null=True)
    anio_creacion = models.IntegerField()
    descripcion = models.TextField()
    poster = models.ImageField(upload_to="peliculas/imagenes", blank=True, null=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

