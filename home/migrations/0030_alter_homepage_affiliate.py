# Generated by Django 3.2.14 on 2022-08-29 10:06

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_updatestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='affiliate',
            field=wagtail.core.fields.StreamField([('promotion', wagtail.core.blocks.StructBlock([('promotion', wagtail.core.blocks.StructBlock([('hidden', wagtail.core.blocks.BooleanBlock(help_text='hide this promotion', required=False)), ('text', wagtail.core.blocks.CharBlock(required=True)), ('url', wagtail.core.blocks.URLBlock(required=True)), ('background', wagtail.images.blocks.ImageChooserBlock(help_text='Vendor Background Image', required=True))]))]))], blank=True, null=True),
        ),
    ]
