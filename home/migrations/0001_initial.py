# Generated by Django 3.2.12 on 2022-04-15 15:08

import customblocks.blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailimages', '0023_add_choose_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', models.TextField(blank=True, default='', max_length=150)),
                ('content', wagtail.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock())], blank=True, null=True)),
                ('keywords', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', models.CharField(max_length=250, null=True)),
                ('content', wagtail.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock())], blank=True, null=True)),
                ('keywords', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', models.CharField(max_length=250, null=True)),
                ('content', wagtail.fields.StreamField([('product_details', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.blocks.CharBlock(help_text='Very Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('product_details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('model', wagtail.blocks.CharBlock(max_length=40, required=True)), ('processor', wagtail.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.blocks.CharBlock(max_length=100, required=True)), ('memory', wagtail.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.blocks.CharBlock(max_length=100, required=True)), ('ports', wagtail.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.blocks.TextBlock(max_length=250, required=False)), ('button_url', wagtail.blocks.URLBlock(required=True))])))]))], blank=True, null=True)),
                ('keywords', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.fields.StreamField([('richtext', customblocks.blocks.RichtextBlock()), ('product_details', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.blocks.CharBlock(help_text='Very Short Vendor Description', required=True)), ('vendor_logo', wagtail.images.blocks.ImageChooserBlock(required=True)), ('product_details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('model', wagtail.blocks.CharBlock(max_length=40, required=True)), ('processor', wagtail.blocks.CharBlock(max_length=100, required=True)), ('screen', wagtail.blocks.CharBlock(max_length=100, required=True)), ('memory', wagtail.blocks.CharBlock(max_length=100, required=True)), ('storage', wagtail.blocks.CharBlock(max_length=100, required=True)), ('ports', wagtail.blocks.CharBlock(max_length=100, required=True)), ('graphics', wagtail.blocks.CharBlock(max_length=100, required=False)), ('description', wagtail.blocks.TextBlock(max_length=250, required=False)), ('button_url', wagtail.blocks.URLBlock(required=True))])))]))], blank=True, null=True)),
                ('manjaro_title', models.CharField(blank=True, default='', max_length=50)),
                ('manjaro_intro', models.CharField(blank=True, default='', max_length=200)),
                ('partners_title', models.CharField(blank=True, default='', max_length=50)),
                ('partners_intro', models.CharField(blank=True, default='', max_length=200)),
                ('partners_url', models.URLField(blank=True)),
                ('shells_title', models.CharField(blank=True, default='', max_length=50)),
                ('shells_intro', models.CharField(blank=True, default='', max_length=200)),
                ('keywords', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PartnersSponsors',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.fields.StreamField([('partners', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Vendor', required=True)), ('description', wagtail.blocks.TextBlock(help_text='Short Vendor Description', required=True)), ('details', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True))])))]))], blank=True, null=True)),
                ('intro', models.TextField(blank=True, default='', max_length=150)),
                ('keywords', models.CharField(blank=True, default='', max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', models.TextField(blank=True, default='', max_length=150)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Downloads',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', models.CharField(blank=True, default='', max_length=50)),
                ('question_one', models.CharField(blank=True, default='', max_length=50)),
                ('answer_one', models.TextField(blank=True, default='', max_length=200)),
                ('question_two', models.CharField(blank=True, default='', max_length=50)),
                ('answer_two', models.TextField(blank=True, default='', max_length=200)),
                ('question_three', models.CharField(blank=True, default='', max_length=50)),
                ('answer_three', models.TextField(blank=True, default='', max_length=200)),
                ('team_spins_intro', models.TextField(blank=True, default='', max_length=200)),
                ('community_spins_intro', models.TextField(blank=True, default='', max_length=200)),
                ('arm_spins_intro', models.TextField(blank=True, default='', max_length=200)),
                ('manual_intro', models.TextField(blank=True, default='', max_length=200)),
                ('docker_intro', models.TextField(blank=True, default='', max_length=200)),
                ('xfce_description', models.TextField(blank=True, default='', max_length=150)),
                ('xfce_notes', models.TextField(blank=True, default='', max_length=200)),
                ('plasma_description', models.TextField(blank=True, default='', max_length=150)),
                ('plasma_notes', models.TextField(blank=True, default='', max_length=200)),
                ('gnome_description', models.TextField(blank=True, default='', max_length=150)),
                ('gnome_notes', models.TextField(blank=True, default='', max_length=200)),
                ('cinnamon_description', models.TextField(blank=True, default='', max_length=150)),
                ('cinnamon_notes', models.TextField(blank=True, default='', max_length=200)),
                ('i3_description', models.TextField(blank=True, default='', max_length=150)),
                ('i3_notes', models.TextField(blank=True, default='', max_length=200)),
                ('budgie_description', models.TextField(blank=True, default='', max_length=150)),
                ('budgie_notes', models.TextField(blank=True, default='', max_length=200)),
                ('mate_description', models.TextField(blank=True, default='', max_length=150)),
                ('mate_notes', models.TextField(blank=True, default='', max_length=200)),
                ('sway_description', models.TextField(blank=True, default='', max_length=150)),
                ('sway_notes', models.TextField(blank=True, default='', max_length=200)),
                ('keywords', models.CharField(blank=True, default='', max_length=100)),
                ('budgie_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('cinnamon_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('gnome_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('i3_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('mate_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('plasma_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('sway_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('xfce_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
