from rest_framework import serializers
from .models import Article, Comment
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
        

class ArticleLikeSerializer(serializers.ModelSerializer):
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = Article
        fields = ["likes", "likes_count"]


class ArticleDetailSerializer(ArticleLikeSerializer):
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = Article
        fields = "__all__"
        
        
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", 'content','created_at', 'updated_at']


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "content"]
    
        read_only_fields = ["author"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "article"]
        
        
class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["likes", "like_count"]