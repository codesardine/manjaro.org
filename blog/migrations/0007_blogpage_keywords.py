# Generated by Django 3.2.12 on 2022-03-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_body_blogpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='keywords',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
