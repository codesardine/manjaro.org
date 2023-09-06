from wagtail.admin.panels import FieldPanel
from django.db import models
from django.conf import settings
from wagtail.admin.panels import (
    FieldPanel
)


class Advert(models.Model,):
    title = models.CharField(max_length=255, null=False, default="")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    url = models.URLField(null=False, default="")
    image = models.ImageField(null=False, default="")
    description = models.TextField(max_length=255, null=False, default="") 

    panels = [
        FieldPanel("title"),
        FieldPanel("author"),
        FieldPanel("url"),
        FieldPanel("image"),
        FieldPanel("description"),
    ]
