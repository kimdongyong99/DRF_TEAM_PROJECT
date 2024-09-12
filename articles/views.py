from django.shortcuts import render
from .models import Article
from rest_framework.generics import ListCreateAPIView
from articles.serializers import ArticleListSerializer, ArticleCreateSerializer


# Create your views here.
class ArticleListView(ListCreateAPIView):
    queryset = Article.objects.all().order_by("-pk")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleListSerializer
        return ArticleCreateSerializer
