# Generated by Django 3.2.12 on 2022-03-22 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_alter_menu_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='title',
        ),
    ]
