from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    position = models.DecimalField(decimal_places=0, max_digits=2, default=0)
    description = models.TextField(max_length=350, blank=True)
    bio = models.TextField(max_length=350, blank=True)
    title = models.CharField(max_length=50, blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    forum = models.URLField(blank=True)
    avatar = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
