from django import template
from ..models import Menu
from wagtail.core.models import Site


register = template.Library()


@register.simple_tag()
def get_menu(slug):
    try:
        return Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        return Menu.objects.none()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # this is returning the wrong root page
    return Site.find_for_request(context["request"]).root_page