# Generated by Django 3.2.16 on 2022-12-13 12:16

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_videos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videos',
            name='_videos',
        ),
        migrations.AddField(
            model_name='videos',
            name='video_media',
            field=wagtail.core.fields.StreamField([('video', wagtail.core.blocks.StructBlock([('video', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('date', wagtail.core.blocks.DateBlock(required=False)), ('hidden', wagtail.core.blocks.BooleanBlock(default=False, help_text='hide this video', required=False)), ('embed_code', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.TextBlock(required=True))]))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='reviews',
            field=wagtail.core.fields.StreamField([('reviews', wagtail.core.blocks.StructBlock([('video', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('date', wagtail.core.blocks.DateBlock(required=False)), ('hidden', wagtail.core.blocks.BooleanBlock(default=False, help_text='hide this video', required=False)), ('embed_code', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.TextBlock(required=True))]))]))], blank=True, null=True),
        ),
    ]
