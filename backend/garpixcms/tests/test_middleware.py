import pytest
from django.http import HttpResponse
from django.urls import Resolver404
from django.urls import path

from garpixcms.middleware.locale import resolve_class

urlpatterns = [
    path('en/', lambda request: HttpResponse(), name='en_home'),
    path('fr/', lambda request: HttpResponse(), name='fr_home'),
]


@pytest.fixture
def mock_get_resolver(mocker):
    mock_resolver = mocker.MagicMock()
    mock_resolver.url_patterns = []
    mock_resolver.pattern.match.return_value = None
    mock_resolver.default_kwargs = {}
    return mock_resolver


def test_resolve_class_success(mock_get_resolver, mocker):
    mock_pattern = mocker.MagicMock()
    mock_sub_match = mocker.MagicMock()
    mock_sub_match.kwargs = {'key': 'value'}
    mock_sub_match.tried = []

    mock_get_resolver.pattern.match.return_value = ('new_path', [], {})
    mock_get_resolver.url_patterns = [mock_pattern]
    mock_pattern.resolve.return_value = mock_sub_match

    result = resolve_class(mock_get_resolver, '/en/some/path/')

    assert result == mock_pattern
    mock_pattern.resolve.assert_called_once_with('new_path')
    mock_get_resolver._extend_tried.assert_called_once()


def test_resolve_class_no_match(mock_get_resolver):
    mock_get_resolver.pattern.match.return_value = None

    result = resolve_class(mock_get_resolver, '/nonexistent/path/')

    assert result is None


def test_resolve_class_with_resolver404(mock_get_resolver, mocker):
    mock_pattern = mocker.MagicMock()
    mock_get_resolver.pattern.match.return_value = ('new_path', [], {})
    mock_get_resolver.url_patterns = [mock_pattern]

    mock_pattern.resolve.side_effect = Resolver404({'tried': []})

    result = resolve_class(mock_get_resolver, '/en/some/path/')

    assert result is None
    mock_get_resolver._extend_tried.assert_called_once()


def test_resolve_class_updates_kwargs(mock_get_resolver, mocker):
    mock_pattern = mocker.MagicMock()
    mock_sub_match = mocker.MagicMock()
    mock_sub_match.kwargs = {'additional_key': 'additional_value'}
    mock_sub_match.tried = []

    mock_get_resolver.pattern.match.return_value = ('new_path', [], {'existing_key': 'existing_value'})
    mock_get_resolver.url_patterns = [mock_pattern]
    mock_pattern.resolve.return_value = mock_sub_match

    result = resolve_class(mock_get_resolver, '/en/some/path/')

    assert result == mock_pattern
    mock_pattern.resolve.assert_called_once_with('new_path')
    mock_get_resolver._extend_tried.assert_called_once()
