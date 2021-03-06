# Generated by Django 3.1.14 on 2022-06-30 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_notify', '0008_auto_20220601_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifyconfig',
            name='telegram_allow_sending_without_reply',
            field=models.BooleanField(default=False, verbose_name='Разрешить, если сообщение должно быть отправлено, даже если ответное сообщение не найдено'),
        ),
        migrations.AddField(
            model_name='notifyconfig',
            name='telegram_disable_notification',
            field=models.BooleanField(default=False, verbose_name='Пользователи получат уведомление без звука'),
        ),
        migrations.AddField(
            model_name='notifyconfig',
            name='telegram_disable_web_page_preview',
            field=models.BooleanField(default=False, verbose_name='Отключает предварительный просмотр ссылок в сообщениях'),
        ),
        migrations.AddField(
            model_name='notifyconfig',
            name='telegram_parse_mode',
            field=models.CharField(blank=True, choices=[('', 'Без форматирования'), ('HTML', 'HTML'), ('Markdown', 'Markdown')], default='', max_length=100, verbose_name='Тип парсера телеграм сообщений'),
        ),
        migrations.AddField(
            model_name='notifyconfig',
            name='telegram_timeout',
            field=models.FloatField(blank=True, default=None, null=True, verbose_name='Тайм-аут чтения с сервера'),
        ),
        migrations.AlterField(
            model_name='notifyconfig',
            name='call_login',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Логин/Индетификатор сервиса оператора связи'),
        ),
        migrations.AlterField(
            model_name='notifyconfig',
            name='call_password',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Пароль/Секретный ключ оператора связи'),
        ),
        migrations.AlterField(
            model_name='notifyconfig',
            name='call_url_type',
            field=models.IntegerField(choices=[(0, 'sms.ru API'), (1, 'sms.ru LOGIN'), (2, 'smsc.ru'), (3, 'ucaller.ru')], default=0, verbose_name='URL звонка провайдера'),
        ),
    ]
