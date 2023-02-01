# Generated by Django 3.2.16 on 2023-02-01 17:47

import customblocks.blocks
from django.db import migrations, models
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_auto_20221217_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompage',
            name='intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='budgie_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='cinnamon_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='community_intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='docker_intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='gnome_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='i3_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='manjaro_arm_team_intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='manjaro_team_intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='mate_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='minimal_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='phosh_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='plasma_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='plasma_mobile_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='sway_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='downloads',
            name='xfce_description',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='arch_linux_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='aur_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='branches_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='calamares_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='common_settings_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='gnome_layout_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='gnome_layout_switcher_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='graphic_drivers_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='kernels_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='manjaro_layout_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='microsoft_office_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='msm_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='package_formats_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='pamac_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='skype_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='stable_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='testing_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='tilling_layout_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='traditional_layout_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='unstable_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='updates_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='features',
            name='web_app_manager_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='content',
            field=wagtail.fields.StreamField([('product_details', wagtail.blocks.StructBlock([('product_details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('certified', wagtail.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified', required=False)), ('hidden', wagtail.blocks.BooleanBlock(help_text='hide this product', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='images must be 500x375 with space around the space determinates the image size', required=True)), ('model', wagtail.blocks.CharBlock(max_length=100, required=True)), ('processor', wagtail.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.blocks.CharBlock(max_length=100, required=False)), ('memory', wagtail.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.blocks.TextBlock(max_length=1000, required=False)), ('button_url', wagtail.blocks.URLBlock(required=True))])))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='intro',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock()), ('product_details', wagtail.blocks.StructBlock([('product_details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('certified', wagtail.blocks.BooleanBlock(help_text='if the hardware is Manjaro certified', required=False)), ('hidden', wagtail.blocks.BooleanBlock(help_text='hide this product', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='images must be 500x375 with space around the space determinates the image size', required=True)), ('model', wagtail.blocks.CharBlock(max_length=100, required=True)), ('processor', wagtail.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.blocks.CharBlock(max_length=100, required=False)), ('memory', wagtail.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.blocks.TextBlock(max_length=1000, required=False)), ('button_url', wagtail.blocks.URLBlock(required=True))])))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='keywords',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='manjaro_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='manjaro_title',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='partners_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='partners_title',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='software_intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='partnerssponsors',
            name='intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='team',
            name='intro',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='updatestatus',
            name='intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='videos',
            name='intro',
            field=models.TextField(blank=True, default='', max_length=1000),
        ),
    ]
