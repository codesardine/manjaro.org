from django.db import models
from django_extensions.db.fields import AutoSlugField
from wagtail.admin.edit_handlers import (
    MultiFieldPanel,
    InlinePanel,
    FieldPanel,
    PageChooserPanel
)
from wagtail.snippets.models import register_snippet
from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

class MenuItem(Orderable):
    
    link_title = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    link_url = models.CharField(
        max_length=500,
        blank=True
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab")
    ]

    @property
    def link(self) -> str:
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return "#"

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing Title"


@register_snippet
class Menu(ClusterableModel):
    
    title = models.CharField(max_length=50, null=True, help_text="Options: top left, top right, footer one, footer two, footer three, footer four")
    category_title = models.CharField(max_length=50, null=True, help_text="Visible name of the menu, footer menus only")
    slug = AutoSlugField(populate_from="title", editable=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("category_title"),
            FieldPanel("title"),
            FieldPanel("slug")
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]
    
    def __str__(self) -> str:
        return self.title
    