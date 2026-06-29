from rest_framework.viewsets import ModelViewSet
from peliculas.api.serializers import PeliculaSerializer
from peliculas.models import Pelicula
from .permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class PeliculaViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = PeliculaSerializer
    queryset = Pelicula.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["estado", "categoria"]
    ordering = ["-anio_creacion"]