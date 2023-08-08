# Generated by Django 3.2.13 on 2022-04-23 17:56

import customblocks.blocks
from django.db import migrations, models
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_rename_promotion_link_homepage_promotion_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardware',
            name='content',
            field=wagtail.fields.StreamField([('product_details', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.blocks.CharBlock(help_text='Very Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('product_details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('model', wagtail.blocks.CharBlock(max_length=40, required=True)), ('processor', wagtail.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.blocks.CharBlock(max_length=100, required=True)), ('memory', wagtail.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.blocks.CharBlock(max_length=100, required=True)), ('ports', wagtail.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.blocks.TextBlock(max_length=250, required=False)), ('button_url', wagtail.blocks.URLBlock(required=True)), ('certified', wagtail.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified'))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='intro',
            field=models.TextField(max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='keywords',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock()), ('product_details', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.blocks.CharBlock(help_text='Very Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('product_details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('model', wagtail.blocks.CharBlock(max_length=40, required=True)), ('processor', wagtail.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.blocks.CharBlock(max_length=100, required=True)), ('memory', wagtail.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.blocks.CharBlock(max_length=100, required=True)), ('ports', wagtail.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.blocks.TextBlock(max_length=250, required=False)), ('button_url', wagtail.blocks.URLBlock(required=True)), ('certified', wagtail.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified'))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='manjaro_intro',
            field=models.TextField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='partners_intro',
            field=models.TextField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='shells_intro',
            field=models.TextField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name='partnerssponsors',
            name='intro',
            field=models.TextField(blank=True, default='', max_length=350),
        ),
        migrations.AlterField(
            model_name='partnerssponsors',
            name='keywords',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='team',
            name='intro',
            field=models.TextField(blank=True, default='', max_length=350),
        ),
    ]
