from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import User
# from articles.models import Article
from .serializers import Userserializers, UserProfileSerializer, UserChangeSerializer
from .validata import passwordValidation

class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializers
    
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializers = UserProfileSerializer(user)
        # articles = Article.objects.filter(author=user.pk)
        return Response(serializers.data)
    
    def put(self, request, username):
        newpassword = pass
        if not passwordValidation(newpassword):
            return Response({'error':'비밀번호는 최소 8자이상 1개 이상의 특수문자, 숫자가 포함되어야 함'}, status=400)
        user = get_object_or_404(User, username=username)
        serializers = UserChangeSerializer(request.user, data= request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=200)
        