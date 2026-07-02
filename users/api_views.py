from rest_framework import viewsets, permissions, generics
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    # CreateAPIView - Provides a post method handler.
    #generics have individual classes for CRUD
    #so we need only POST
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    #RetrieveUpdateAPIView = GET for viewing, PUT/PATCH for update
    serializer_class = UserSerializer

    def get_object(self):
        #returning only user profile
        return self.request.user
