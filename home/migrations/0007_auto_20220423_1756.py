# Generated by Django 3.2.13 on 2022-04-23 17:56

import customblocks.blocks
from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_rename_promotion_link_homepage_promotion_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardware',
            name='content',
            field=wagtail.core.fields.StreamField([('product_details', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.core.blocks.CharBlock(help_text='Very Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('product_details', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('model', wagtail.core.blocks.CharBlock(max_length=40, required=True)), ('processor', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('memory', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('ports', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.core.blocks.TextBlock(max_length=250, required=False)), ('button_url', wagtail.core.blocks.URLBlock(required=True)), ('certified', wagtail.core.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified'))])))]))], blank=True, null=True),
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
            field=wagtail.core.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock()), ('product_details', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.core.blocks.CharBlock(help_text='Very Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('product_details', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('model', wagtail.core.blocks.CharBlock(max_length=40, required=True)), ('processor', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('memory', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('ports', wagtail.core.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.core.blocks.TextBlock(max_length=250, required=False)), ('button_url', wagtail.core.blocks.URLBlock(required=True)), ('certified', wagtail.core.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified'))])))]))], blank=True, null=True),
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
