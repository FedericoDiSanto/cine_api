from user.api.views import UserView, RegisterUserView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("auth/register/", RegisterUserView.as_view(), name="register"),
    path("auth/me/", UserView.as_view(), name="me"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
