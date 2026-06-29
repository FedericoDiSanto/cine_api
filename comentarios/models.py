from django.db import models
from peliculas.models import Pelicula
from user.models import User
from django.db.models import SET_NULL, CASCADE


class Comentario(models.Model):
    mensaje = models.TextField()
    fecha_mensaje = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    pelicula = models.ForeignKey(Pelicula, on_delete=SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.pelicula}"