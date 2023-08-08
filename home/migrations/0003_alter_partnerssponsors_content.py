# Generated by Django 3.2.13 on 2022-04-18 07:32

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_partnerssponsors_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerssponsors',
            name='content',
            field=wagtail.fields.StreamField([('partners', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.blocks.TextBlock(help_text='Short Vendor Description', required=True)), ('avatar', wagtail.images.blocks.ImageChooserBlock(required=False))]))], blank=True, null=True),
        ),
    ]
