from wagtail.core.models import Page
from home.models import CustomPage
from django.db import models
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField
from django import forms
from customblocks import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel
from wagtail.search import index
from django.utils.text import slugify


@register_snippet
class DocsCategory(models.Model):
    category = models.CharField(max_length=20, default="category")
    slug = models.SlugField()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(DocsCategory, self).save(*args, **kwargs)


    panels = [
        FieldPanel("category"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Docs Category"
        verbose_name_plural = "Docs Categories"


class DocsListing(CustomPage):
    max_count=1
    template = "docs-listing.html"
    subpage_types = [
        'docs.Document',
        ]
    parent_page_types = [
        'wagtailcore.Page'
    ]

    def get_context(self, request):
        context = super().get_context(request)
        if request.user.is_authenticated:
            context['nav'] = self.get_children().live().specific()
        else:
            context['nav'] = self.get_children().live().specific().public()
        context['categories'] = DocsCategory.objects.all()
        return context


class Document(CustomPage):
    template = "document.html"
    subpage_types = []
    parent_page_types = [
        'docs.DocsListing',
    ]

    categories = ParentalManyToManyField("docs.DocsCategory", blank=True)

    @property
    def category(self):
        return self.categories.first()

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.SelectMultiple)
            ],
            heading="Categories"
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=('Content')),
        ObjectList(Page.promote_panels, heading=('Promote')),
        ObjectList(Page.settings_panels, heading=('Settings')),
        YoastPanel(
            keywords='keywords',
            title='seo_title',
            search_description='search_description',
            slug='slug'
        ),
    ])

    def get_context(self, request):
        context = super().get_context(request)
        if request.user.is_authenticated:
            context['nav'] = self.get_parent().get_children().live().specific()
        else:
            context['nav'] = self.get_parent().get_children().live().specific().public()
        context['categories'] = DocsCategory.objects.all()
        return context

