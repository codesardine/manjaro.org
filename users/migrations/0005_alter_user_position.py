# Generated by Django 3.2.13 on 2022-05-06 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2),
        ),
    ]
