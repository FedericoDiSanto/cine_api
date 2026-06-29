from rest_framework.routers import DefaultRouter
from peliculas.api.views import PeliculaViewSet

router_pelicula = DefaultRouter()
router_pelicula.register(prefix="pelicula", basename="pelicula", viewset=PeliculaViewSet)
