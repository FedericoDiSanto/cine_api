from rest_framework.serializers import ModelSerializer
from user.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password", "first_name", "last_name"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "telefono", "instagram", "twitter", "web_site"]