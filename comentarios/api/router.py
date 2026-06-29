from rest_framework.routers import DefaultRouter
from comentarios.api.views import ComentarioViewSet

router_comentario = DefaultRouter()
router_comentario.register(prefix="comentario", basename="comentario", viewset=ComentarioViewSet)