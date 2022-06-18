from django.db import models
from django.db.models import Q
from django.db import connection
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
import requests
import re
import enum
from collections import namedtuple


class Archs(enum.Enum):
    x86_64 = enum.auto()
    aarch64 = enum.auto()

class Branches(enum.Enum):
    stable = 0
    testing = 1
    unstable = 2


class x86_64Manager(models.Manager):
    """Force type x86_64"""

    def get_queryset(self):
        return super(x86_64Manager, self).get_queryset().filter(architecture=Archs.x86_64.value)

    def create(self, **kwargs):   # not work ?
        # print("     # aarch64Manager.get_queryset() force ", Archs.x86_64, Archs.x86_64.value)
        kwargs.update({'architecture': Archs.x86_64.value})
        return super(x86_64Manager, self).create(**kwargs)


class aarch64Manager(models.Manager):
    """Force type aarch64"""

    def get_queryset(self):
        return super(aarch64Manager, self).get_queryset().filter(architecture=Archs.aarch64.value)

    def create(self, **kwargs):    # not work ?
        # print("     # aarch64Manager.get_queryset() force ", Archs.x86_64, Archs.aarch64.value)
        kwargs.update({'architecture': Archs.aarch64.value})
        return super(aarch64Manager, self).create(**kwargs)


class PackageModel(models.Model):
    id = models.AutoField(primary_key=True)
    architecture = models.IntegerField(null=False)
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
        #abstract = True
        ordering = ("name", "repo")

    def __str__(self) -> str:
        ret = []
        ret.append(f'"architecture":"{Archs(self.architecture).name}", "repo":"{self.repo}", "name":"{self.name}"')
        ret.append(f'"stable":"{self.stable}", "testing":"{self.testing}", "unstable":"{self.unstable}"')
        ret.append(f'"last_modified":"{self.last_modified}", "packager":"{self.packager}", "arch":"{self.arch}"')
        ret.append(f'"id":"{self.id}"')
        return f'{{ {",".join(ret)} }}'

class x86_64(PackageModel):
    objects = x86_64Manager()

    class Meta:
        proxy = True


class aarch64(PackageModel):
    objects = aarch64Manager()

    class Meta:
        proxy = True


class lastModified(models.Model):
    id = models.AutoField(primary_key=True)
    arch = models.CharField(max_length=100, null=True)
    branch = models.CharField(max_length=100, null=True)
    repo = models.CharField(max_length=100, null=True)
    date = models.DateTimeField()
    status = models.TextField(default="")


class Packages(RoutablePageMixin, Page):
    regex = r"\[{*.?$^"
    max_count=1
    template = "packages.html"
    subpage_types = []
    parent_page_types = [
        'wagtailcore.Page'
    ]

    @route(r"^status/$")
    def status(self, request):
        last_modified = lastModified.objects.order_by("arch", "branch", "repo") 
        return self.render(
            request,
            template="status.html",
            context_overrides = {
                "status": last_modified
                }
        )

    @route(r"^status/repos/$")
    def status_repos(self, request):
        repport = RepportPackages()
        repport.request()
        return self.render(
            request,
            template="status_pkgs.html",
            context_overrides={
                "archs": (a for a in Archs),
                "repport": repport,
            }
        )

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
                    search_results = [match for match in all if match.tag == "error"]
                elif "manjaro" in search_query:
                    search_results = model.objects.filter(packager__contains='manjaro')

        else:
            search_results = model.objects.none()

        query_total = len(search_results) if isinstance(search_results, list) else search_results.count()
        context['total_packages'] = total_packages
        context['query'] = search_query

        if search_query is not None and \
           any(match in self.regex for match in search_query) \
           and query_total == 0:
            context['query'] = "your regex"

        context["search_query"] = search_query if search_query else ""
        context['packages'] = search_results
        context['query_total'] = query_total

        return context


class RepportPackages():
    _sql = '''SELECT architecture, repo,
            sum(CASE WHEN (stable) != "" THEN 1 ELSE 0 END)  as stables,
            sum(CASE WHEN (testing) != "" THEN 1 ELSE 0 END)  as testings,
            sum(CASE WHEN (unstable) != "" THEN 1 ELSE 0 END)  as unstables
            FROM compare_packagemodel
            GROUP BY repo, architecture
            order by architecture;'''

    def __init__(self) -> None:
        self.items = {}
        for arch in Archs:
            self.items[arch.name] = []

    def request(self):
        # self.items = PackageModel.objects.raw(self._sql) # no possible: want id field
        with connection.cursor() as cursor:
            cursor.execute(self._sql)
            desc = cursor.description
            obj = namedtuple('Result', [col[0] for col in desc])
            items = cursor.fetchall()
            for item in items:
                item = list(item)
                item[0] = Archs(item[0])
                self.items[Archs(item[0]).name].append(obj(*item))

    def get_total(self, arch: Archs):
        obj = namedtuple('Counts', [f"{b.name}s" for b in Branches])
        return obj(
            sum(n[2] for n in self.items[arch.name]),
            sum(n[3] for n in self.items[arch.name]),
            sum(n[4] for n in self.items[arch.name]),
        )
