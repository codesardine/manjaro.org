from django import template
from datetime import date
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
def date_today(str):
    return date.today().strftime('%Y-%m-%d')
    
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
def remove_protocol(url):
    return url.replace("http://", "").replace("https://", "")