from django.db import models
from accounts.models import User


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article', null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='like_articles', black=True)
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comment', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='like_comments', black=True)
    
    def __str__(self):
        return self.content