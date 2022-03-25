from django.db import models
from wagtail.core.models import Page
from customblocks import blocks

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel


class Downloads(Page):
    max_count=1
    title = "Downloads"
    template = "home/downloads.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]


class Team(Page):
    max_count=1
    title = "Team"
    template = "home/team.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]


class Pages(Page):
    template = "home/pages.html"
    subpage_types = ['home.Pages']
    parent_page_types = [
        'home.HomePage'
    ]

    content = StreamField(
        [
            ("richtext", blocks.RichtextBlock()),
            ("product_details", blocks.ProductBlock()),        
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    keywords = models.CharField(default='', blank=True, max_length=100)

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


class HomePage(Page):
    max_count=1
    template = "home/home-page.html"
    subpage_types = ['home.Pages', 'home.Downloads', 'home.Team']
    parent_page_types = [
        'wagtailcore.Page'
    ]

    content = StreamField(
        [
            ("richtext", blocks.RichtextBlock()),
            ("product_details", blocks.ProductBlock()),        
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    keywords = models.CharField(default='', blank=True, max_length=100)

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
    
    
    