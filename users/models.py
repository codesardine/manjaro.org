from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    description = models.TextField(max_length=150, blank=True)
    title = models.CharField(max_length=50, blank=True)
    tweeter = models.URLField(max_length=100, blank=True)
    github = models.URLField(max_length=100, blank=True)
    avatar = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    bio = models.TextField(max_length=250, blank=True)

