# Generated by Django 3.1 on 2022-05-13 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0003_auto_20220412_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='basecomponent',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Включено'),
        ),
    ]
