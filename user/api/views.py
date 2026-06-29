from rest_framework.views import APIView
from user.api.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from user.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserUpdateSerializer(request.user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)