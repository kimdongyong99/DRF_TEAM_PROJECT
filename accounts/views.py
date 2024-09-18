from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import User

from .serializers import Userserializers, UserProfileSerializer, UserChangeSerializer
from .validata import passwordValidation
from articles.models import Article

class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializers
    
    permission_classes = [AllowAny]
    
class UserProfileView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializers = UserProfileSerializer(user)
        return Response(serializers.data)

    def put(self, request, username):
        if request.data.get("new_password") is not None :
            new_password = request.data.get("new_password")
            if not passwordValidation(new_password):
                return Response({'Error':'비밀번호는 최소 8자이상 1개 이상의 특수문자, 숫자가 포함되어야 함'}, status=400)
            varify_password = request.data.get("varify_password")
            if new_password != varify_password:
                return Response({"Error": "비밀번호가 일치하지 않습니다"}, status=400)

        user = get_object_or_404(User, username=username)
        serializers = UserChangeSerializer(request.user, data= request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            if request.data.get("new_password") is not None :
                user.set_password(new_password)
            user.save()
        return Response({"detail": "정보수정이 완료되었습니다", "data":serializers.data}, status=200)
    
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user != user and not request.user.is_superuser:
            return Response({"Error": "삭제 권한이 없습니다."}, status=403)
        user.is_active = False
        return Response({"message": "회원탈퇴가 완료되었습니다."}, status=204)