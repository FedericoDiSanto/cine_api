from rest_framework.viewsets import ModelViewSet
from comentarios.api.permissions import IsAdminOrReadAndCreateOnly
from comentarios.models import Comentario
from comentarios.api.serializers import ComentarioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class ComentarioViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadAndCreateOnly]
    serializer_class = ComentarioSerializer
    queryset = Comentario.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["estado", "usuario", "pelicula"]
    ordering = ["-fecha_mensaje"]
