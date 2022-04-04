from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    description = models.TextField(max_length=150, blank=True)
    title = models.CharField(max_length=50, blank=True)
    tweeter = models.URLField(max_length=100, blank=True)
    github = models.URLField(max_length=100, blank=True)
    avatar = models.ImageField(
        verbose_name='profile picture',
        upload_to="static/img",
        blank=True,
    )

