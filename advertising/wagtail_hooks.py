from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import Advert


@register_snippet
class Ads(SnippetViewSet):
    model = Advert
    base_url_path = 'affiliates'
    menu_label = 'Affiliates' 
    icon = 'clipboard-list' 
    menu_order = 200  
    add_to_settings_menu = False  
    exclude_from_explorer = False 
    add_to_admin_menu = True 
    list_display = ('title', 'description')
    list_filter = ('description',)
    search_fields = ('title', 'description')



