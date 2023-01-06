from django import template
register = template.Library()


@register.filter
def removedash(value):
    return value.replace("-", " ")

@register.filter
def random_list(list):
    import random
    return random.choice(list)

@register.filter
def clean_id(string):
    return string.replace(" ", "")

@register.filter
def sitemap_date(date):
    return date.strftime('%Y-%m-%d')
    
@register.filter
def url_exists(url):
    import requests
    ok = (301, 302, 200)
    try:
        response = requests.head(url, timeout=2.50)
        if response.status_code in ok:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

@register.filter
def is_doc(item):
    if item != None:
        if item == "40" or "docs." in item or "wiki." in item:
            return True
        return False