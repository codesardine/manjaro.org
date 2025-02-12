# Generated by Django 3.2.16 on 2022-12-17 15:18

import customblocks.blocks
from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0039_auto_20221213_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompage',
            name='content',
            field=wagtail.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock())], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='donations',
            name='content',
            field=wagtail.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock())], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='content',
            field=wagtail.fields.StreamField([('product_details', wagtail.blocks.StructBlock([('product_details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('certified', wagtail.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified', required=False)), ('hidden', wagtail.blocks.BooleanBlock(help_text='hide this product', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='images must be 500x375 with space around the space determinates the image size', required=True)), ('model', wagtail.blocks.CharBlock(max_length=100, required=True)), ('processor', wagtail.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.blocks.CharBlock(max_length=100, required=False)), ('memory', wagtail.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.blocks.TextBlock(max_length=650, required=False)), ('button_url', wagtail.blocks.URLBlock(required=True))])))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='reviews',
            field=wagtail.fields.StreamField([('reviews', wagtail.blocks.StructBlock([('video', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('date', wagtail.blocks.DateBlock(required=False)), ('hidden', wagtail.blocks.BooleanBlock(default=False, help_text='hide this video', required=False)), ('embed_code', wagtail.blocks.CharBlock(required=True)), ('description', wagtail.blocks.TextBlock(required=True))]))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='affiliate',
            field=wagtail.fields.StreamField([('promotion', wagtail.blocks.StructBlock([('promotion', wagtail.blocks.StructBlock([('hidden', wagtail.blocks.BooleanBlock(help_text='hide this promotion', required=False)), ('model', wagtail.blocks.CharBlock(required=True)), ('url', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Vendor Image', required=True)), ('description', wagtail.blocks.TextBlock())]))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock()), ('product_details', wagtail.blocks.StructBlock([('product_details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('certified', wagtail.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified', required=False)), ('hidden', wagtail.blocks.BooleanBlock(help_text='hide this product', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='images must be 500x375 with space around the space determinates the image size', required=True)), ('model', wagtail.blocks.CharBlock(max_length=100, required=True)), ('processor', wagtail.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.blocks.CharBlock(max_length=100, required=False)), ('memory', wagtail.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.blocks.TextBlock(max_length=650, required=False)), ('button_url', wagtail.blocks.URLBlock(required=True))])))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='software',
            field=wagtail.fields.StreamField([('software', wagtail.blocks.StructBlock([('software', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('hidden', wagtail.blocks.BooleanBlock(default=False, help_text='hide this promotion', required=False)), ('url', wagtail.blocks.URLBlock(required=True)), ('description', wagtail.blocks.TextBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))]))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='partnerssponsors',
            name='content',
            field=wagtail.fields.StreamField([('partners', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(required=False)), ('description', wagtail.blocks.TextBlock(help_text='Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=False))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='videos',
            name='video_media',
            field=wagtail.fields.StreamField([('video', wagtail.blocks.StructBlock([('video', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('date', wagtail.blocks.DateBlock(required=False)), ('hidden', wagtail.blocks.BooleanBlock(default=False, help_text='hide this video', required=False)), ('embed_code', wagtail.blocks.CharBlock(required=True)), ('description', wagtail.blocks.TextBlock(required=True))]))]))], blank=True, null=True, use_json_field=True),
        ),
    ]
