import pytest
from django.core.management import call_command
from garpix_auth.models import AccessToken as OldAccessToken, RefreshToken as OldRefreshToken
from garpix_user.models import AccessToken as NewAccessToken, RefreshToken as NewRefreshToken


@pytest.fixture
def old_access_tokens(db):
    return OldAccessToken.objects.bulk_create([
        OldAccessToken(token='old_access_token_1'),
        OldAccessToken(token='old_access_token_2'),
    ])


@pytest.fixture
def old_refresh_tokens(db):
    return OldRefreshToken.objects.bulk_create([
        OldRefreshToken(token='old_refresh_token_1'),
        OldRefreshToken(token='old_refresh_token_2'),
    ])


@pytest.mark.django_db
def test_migrate_tokens(old_access_tokens, old_refresh_tokens, capsys):
    assert NewAccessToken.objects.count() == 0
    assert NewRefreshToken.objects.count() == 0

    call_command('migrate_tokens')

    captured = capsys.readouterr()

    assert 'Done' in captured.out

    assert NewAccessToken.objects.count() == len(old_access_tokens)
    assert NewRefreshToken.objects.count() == len(old_refresh_tokens)

    for old_token in old_access_tokens:
        assert NewAccessToken.objects.filter(token=old_token.token).exists()

    for old_token in old_refresh_tokens:
        assert NewRefreshToken.objects.filter(token=old_token.token).exists()
