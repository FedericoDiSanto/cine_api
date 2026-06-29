from rest_framework.routers import DefaultRouter
from categorias.api.views import CategoriaModelViewSet

router_categoria = DefaultRouter()
router_categoria.register(prefix="categoria", basename="categoria", viewset=CategoriaModelViewSet)