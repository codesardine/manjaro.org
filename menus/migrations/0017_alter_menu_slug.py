# Generated by Django 3.2.12 on 2022-03-23 11:22

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0016_auto_20220323_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name'),
        ),
    ]
