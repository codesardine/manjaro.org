# Generated by Django 3.2.13 on 2022-06-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_partnerssponsors_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='shells_url',
            field=models.URLField(blank=True),
        ),
    ]
