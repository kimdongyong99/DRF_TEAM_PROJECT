from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # article_likes = models.ManyToManyField()
    first_name = None
    last_name = None
    email = models.EmailField()
    image_field = models.ImageField(default="static/default/")
