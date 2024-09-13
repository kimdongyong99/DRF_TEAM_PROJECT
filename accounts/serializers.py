from .models import User
from articles.models import Article, Comment
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from articles.serializers import ArticleListSerializer, CommentSerializer

class Userserializers(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    checkpassword = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data["password"] != data["checkpassword"]:
            raise serializers.ValidationError("똑같은 비밀번호를 입력하세요.")
        return data

    def create(self, data):
        data.pop("checkpassword")

        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )
        return user

    class Meta:
        model = User
        fields = ["username", "email", "password", "checkpassword"]


class UserProfileSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    like_articles = serializers.SerializerMethodField()
    like_comments= serializers.SerializerMethodField()
    
    class Meta:
        model = User
        
    def get_articles(self, obj):
        articles = Article.objects.filter(author=obj)
        return ArticleListSerializer(articles, many=True).data
    
    def get_like_articels(self, obj):
        like_articles = obj.like_articles.all()
        return ArticleListSerializer(like_articles, many=True).data
    
    def get_like_comments(self, obj):
        like_comments = obj.like_comments.all()
        return CommentSerializer(like_comments, many=True).data
    
        fields = ['username', 'email', 'image_field', 'articles', 'like_articles', 'like_comment']
class UserChangeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User 
        fields = ['username', 'image_field', 'email', 'password']