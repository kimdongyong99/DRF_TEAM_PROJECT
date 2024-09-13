from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import User
# from articles.models import Article
from .serializers import Userserializers, UserProfileSerializer, UserChangeSerializer
from articles.models import Article


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializers
    
    permission_classes = [AllowAny]
    
class UserProfileView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializers = UserProfileSerializer(user)
        return Response(serializers.data)
    
    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user:
            return Response({"error":"수정 권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)
        
        serializers = UserChangeSerializer(request.user, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user and not request.user.is_superuser:
            return Response({"error": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({"message": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
    
        