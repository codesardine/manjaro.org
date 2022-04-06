from django.db import models
from wagtail.core.models import Page
from customblocks import blocks
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
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

    intro = models.CharField(default='', blank=True, max_length=50)
    description = models.TextField(default='', blank=True, max_length=200)

    question_one = models.CharField(default='', blank=True, max_length=50)
    answer_one = models.TextField(default='', blank=True, max_length=200)

    question_two = models.CharField(default='', blank=True, max_length=50)
    answer_two = models.TextField(default='', blank=True, max_length=200)

    question_three = models.CharField(default='', blank=True, max_length=50)
    answer_three = models.TextField(default='', blank=True, max_length=200)

    team_spins_intro = models.TextField(default='', blank=True, max_length=200)
    community_spins_intro = models.TextField(default='', blank=True, max_length=200)
    arm_spins_intro = models.TextField(default='', blank=True, max_length=200)
    manual_intro = models.TextField(default='', blank=True, max_length=200)
    docker_intro = models.TextField(default='', blank=True, max_length=200)

    xfce_description = models.TextField(default='', blank=True, max_length=150)
    xfce_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    xfce_notes = models.TextField(default='', blank=True, max_length=200)

    plasma_description = models.TextField(default='', blank=True, max_length=150)
    plasma_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    plasma_notes = models.TextField(default='', blank=True, max_length=200)

    gnome_description = models.TextField(default='', blank=True, max_length=150)
    gnome_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    gnome_notes = models.TextField(default='', blank=True, max_length=200)

    cinnamon_description = models.TextField(default='', blank=True, max_length=150)
    cinnamon_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cinnamon_notes = models.TextField(default='', blank=True, max_length=200)

    i3_description = models.TextField(default='', blank=True, max_length=150)
    i3_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    i3_notes = models.TextField(default='', blank=True, max_length=200)

    budgie_description = models.TextField(default='', blank=True, max_length=150)
    budgie_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    budgie_notes = models.TextField(default='', blank=True, max_length=200)

    mate_description = models.TextField(default='', blank=True, max_length=150)
    mate_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    mate_notes = models.TextField(default='', blank=True, max_length=200)

    sway_description = models.TextField(default='', blank=True, max_length=150)
    sway_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    sway_notes = models.TextField(default='', blank=True, max_length=200)


    edition_panels = [
        FieldPanel("xfce_description"),
        #ImageChooserPanel('xfce_image'),
        FieldPanel("xfce_notes"),
        FieldPanel("plasma_description"),
        #ImageChooserPanel('plasma_image'),
        FieldPanel("plasma_notes"),
        FieldPanel("gnome_description"),
        #ImageChooserPanel('gnome_image'),
        FieldPanel("gnome_notes"),

        FieldPanel("cinnamon_description"),
        #ImageChooserPanel('cinnamon_image'),
        FieldPanel("cinnamon_notes"),
        FieldPanel("budgie_description"),
        #ImageChooserPanel('budgie_image'),
        FieldPanel("budgie_notes"),
        FieldPanel("i3_description"),
        #ImageChooserPanel('i3_image'),
        FieldPanel("i3_notes"),
        FieldPanel("mate_description"),
        #ImageChooserPanel('mate_image'),
        FieldPanel("mate_notes"),
        FieldPanel("sway_description"),
        #ImageChooserPanel('sway_image'),
        FieldPanel("sway_notes"),
    ]
    

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("description"),
        FieldPanel("question_one"),
        FieldPanel("answer_one"),
        FieldPanel("question_two"),
        FieldPanel("answer_two"),
        FieldPanel("question_three"),
        FieldPanel("answer_three"),
        FieldPanel("team_spins_intro"),
        FieldPanel("community_spins_intro"),
        FieldPanel("arm_spins_intro"),
        FieldPanel("manual_intro"),
        FieldPanel("docker_intro"),
    ]
    

    def get_context(self, request):
        data_source = "https://gitlab.manjaro.org/webpage/iso-info/-/raw/master/file-info.json"
        response = requests.get(data_source)
        data = response.json()

        context = super(Downloads, self).get_context(request)
        context['data'] = data
        return context


    keywords = models.CharField(default='', blank=True, max_length=100)

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=('Content')),
        ObjectList(edition_panels, heading=('Editions')),
        ObjectList(Page.promote_panels, heading=('Promote')),
        ObjectList(Page.settings_panels, heading=('Settings')),
        YoastPanel(
            keywords='keywords',
            title='seo_title',
            search_description='search_description',
            slug='slug'
        ),
    ])

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
    
    
    