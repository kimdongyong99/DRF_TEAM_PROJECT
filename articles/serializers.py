from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User


# CommentLikeSerializer: 댓글의 좋아요 수 및 정보를 보여주기 위한 Serializer
class CommentLikeSerializer(serializers.ModelSerializer):
    likes = serializers.StringRelatedField(many=True)  # 댓글에 좋아요를 누른 사용자 목록
    likes_count = serializers.SerializerMethodField()  # 댓글의 좋아요 수

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Comment
        fields = ["author", "content", "likes_count", "likes", "created_at", "updated_at"]


# ArticleListSerializer: 게시글 목록에 필요한 정보만 제공
class ArticleListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()  # 게시글의 좋아요 수

    class Meta:
        model = Article
        fields = ["image", "title", "likes_count"]

    def get_likes_count(self, obj):
        return obj.likes.count()


# ArticleCreateUpdateSerializer: 게시글 생성 및 업데이트용 Serializer
class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["image", "title", "content"]


# ArticleDetailSerializer: 게시글 상세 정보와 댓글, 좋아요 수를 포함한 Serializer
class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = CommentLikeSerializer(many=True, source='article_comment')  # 게시글의 댓글 목록
    article_likes_count = serializers.SerializerMethodField()  # 게시글의 좋아요 수
    article_likes = serializers.StringRelatedField(many=True, source='likes')  # 게시글에 좋아요를 누른 사용자 목록

    def get_article_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Article
        fields = [
            "image",
            "title",
            "content",
            "created_at",
            "updated_at",
            "article_likes",
            "article_likes_count",
            "comments",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "article"]

# CommentListSerializer: 댓글 목록을 위한 간단한 Serializer
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "content", "created_at", "updated_at"]


# CommentCreateUpdateSerializer: 댓글 생성 및 업데이트용 Serializer
class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "content"]

        read_only_fields = ["author"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["author", "title", "content"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "article", "content"]