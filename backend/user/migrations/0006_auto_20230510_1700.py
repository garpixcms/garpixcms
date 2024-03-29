# Generated by Django 3.2 on 2023-05-10 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20230307_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmed_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date email was confirmed'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_confirmed_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date phone was confirmed'),
        ),
    ]
