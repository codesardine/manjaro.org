# Generated by Django 3.2.13 on 2022-05-06 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220423_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2),
        ),
    ]
