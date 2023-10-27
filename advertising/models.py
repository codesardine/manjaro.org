from wagtail.admin.panels import FieldPanel
from django.db import models
from wagtail.admin.panels import (
    FieldPanel
)


class Advert(models.Model):
    title = models.CharField(max_length=255, null=False, default="")
    url = models.URLField(null=False, default="")
    description = models.TextField(max_length=255, null=False, default="") 
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        FieldPanel("image"),
        FieldPanel("description"),
    ]
