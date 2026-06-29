from rest_framework.serializers import ModelSerializer
from peliculas.models import Pelicula

class PeliculaSerializer(ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ["id", "nombre", "categoria", "anio_creacion", "descripcion", "poster", "estado"]