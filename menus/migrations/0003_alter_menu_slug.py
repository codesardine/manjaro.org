# Generated by Django 3.2.12 on 2022-03-22 16:58

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_auto_20220322_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name'),
        ),
    ]
