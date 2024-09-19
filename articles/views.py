from django.shortcuts import render
from rest_framework.decorators import permission_classes

from .models import Article, Comment
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from .serializers import (
    ArticleListSerializer,
    ArticleCreateUpdateSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentCreateUpdateSerializer,
    CommentLikeSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db.models import Count
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)


class ArticleListView(ListCreateAPIView):
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        search = self.request.query_params.get("search")
        order_by = self.request.query_params.get("order_by")
        queryset = Article.objects.all()

        # 검색
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        # 정렬
        if order_by == "likes":
            queryset = queryset.annotate(likes_count=Count("likes")).order_by(
                "-likes_count"
            )
        else:  # 기본값은 최신순
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleListSerializer
        return ArticleCreateUpdateSerializer


class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsAuthenticated]

    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        likes_count = article.likes.count()
        return Response({"likes_count": likes_count}, status=status.HTTP_200_OK)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response(
                {"message": "좋아요 취소", "like_count": article.likes.count()},
                status=status.HTTP_200_OK,
            )
        else:
            article.likes.add(request.user)
            return Response(
                {"message": "좋아요", "like_count": article.likes.count()},
                status=status.HTTP_200_OK,
            )


class CommentListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all().order_by("-pk")
    serializer_class = CommentListSerializer

    def perform_create(self, serializer):
        author = self.request.user
        article = get_object_or_404(Article, pk=self.kwargs["pk"])
        serializer.save(author=author, article=article)


class CommentUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return CommentCreateUpdateSerializer


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment_count = comment.likes.count()
        serializer = CommentLikeSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response(
                {"message": "좋아요 취소", "like_count": comment.likes.count()},
                status=status.HTTP_200_OK,
            )
        else:
            comment.likes.add(request.user)
            return Response(
                {"message": "좋아요", "like_count": comment.likes.count()},
                status=status.HTTP_200_OK,
            )
