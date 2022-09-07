# Generated by Django 3.2.14 on 2022-09-07 12:06

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_alter_downloads_intro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='shells_intro',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='shells_title',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='shells_url',
        ),
        migrations.AddField(
            model_name='homepage',
            name='software',
            field=wagtail.core.fields.StreamField([('software', wagtail.core.blocks.StructBlock([('software', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('hidden', wagtail.core.blocks.BooleanBlock(default=False, help_text='hide this promotion', required=False)), ('url', wagtail.core.blocks.URLBlock(required=True)), ('description', wagtail.core.blocks.TextBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))]))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='software_intro',
            field=models.TextField(blank=True, max_length=350),
        ),
    ]
