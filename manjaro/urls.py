from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from puput import urls as puput_urls 
from search import views as search_views
from wagtail.contrib.sitemaps.views import sitemap

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),
    path(r'', include('puput.urls')),
] 

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    
    urlpatterns += path("__reload__/", include("django_browser_reload.urls")),
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path('sitemap.xml', sitemap),
    path(r'',include(puput_urls)),
    path("", include(wagtail_urls)),
]
