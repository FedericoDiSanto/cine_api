from rest_framework.permissions import BasePermission
from comentarios.models import Comentario

class IsAdminOrReadAndCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET" or request.method == "POST":
            return True
        else:
            if 'pk' not in view.kwargs:
                return False
            comentario_id = view.kwargs["pk"]
            comentario_bd = Comentario.objects.get(pk = comentario_id)

            if request.user.id == comentario_bd.usuario.id:
                return True
            
            return False