import pytest
from unittest.mock import patch, MagicMock
from django.http import HttpRequest, HttpResponse
from django.urls import path, include
from django.utils import translation
from django.conf import settings
from django.test import RequestFactory
from garpixcms.middleware.locale import resolve_class, is_language_prefix_patterns_used_for_url, GarpixLocaleMiddleware

urlpatterns = [
    path('en/', lambda request: HttpResponse(), name='en_home'),
    path('fr/', lambda request: HttpResponse(), name='fr_home'),
]


@pytest.fixture
def mock_get_resolver():
    mock_resolver = MagicMock()
    mock_resolver.url_patterns = urlpatterns
    mock_resolver.pattern.match.return_value = ('new_path', [], {})
    return mock_resolver


def test_resolve_class(mock_get_resolver):
    mock_pattern = MagicMock()
    mock_get_resolver.url_patterns = [mock_pattern]
    result = resolve_class(mock_get_resolver, '/en/some/path/')
    assert result == mock_pattern


def test_resolve_class_no_match(mock_get_resolver):
    mock_get_resolver.pattern.match.return_value = None
    result = resolve_class(mock_get_resolver, '/nonexistent/path/')
    assert result is None


@pytest.mark.parametrize('path, expected_language_code', [
    ('/en/about/', 'en'),
    ('/about/', 'en'),
    ('/fr/about/', 'fr'),
    ('/about-us/', 'en'),
])
@patch('django.utils.translation.get_language')
@patch('garpixcms.middleware.locale.GarpixLocaleMiddleware.process_request')
def test_garpix_locale_middleware_process_request(mock_process_request, mock_get_language, path,
                                                  expected_language_code):
    mock_get_language.return_value = expected_language_code
    request = RequestFactory().get(path)
    middleware = GarpixLocaleMiddleware(lambda request: HttpResponse())

    translation.activate(expected_language_code)

    middleware.process_request(request)

    assert translation.get_language() == expected_language_code, f"Expected {expected_language_code} but got {translation.get_language()} for path {path}"
