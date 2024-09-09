import pytest
from unittest.mock import patch, MagicMock
from django.conf import settings
from django.core.management import call_command
from django.db import IntegrityError


@pytest.fixture(autouse=True)
def add_apps_to_installed_apps(settings):
    if 'garpix_auth' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += ['garpix_auth']
    if 'garpix_user' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += ['garpix_user']

@pytest.fixture
def mock_old_access_tokens():
    MockOldAccessToken = MagicMock()
    MockOldAccessToken.objects.all.return_value = [
        MagicMock(token='old_access_token_1'),
        MagicMock(token='old_access_token_2'),
    ]
    return MockOldAccessToken

@pytest.fixture
def mock_new_access_tokens():
    MockNewAccessToken = MagicMock()
    MockNewAccessToken.objects.bulk_create = MagicMock(return_value=None)
    return MockNewAccessToken

@pytest.fixture
def mock_new_refresh_tokens():
    MockNewRefreshToken = MagicMock()
    MockNewRefreshToken.objects.bulk_create = MagicMock(return_value=None)
    return MockNewRefreshToken


@pytest.mark.django_db
def test_migrate_tokens_error(mock_old_access_tokens, mock_new_access_tokens, mock_new_refresh_tokens):
    # Настройте моки
    MockOldAccessToken = MagicMock()
    MockOldAccessToken.objects.all.return_value = [
        MagicMock(token='old_access_token_1'),
        MagicMock(token='old_access_token_2'),
    ]

    mock_new_access_tokens.objects.bulk_create.side_effect = IntegrityError("Integrity error")
    mock_new_refresh_tokens.objects.bulk_create.side_effect = IntegrityError("Integrity error")

    with patch('garpix_auth.models.AccessToken', MockOldAccessToken), \
            patch('garpix_auth.models.RefreshToken', MockOldAccessToken), \
            patch('garpix_user.models.AccessToken', mock_new_access_tokens), \
            patch('garpix_user.models.RefreshToken', mock_new_refresh_tokens):
        with pytest.raises(IntegrityError):
            call_command('update_user_module')

@pytest.mark.django_db
def test_migrate_tokens(mock_old_access_tokens, mock_new_access_tokens, mock_new_refresh_tokens):
    with patch('garpix_auth.models.AccessToken', mock_old_access_tokens), \
            patch('garpix_auth.models.RefreshToken', mock_old_access_tokens), \
            patch('garpix_user.models.AccessToken', mock_new_access_tokens), \
            patch('garpix_user.models.RefreshToken', mock_new_refresh_tokens):
        call_command('update_user_module')

        mock_new_access_tokens.objects.bulk_create.assert_called()
        mock_new_refresh_tokens.objects.bulk_create.assert_called()
