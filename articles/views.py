from django.shortcuts import render
from .models import Article,Comment
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView)
from rest_framework.views import APIView
from .serializers import (
    ArticleListSerializer,
    ArticleCreateUpdateSerializer,
    ArticleDetailSerializer,
    CommentListSerializer,
    CommentCreateUpdateSerializer,
    CommentLikeSerializer,

)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

class ArticleListView(ListCreateAPIView):
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search = self.request.query_params.get("search")
        if search:
            return Article.objects.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        return Article.objects.all().order_by("-pk")



    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleListSerializer
        return ArticleCreateUpdateSerializer


class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleDetailSerializer
        elif self.request.method == "PATCH":
            return ArticleCreateUpdateSerializer
        elif self.request.method == "PUT":
            return ArticleCreateUpdateSerializer


class ArticleLikeView(APIView):
    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        likes_count = article.likes.count()
        serializer = ArticleLikeSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"message": "좋아요 취소", "like_count": article.likes.count()}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"message": "좋아요", "like_count": article.likes.count()}, status=status.HTTP_200_OK)
    

        
class CommentListCreateView(ListCreateAPIView):
    queryset = Comment.objects.all().order_by("-pk")
    serializer_class = CommentListSerializer

    def perform_create(self, serializer):
        author = self.request.user
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        serializer.save(author = author, article = article)


class CommentUpdateDeleteView(UpdateAPIView,DestroyAPIView):
    queryset = Comment.objects.all()
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return CommentCreateUpdateSerializer
        
        
class CommentLikeView(APIView):
    def get(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment_count = comment.likes.count()
        serializer = CommentLikeSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({"message": "좋아요 취소", "like_count": comment.likes.count()}, status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
            return Response({"message": "좋아요", "like_count": comment.likes.count()}, status=status.HTTP_200_OK)
        
    
