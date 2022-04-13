# Generated by Django 3.2.12 on 2022-04-13 11:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('home', '0048_remove_downloads_description'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Partners',
            new_name='PartnersSponsors',
        ),
    ]
