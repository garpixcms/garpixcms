# Generated by Django 3.1 on 2022-05-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_notify', '0006_auto_20220404_1158'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifyuserlistparticipant',
            options={'verbose_name': 'Дополнительный участник списка рассылки', 'verbose_name_plural': 'Дополнительные участники списка рассылки'},
        ),
        migrations.AddField(
            model_name='notify',
            name='users_list',
            field=models.ManyToManyField(blank=True, to='garpix_notify.NotifyUserList', verbose_name='Списки пользователей для рассылки'),
        ),
        migrations.AddField(
            model_name='notifyconfig',
            name='email_malling',
            field=models.IntegerField(choices=[(0, 'Обычная рассылка'), (1, 'Скрытая рассылка')], default=1, help_text='Если выбрана обычная рассылка, то пользователи будут видеть email друг друга', verbose_name='Тип массовой рассылки'),
        ),
        migrations.AlterField(
            model_name='notifyconfig',
            name='is_telegram_enabled',
            field=models.BooleanField(default=True, verbose_name='Разрешить отправку Telegram'),
        ),
        migrations.AlterField(
            model_name='notifyconfig',
            name='sms_url_type',
            field=models.IntegerField(choices=[(0, 'sms.ru'), (1, 'web.szk-info.ru'), (2, 'iqsms.ru'), (3, 'infosmska.ru'), (4, 'smsc.ru'), (5, 'sms-sending.ru'), (6, 'sms-prosto.ru')], default=0, verbose_name='URL СМС провайдера'),
        ),
        migrations.AlterField(
            model_name='notifytemplate',
            name='user_lists',
            field=models.ManyToManyField(blank=True, to='garpix_notify.NotifyUserList', verbose_name='Списки пользователей для рассылки'),
        ),
        migrations.AlterField(
            model_name='notifyuserlist',
            name='mail_to_all',
            field=models.BooleanField(default=False, verbose_name='Массовая рассылка для всех пользователей сайта'),
        ),
        migrations.AlterField(
            model_name='smtpaccount',
            name='host',
            field=models.CharField(default='smtp.yandex.com', max_length=255, verbose_name='Хост'),
        ),
        migrations.AlterField(
            model_name='smtpaccount',
            name='is_use_ssl',
            field=models.BooleanField(default=True, verbose_name='Использовать SSL?'),
        ),
        migrations.AlterField(
            model_name='smtpaccount',
            name='is_use_tls',
            field=models.BooleanField(default=False, verbose_name='Использовать TLS?'),
        ),
        migrations.AlterField(
            model_name='smtpaccount',
            name='port',
            field=models.IntegerField(default=465, verbose_name='Порт'),
        ),
    ]
