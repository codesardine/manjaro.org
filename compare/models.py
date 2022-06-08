from tokenize import group
from django.db import models
from wagtail.core.models import Page
from wagtail.search.models import Query
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel


class Package(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    arch = models.CharField(max_length=50, null=True)
    branch = models.CharField(max_length=50, null=True)
    repo = models.CharField(max_length=20, null=True)
    stable = models.CharField(max_length=50, null=True)
    testing = models.CharField(max_length=50, null=True)
    unstable = models.CharField(max_length=50, null=True)
    last_update = models.CharField(max_length=20, null=True)
    group = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=120, null=True)
    packager = models.CharField(max_length=100, null=True)
    builddate = models.DateField(null=True)


class armPackage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    arch = models.CharField(max_length=50, null=True)
    branch = models.CharField(max_length=50, null=True)
    repo = models.CharField(max_length=20, null=True)
    stable = models.CharField(max_length=50, null=True)
    testing = models.CharField(max_length=50, null=True)
    unstable = models.CharField(max_length=50, null=True)
    last_update = models.CharField(max_length=20, null=True)
    group = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=120, null=True)
    packager = models.CharField(max_length=100, null=True)
    builddate = models.DateField(null=True)


class Updates(models.Model):
    id = models.AutoField(primary_key=True)
    arch = models.CharField(max_length=100, null=True)
    branch = models.CharField(max_length=100, null=True)
    repo = models.CharField(max_length=100, null=True)
    last_update = models.DateTimeField(max_length=100, default="")


class Packages(Page):
    max_count=1
    template = "packages.html"
    subpage_types = []
    parent_page_types = [
        'wagtailcore.Page'
    ]

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
    
    def get_context(self, request):
        context = super().get_context(request)
        search_query = request.GET.get('query', None)
        arm = request.GET.get('arm', None)
        if arm:
            model = armPackage
            context['arm_query'] = True
        else:
            model = Package
        
        all = model.objects.all()
        total_packages = len(all)
        if search_query:            
            search_results = model.objects.filter(name__contains=search_query)
            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()

            if search_query == "all":
                search_results = all
        else:
            search_results = model.objects.none()

        context['total_packages'] = total_packages
        context['query'] = search_query
        context['query_total'] = len(search_results)
        context['packages'] = search_results
        return context   
    
