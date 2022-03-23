# Generated by Django 3.2.12 on 2022-03-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0012_alter_menu_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='slug',
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
