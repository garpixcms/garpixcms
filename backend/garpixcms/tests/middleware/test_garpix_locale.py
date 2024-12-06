import pytest
from django.http import HttpResponse
from django.test import RequestFactory, override_settings
from django.urls import Resolver404
from django.urls import path
from django.utils import translation

from garpixcms.middleware.locale import resolve_class, GarpixLocaleMiddleware

urlpatterns = [
    path('', lambda request: HttpResponse("Home page"), name='home'),
    path('about/', lambda request: HttpResponse("About page"), name='about'),
]

test_settings = {
    "LANGUAGE_CODE": 'en',
    "LANGUAGES": (('en', 'English'), ('fr', 'French')),
    "USE_I18N": True,
    "ROOT_URLCONF": __name__,
}

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


@override_settings(**test_settings)
@pytest.mark.parametrize('path, expected_language_code', [
    ('/en/about/', 'en'),
    ('/about/', 'en'),
    ('/fr/about/', 'fr'),
    ('/nonexistent/', 'en'),
])
def test_garpix_locale_middleware_process_request(path, expected_language_code):
    request = RequestFactory().get(path)
    middleware = GarpixLocaleMiddleware(lambda request: HttpResponse())

    translation.activate(expected_language_code)

    middleware.process_request(request)

    assert translation.get_language() == expected_language_code, (
        f"Expected language '{expected_language_code}' but got '{translation.get_language()}' for path '{path}'"
    )
