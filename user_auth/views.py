from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from user_auth.models import User
from user_auth.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
