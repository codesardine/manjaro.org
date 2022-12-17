from django.db import models
from wagtail.core.models import Page
from customblocks import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel
from wagtail.search import index
import requests
import random
from django.contrib.auth import get_user_model
from wagtail.users.models import UserProfile
from manjaro.settings.base import MEDIA_ROOT, MEDIA_URL
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import redirect
from puput.models import EntryPage

import urllib.request
import json
import concurrent.futures

def get_sitemap_urls(self, request=None):
    # fix for https://github.com/APSL/puput/issues/225
    from wagtail.core.models import Site
    from puput.urls import get_entry_url
    root_page = Site.find_for_request(request).root_page
    root_url = self.get_url_parts()[1]
    
    # use root_page instance, not root_url
    entry_url = get_entry_url(self, self.blog_page.page_ptr, root_page) 
    return [
        {
            'location': root_url + entry_url,
            # fall back on latest_revision_created_at if last_published_at is null
            # (for backwards compatibility from before last_published_at was added)
            'lastmod': (self.last_published_at or self.latest_revision_created_at),
        }
    ]

EntryPage.get_sitemap_urls = get_sitemap_urls


class UpdateStatus(Page):
    max_count=1
    template = "home/update-status.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]
    
    def get_context(self, request):
        
        def _get_votes(topic):
            """read one subject"""
            with urllib.request.urlopen(f"https://forum.manjaro.org/t/{topic['id']}.json") as f_url:
                req = f_url.read()
            post = json.loads(req)['post_stream']['posts'][0]
            topic['voters'] = 0
            if post['polls'][0]['voters'] > 0:
                topic['voters'] = post['polls'][0]['voters']
                
            topic['poll_ok'] = post['polls'][0]['options'][0]['votes']
            pourcentage = round((post['polls'][0]['options'][0]['votes'] / post['polls'][0]['voters']) * 100)
            topic['poll_pourcent'] = 100 - pourcentage
            topic['poll_thanks'] = post['polls'][0]['options'][1]['votes']
            topic['poll_opps'] = post['polls'][0]['options'][2]['votes']

        branch = request.GET.get('branch', None)
        arm = request.GET.get('arm', None)
        if branch not in ("stable", "testing", "unstable"):
            branch = "stable"

        if arm == "true":
            updates_url = f"https://forum.manjaro.org/c/arm/{branch}-updates.json"
        else:
            updates_url = f"https://forum.manjaro.org/c/announcements/{branch}-updates.json"

        with urllib.request.urlopen(updates_url) as f_url:
            req = f_url.read()

        # doc: https://docs.discourse.org/#tag/Categories
        topics = json.loads(req)['topic_list']['topics']
        post_limit = 4
        topics = [t for t in topics if not t['title'].startswith('About')][0:post_limit]  # limit 12 / 30

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=post_limit) as executor:
            futures.append(executor.map(_get_votes, topics))
        
        context = super().get_context(request)
        context["branch"] = branch
        context["topics"] = topics
        context["arm"] = arm
        return context

    intro = models.TextField(default='', blank=True, max_length=350)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    keywords = models.CharField(default='', blank=True, max_length=150)

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


class Downloads(RoutablePageMixin, Page):
    max_count=1
    template = "home/downloads.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    intro = models.TextField(default='', blank=True, max_length=700)

    manjaro_team_intro = models.TextField(default='', blank=True, max_length=200)
    community_intro = models.TextField(default='', blank=True, max_length=200)
    manjaro_arm_team_intro = models.TextField(default='', blank=True, max_length=200)

    xfce_description = models.TextField(default='', blank=True, max_length=350)
    plasma_description = models.TextField(default='', blank=True, max_length=350)
    gnome_description = models.TextField(default='', blank=True, max_length=350)
    cinnamon_description = models.TextField(default='', blank=True, max_length=350)
    i3_description = models.TextField(default='', blank=True, max_length=350)
    budgie_description = models.TextField(default='', blank=True, max_length=350)
    mate_description = models.TextField(default='', blank=True, max_length=350)
    sway_description = models.TextField(default='', blank=True, max_length=350)
    docker_intro = models.TextField(default='', blank=True, max_length=350)
    
    phosh_description = models.TextField(default='', blank=True, max_length=350)
    plasma_mobile_description = models.TextField(default='', blank=True, max_length=350)
    minimal_description = models.TextField(default='', blank=True, max_length=350)

    edition_panels = [
        FieldPanel("xfce_description"),
        FieldPanel("plasma_description"),
        FieldPanel("gnome_description"),
        
        FieldPanel("cinnamon_description"),
        FieldPanel("budgie_description"),
        FieldPanel("i3_description"),
        FieldPanel("mate_description"),
        FieldPanel("sway_description"),
        FieldPanel("docker_intro"),

        FieldPanel("phosh_description"),
        FieldPanel("plasma_mobile_description"),
        FieldPanel("minimal_description"),
    ]
    

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("manjaro_team_intro"),
        FieldPanel("community_intro"),
        FieldPanel("manjaro_arm_team_intro"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("manjaro_team_intro"),
        index.SearchField("community_intro"),
        index.SearchField("manjaro_arm_team_intro"),
        index.SearchField("docker_intro")
    ]
    
    def get_iso_info(self):
        data_source = "https://gitlab.manjaro.org/webpage/iso-info/-/raw/master/file-info.json"
        response = requests.get(data_source)
        return response.json()

    def get_context(self, request):    
        context = super(Downloads, self).get_context(request)
        context['data'] = self.get_iso_info()
        return context

    @route(r"^plasma/$")
    def plasma(self, request):
        iso_info = self.get_iso_info()
        iso = iso_info["official"]["plasma"]["image"]
        return redirect(iso)

    @route(r"^xfce/$")
    def xfce(self, request):
        iso_info = self.get_iso_info()
        iso = iso_info["official"]["xfce"]["image"]
        return redirect(iso)

    @route(r"^gnome/$")
    def gnome(self, request):
        iso_info = self.get_iso_info()
        iso = iso_info["official"]["gnome"]["image"]
        return redirect(iso)

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


class Donations(Page):
    max_count=1
    template = "home/donations.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    intro = models.TextField(max_length=350, null=True)

    content = StreamField(
        [
            ("richtext", blocks.RichtextBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel("content"),
    ]

    keywords = models.CharField(default='', blank=True, max_length=150)

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


class Hardware(Page):
    max_count=1
    template = "home/hardware.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    intro = models.TextField(max_length=350, null=True)

    content = StreamField(
        [
            ("product_details", blocks.ProductBlock()),        
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel("content"),
    ]

    reviews = StreamField(
        [
            ("reviews", blocks.UrlBlock()),        
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    reviews_panels = [
        FieldPanel("reviews"),
    ]

    keywords = models.CharField(default='', blank=True, max_length=150)

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=('Content')),
        ObjectList(reviews_panels, heading=('Video Reviews')),
        ObjectList(Page.promote_panels, heading=('Promote')),
        ObjectList(Page.settings_panels, heading=('Settings')),
        YoastPanel(
            keywords='keywords',
            title='seo_title',
            search_description='search_description',
            slug='slug'
        ),
    ])


class Features(Page):
    max_count=1
    template = "home/features.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    intro =  models.TextField(blank=True, max_length=450)
    branches_intro =  models.TextField(blank=True, max_length=650)
    arch_linux_intro =  models.TextField(blank=True, max_length=350)
    unstable_intro =  models.TextField(blank=True, max_length=350)
    testing_intro =  models.TextField(blank=True, max_length=350)
    stable_intro =  models.TextField(blank=True, max_length=350)

    pamac_intro =  models.TextField(blank=True, max_length=500)
    package_formats_intro =  models.TextField(blank=True, max_length=350)
    updates_intro =  models.TextField(blank=True, max_length=350)
    aur_intro =  models.TextField(blank=True, max_length=450)

    gnome_layout_switcher_intro =  models.TextField(blank=True, max_length=350)
    manjaro_layout_intro =  models.TextField(blank=True, max_length=350)
    traditional_layout_intro =  models.TextField(blank=True, max_length=350)
    tilling_layout_intro =  models.TextField(blank=True, max_length=350)
    gnome_layout_intro =  models.TextField(blank=True, max_length=350)

    msm_intro =  models.TextField(blank=True, max_length=350)
    kernels_intro =  models.TextField(blank=True, max_length=350)
    common_settings_intro =  models.TextField(blank=True, max_length=350)
    graphic_drivers_intro =  models.TextField(blank=True, max_length=350)

    web_app_manager_intro =  models.TextField(blank=True, max_length=450)
    microsoft_office_intro =  models.TextField(blank=True, max_length=350)
    skype_intro =  models.TextField(blank=True, max_length=350)

    calamares_intro =  models.TextField(blank=True, max_length=450)    

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField("branches_intro"),
        index.SearchField("arch_linux_intro"),
        index.SearchField("unstable_intro"),
        index.SearchField("testing_intro"),
        index.SearchField("stable_intro"),
        index.SearchField("pamac_intro"),
        index.SearchField("package_formats_intro"),
        index.SearchField("updates_intro"),
        index.SearchField("aur_intro"),
        index.SearchField("gnome_layout_switcher_intro"),
        index.SearchField("manjaro_layout_intro"),
        index.SearchField("traditional_layout_intro"),
        index.SearchField("tilling_layout_intro"),
        index.SearchField("gnome_layout_intro"),
        index.SearchField("msm_intro"),
        index.SearchField("kernels_intro"),
        index.SearchField("common_settings_intro"),
        index.SearchField("graphic_drivers_intro"),
        index.SearchField("web_app_manager_intro"),
        index.SearchField("microsoft_office_intro"),
        index.SearchField("skype_intro"),
        index.SearchField("calamares_intro"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("branches_intro"),
        FieldPanel("arch_linux_intro"),
        FieldPanel("unstable_intro"),
        FieldPanel("testing_intro"),
        FieldPanel("stable_intro"),
        FieldPanel("pamac_intro"),
        FieldPanel("package_formats_intro"),
        FieldPanel("updates_intro"),
        FieldPanel("aur_intro"),
        FieldPanel("gnome_layout_switcher_intro"),
        FieldPanel("manjaro_layout_intro"),
        FieldPanel("traditional_layout_intro"),
        FieldPanel("tilling_layout_intro"),
        FieldPanel("gnome_layout_intro"),
        FieldPanel("msm_intro"),
        FieldPanel("kernels_intro"),
        FieldPanel("common_settings_intro"),
        FieldPanel("graphic_drivers_intro"),
        FieldPanel("web_app_manager_intro"),
        FieldPanel("microsoft_office_intro"),
        FieldPanel("skype_intro"),
        FieldPanel("calamares_intro"),
    ]

    keywords = models.CharField(default='', blank=True, max_length=150)

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


class Team(Page):
    max_count=1
    title = "Team"
    template = "home/team.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    intro =  models.TextField(blank=True, max_length=350)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
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
                imgs =["jaro-1.png", "jaro-3.png", "jaro-4.png"]
                avatar = f"/static/img/{random.choice(imgs)}"
            twitter = profile.user.twitter
            github = profile.user.github
            position = profile.user.position
            forum = profile.user.forum
            dict = {"position": position, "name": name, "forum": forum, "title": title, "description": description, "avatar": avatar, "twitter": twitter, "github": github}
            profiles.append(dict) 
           
        def get_position(profile):
            return profile.get('position')
            
        profiles.sort(key=get_position)
        context = super().get_context(request)
        context['users'] = profiles
        return context

    keywords = models.CharField(default='', blank=True, max_length=150)

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


class CustomPage(Page):
    template = "home/custom-page.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    intro =  models.TextField(default='', blank=True, max_length=450)

    content = StreamField(
        [
            ("richtext", blocks.RichtextBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("content"),
    ]
    

    keywords = models.CharField(default='', blank=True, max_length=150)

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


class PartnersSponsors(Page):
    max_count=2
    template = "home/partners-sponsors.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    
    content = StreamField(
        [
            ("partners", blocks.PartnerBlock()),     
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    intro =  models.TextField(default='', blank=True, max_length=350)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('content'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("content"),
    ]

    keywords = models.CharField(default='', blank=True, max_length=150)

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
    subpage_types = [
        'home.CustomPage',
        'home.PartnersSponsors',
        'home.Downloads',
        'home.Team',
        'home.Hardware',
        'home.Donations',
        'contact.ContactPage',
        'features',
        'home.UpdateStatus',
        'home.videos'
        ]
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
        use_json_field=True,
    )

    manjaro_title = models.CharField(default='', blank=True, max_length=50)
    manjaro_intro = models.TextField(blank=True, max_length=350)
    
    partners_title = models.CharField(default='', blank=True, max_length=50)
    partners_intro = models.TextField(blank=True, max_length=350)
    partners_url = models.URLField(blank=True)

    software_intro = models.TextField(blank=True, max_length=350)

    content_panels = Page.content_panels + [
        FieldPanel("manjaro_title"),
        FieldPanel("manjaro_intro"),
        FieldPanel("partners_title"),
        FieldPanel("partners_intro"),
        FieldPanel("partners_url"),
        FieldPanel("content"),
    ]

    affiliate = StreamField(
        [
            ("promotion", blocks.AffiliateBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    software = StreamField(
        [
            ("software", blocks.SoftwareBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    affiliate_panels = [
        FieldPanel("affiliate"),
    ]

    software_panels = [
        FieldPanel("software_intro"),
        FieldPanel("software"),
    ]

    keywords = models.CharField(default='', blank=True, max_length=100)

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=('Content')),
        ObjectList(affiliate_panels, heading=('Affiliate')),
        ObjectList(software_panels, heading=('Software')),
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
        from puput.models import EntryPage 
        context = super(HomePage, self).get_context(request)
        from wagtail.core.models import Page
        context['blog'] = EntryPage.objects.all().order_by('-date')[0:3]
        return context

    
class Videos(Page):
    template = "home/videos.html"
    subpage_types = []
    parent_page_types = [
        'home.HomePage'
    ]

    intro =  models.TextField(default='', blank=True, max_length=450)

    video_media = StreamField(
        [
            ("video", blocks.UrlBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('video_media'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("video_media"),
    ]
    

    keywords = models.CharField(default='', blank=True, max_length=150)

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