from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields":("username", "email", "password")}),
        ("Informacion Personal", {"fields":("first_name", "last_name", "telefono")}),
        ("Permisos", {"fields":("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Redes sociales", {"fields":("web_site", "instagram", "twitter")})
    )