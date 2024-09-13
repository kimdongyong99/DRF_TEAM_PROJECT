from rest_framework import serializers
from .models import Article, comment
from accounts.models import User


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["image", "title"]


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["image", "title", "content"]


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = ['content', 'article']