from django.db import models
from django.db.models import Q
from wagtail.core.models import Page
from wagtail.search.models import Query
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel
import re

class PackageAbstract(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    arch = models.CharField(max_length=50, null=True)
    repo = models.CharField(max_length=20, null=True)
    stable = models.CharField(max_length=50, null=True)
    testing = models.CharField(max_length=50, null=True)
    unstable = models.CharField(max_length=50, null=True)
    last_modified = models.CharField(max_length=20, null=True)
    group = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=120, null=True)
    packager = models.CharField(max_length=100, null=True)
    builddate = models.DateField(null=True)

    @property
    def tag(self):
        status = ""
        if not self.testing and self.stable and self.unstable or \
           not self.stable and not self.unstable and self.testing:
            status = "error"
        elif not self.stable:
            status = "new"
        elif not self.unstable:
            status = "eol"
        return status
    class Meta:
        abstract = True
        ordering = ("name", "repo")

class x86_64(PackageAbstract):
    pass

class aarch64(PackageAbstract):
    pass


class lastModified(models.Model):
    id = models.AutoField(primary_key=True)
    arch = models.CharField(max_length=100, null=True)
    branch = models.CharField(max_length=100, null=True)
    repo = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()
    status = models.TextField(default="")


class Packages(Page):
    regex = r"\[{*.?$^"
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

    def get_request(self, model, search_query):
        """
            set orm request
            search_query in name OR search_query == group
        """
        try:
            re.compile(search_query)        
        except re.error:
            return model.none()
        
        if any(match in self.regex for match in search_query):
            return model.filter(name__iregex=search_query)
        return model.filter(
            Q(name__contains=search_query) | Q(group__exact=search_query)
        )

    def get_context(self, request):
        context = super().get_context(request)
        search_query = request.GET.get('query', None)
        arm = request.GET.get('arm', None)
        model = x86_64
        if arm:
            model = aarch64
            context['arm_query'] = True

        all = model.objects.all()
        total_packages = all.count()
        if search_query:
            search_query = search_query.lower()
            search_results = self.get_request(all, search_query)
            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()

            if search_query.startswith("#"):
                # filter commands
                if "all" in search_query:
                    search_results = all
                elif "kernels" in search_query:
                    pattern = r"linux([0-9].{1,3})(?!.)"
                    if arm:
                        pattern = r"^linux-([a-z0-9]{1,9}(?!.))"
                    search_results = model.objects.filter(name__iregex=pattern)
                elif "new" in search_query:
                    search_results = model.objects.filter(stable__exact='')
                elif "eol" in search_query:
                    search_results = model.objects.filter(unstable__exact='')
                elif "error" in search_query:
                    search_results = model.objects.filter(testing__exact='').exclude(unstable__exact='')
                elif "manjaro" in search_query:
                    search_results = model.objects.filter(packager__contains='manjaro')

        else:
            search_results = model.none()

        query_total = search_results.count()
        context['total_packages'] = total_packages
        context['query'] = search_query
        if any(match in self.regex for match in search_query) and query_total == 0:
            context['query'] = "your regex"

        context["search_query"] = search_query if search_query else ""
        context['packages'] = search_results
        context['query_total'] = query_total
        return context
