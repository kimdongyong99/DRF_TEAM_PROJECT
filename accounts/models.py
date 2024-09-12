from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField()
    image_field = models.ImageField(default="static/default/")
