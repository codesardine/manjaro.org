# Generated by Django 3.2.16 on 2022-12-13 12:00

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('home', '0037_auto_20221129_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', models.TextField(blank=True, default='', max_length=450)),
                ('_videos', wagtail.core.fields.StreamField([('video', wagtail.core.blocks.StructBlock([('video', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('hidden', wagtail.core.blocks.BooleanBlock(default=False, help_text='hide this video', required=False)), ('embed_code', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.TextBlock(required=True))]))]))], blank=True, null=True)),
                ('keywords', models.CharField(blank=True, default='', max_length=150)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
