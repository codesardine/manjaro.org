from django import template
import requests


register = template.Library()


@register.simple_tag()
def get_downloads():
        data_source = "https://gitlab.manjaro.org/webpage/iso-info/-/raw/master/file-info.json"
        response = requests.get(data_source)
        print(response.json())
        if response.ok:
            return response.json()