from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import Userserializers


# Create your views here.

class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializers