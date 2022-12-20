# Generated by Django 3.2.16 on 2022-12-20 11:29

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0006_alter_menuitem_submenu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='submenu',
            field=wagtail.fields.StreamField([('submenu_item', wagtail.blocks.StructBlock([('submenu_item', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(blank=True, max_length=50, null=True, required=True)), ('icon', wagtail.blocks.CharBlock(blank=True, max_length=150)), ('description', wagtail.blocks.CharBlock(blank=True, max_length=150)), ('url', wagtail.blocks.CharBlock(blank=True, max_length=500)), ('open_in_new_tab', wagtail.blocks.BooleanBlock(required=False))]))]))], blank=True, null=True, use_json_field=True),
        ),
    ]
