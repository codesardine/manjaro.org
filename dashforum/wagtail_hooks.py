from django.urls import path, reverse
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from .views import certificates, index


@hooks.register('register_admin_urls')
def register_forum_url():
    return [
        path('forum/', index, name='forum'),
        path('certificates/', certificates, name='certificates'),
    ]

@hooks.register('register_admin_menu_item')
def register_forum_menu_item():
    return MenuItem('Forum', reverse('forum'), icon_name='date')

@hooks.register('register_admin_menu_item')
def register_certificate_menu_item():
    return MenuItem('Certificates', reverse('certificates'), icon_name='date')
