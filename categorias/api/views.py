from categorias.api.serializers import CategoriaSerializer
from rest_framework.viewsets import ModelViewSet
from categorias.models import Categoria
from categorias.api.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class CategoriaModelViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["genero"]