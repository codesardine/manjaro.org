from django import template

register = template.Library()

@register.filter
def to_string(category):
    return str(category)
    
@register.filter
def is_internal(category):
    if str(category) == "internal":
        return True
