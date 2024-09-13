from django.shortcuts import render
from .models import Article,Comment
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView)
from .serializers import (
    ArticleListSerializer,
    ArticleCreateUpdateSerializer,
    ArticleDetailSerializer,
    CommentListSerializer,
    CommentCreateUpdateSerializer,
)
from django.shortcuts import get_object_or_404


# Create your views here.
class ArticleListView(ListCreateAPIView):
    queryset = Article.objects.all().order_by("-pk")


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