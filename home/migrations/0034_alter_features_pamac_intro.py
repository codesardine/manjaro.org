# Generated by Django 3.2.14 on 2022-09-20 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_hardware_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='features',
            name='pamac_intro',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
