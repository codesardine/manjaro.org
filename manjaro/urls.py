from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from puput import urls as puput_urls 
from compare.views import pkgs_update_status_json
from wagtail.contrib.sitemaps.views import sitemap
from search import views as search_views
from compare.views import pkgs_json, mesa_json
from home.views import merch
from advertising.views import ads_json


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('status.json', pkgs_update_status_json),
    #path('packages.json', pkgs_json),
    path('mesa.json', mesa_json),
    path('ads.json', ads_json),
    re_path(r"^search/$", search_views.search, name="search"), 
    path('merchandise/', merch, name="Merchandise"),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    try:
        urlpatterns += path("__reload__/", include("django_browser_reload.urls")),
    except ModuleNotFoundError as e:
        print(e)
    
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),

urlpatterns = urlpatterns + [
    path(r'',include(puput_urls)),
    path("", include(wagtail_urls)),
    path('sitemap.xml', sitemap),

]
