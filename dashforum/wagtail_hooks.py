from django.urls import path, reverse
from wagtail.admin.menu import MenuItem
from wagtail import hooks
from .views import certificates


@hooks.register('register_admin_urls')
def register_cert_url():
    return [
        path('certificates/', certificates, name='certificates'),
    ]

@hooks.register('register_admin_menu_item')
def register_certificate_menu_item():
    return MenuItem('Certificates', reverse('certificates'), icon_name='date')
