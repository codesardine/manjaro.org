from django import template


register = template.Library()


@register.filter
def removedash(value):
    return value.replace("-", " ")
