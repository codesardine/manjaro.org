from wagtail.core.models import Site
from django import template
import random

register = template.Library()


@register.filter
def removedash(value):
    return value.replace("-", " ")

@register.filter
def random_list(list):
    return random.choice(list)

@register.filter
def clean_id(string):
    return string.replace(" ", "")

@register.simple_tag(takes_context=True)
def menu(context):    
    homepage = Site.objects.filter(is_default_site=True).first().root_page
    context['menuitems'] = homepage.get_children().live().in_menu()
    return ""
