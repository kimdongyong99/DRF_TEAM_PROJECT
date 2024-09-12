from django.shortcuts import render
from .models import Article
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import (
    ArticleListSerializer,
    ArticleCreateUpdateSerializer,
    ArticleDetailSerializer,
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
