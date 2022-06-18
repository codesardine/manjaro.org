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

@register.filter
def format_branch(value):
    return value.replace("arm-", "")

@register.filter
def format_status(status):
    if any(char.isdigit() for char in status):
        return status
    else:
        return "unkown"