# Generated by Django 3.2.18 on 2023-04-06 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_auto_20221217_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactpage',
            name='intro',
        ),
    ]
