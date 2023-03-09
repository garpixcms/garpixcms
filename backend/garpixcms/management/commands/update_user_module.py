"""Команда для запуска 'python3 manage.py update_user_module'"""
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from garpix_menu.models import MenuItem


class Command(BaseCommand):
    help = "Команда для переезда с garpix_auth на garpix_user"

    @atomic
    def handle(self, *args, **options):
        from garpix_auth.models import AccessToken, RefreshToken
        from garpix_user.models import AccessToken as NewAccessToken, RefreshToken as NewRefreshToken

        access_tokens = AccessToken.objects.all()
        refresh_tokens = RefreshToken.objects.all()

        NewAccessToken.objects.bulk_create(access_tokens)
        NewRefreshToken.objects.bulk_create(refresh_tokens)

        self.stdout.write(self.style.SUCCESS('Done'))
