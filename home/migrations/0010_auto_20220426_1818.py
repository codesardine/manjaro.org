# Generated by Django 3.2.13 on 2022-04-26 18:18

import customblocks.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardware',
            name='content',
            field=wagtail.core.fields.StreamField([('product_details', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.core.blocks.CharBlock(help_text='Very Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('product_details', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('certified', wagtail.core.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('model', wagtail.core.blocks.CharBlock(max_length=40, required=True)), ('processor', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('memory', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('ports', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.core.blocks.TextBlock(max_length=250, required=False)), ('button_url', wagtail.core.blocks.URLBlock(required=True))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock()), ('product_details', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.core.blocks.CharBlock(help_text='Very Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('product_details', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('certified', wagtail.core.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('model', wagtail.core.blocks.CharBlock(max_length=40, required=True)), ('processor', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('memory', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('ports', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.core.blocks.TextBlock(max_length=250, required=False)), ('button_url', wagtail.core.blocks.URLBlock(required=True))])))]))], blank=True, null=True),
        ),
    ]
