# Generated by Django 3.2.12 on 2022-03-23 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0011_menu_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
