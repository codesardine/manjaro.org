from email.policy import default
from django.db import models
from wagtail.core.models import Page
from customblocks import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel
from wagtail.search import index
import requests
import random
from django.contrib.auth import get_user_model
from wagtail.users.models import UserProfile
from manjaro.settings.base import MEDIA_ROOT, MEDIA_URL


# pre defined pages 

class Downloads(Page):
    max_count=1
    template = "home/downloads.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    def get_context(self, request):
        data_source = "https://gitlab.manjaro.org/webpage/iso-info/-/raw/master/file-info.json"
        response = requests.get(data_source)
        print(response.json())
        data = response.json()

        context = super(Downloads, self).get_context(request)
        context['data'] = data
        return context

#Downloads._meta.get_field("title").default = "Downloads"
#Downloads._meta.get_field("slug").default = "default-homepage-title"


class Donations(Page):
    max_count=1
    title = "Donations"
    template = "home/donations.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    intro = models.CharField(max_length=250, null=True)

    content = StreamField(
        [
            ("richtext", blocks.RichtextBlock()),
        ],
        null=True,
        blank=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
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


#Donations._meta.get_field("title").default = "Donations"
#Donations._meta.get_field("slug").default = "default-homepage-title"

class Team(Page):
    max_count=1
    title = "Team"
    template = "home/team.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    def get_context(self, request):
        User = get_user_model()
        users = User.objects.all()
        profiles =[]
        for user in users:
            profile = UserProfile.get_for_user(user)
            name = profile.user.get_full_name()
            title = profile.user.title
            description = profile.user.description
            try:
                avatar = f"/media/{profile.user.avatar.file}"
            except AttributeError:
                imgs =["jaro-1.png", "jaro-2.png", "jaro-3.png"]
                avatar = f"/static/img/{random.choice(imgs)}"
            tweeter = profile.user.tweeter
            github = profile.user.github
            dict = {"name": name, "title": title, "description": description, "avatar": avatar, "tweeter": tweeter, "github": github}
            profiles.append(dict) 
           
        context = super().get_context(request)
        context['users'] = profiles
        return context

#Team._meta.get_field("title").default = "Team"
#Team._meta.get_field("slug").default = "default-homepage-title"

# end pre defined pages 

class Pages(Page):
    template = "home/pages.html"
    subpage_types = []
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
    subpage_types = ['home.Pages', 'home.Downloads', 'home.Team', 'home.donations', 'contact.ContactPage']
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

    manjaro_title = models.CharField(default='', blank=True, max_length=50)
    manjaro_intro = models.CharField(default='', blank=True, max_length=200)
    partners_title = models.CharField(default='', blank=True, max_length=50)
    partners_intro = models.CharField(default='', blank=True, max_length=200)
    partners_url = models.URLField(blank=True)
    shells_intro = models.CharField(default='', blank=True, max_length=50)
    shells_title = models.CharField(default='', blank=True, max_length=50)
    shells_intro = models.CharField(default='', blank=True, max_length=200)
    footer_intro = models.CharField(default='', blank=True, max_length=200)
    footer_description = models.CharField(default='', blank=True, max_length=200)

    content_panels = Page.content_panels + [
        FieldPanel("manjaro_title"),
        FieldPanel("manjaro_intro"),
        FieldPanel("partners_title"),
        FieldPanel("partners_intro"),
        FieldPanel("partners_url"),
        FieldPanel("shells_intro"),
        FieldPanel("shells_title"),
        FieldPanel("shells_intro"),
        FieldPanel("footer_intro"),
        FieldPanel("footer_description"),
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
    
    
    