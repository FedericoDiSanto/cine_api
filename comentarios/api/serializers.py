from rest_framework.serializers import ModelSerializer
from comentarios.models import Comentario

class ComentarioSerializer(ModelSerializer):
    class Meta:
        model = Comentario
        fields = ["id", "mensaje", "fecha_mensaje", "estado", "pelicula", "usuario"]