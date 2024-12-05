import pytest
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse
from django.test import RequestFactory, override_settings
from django.urls import Resolver404
from django.urls import path, clear_url_caches
from django.utils import translation

from garpixcms.middleware.locale import resolve_class, GarpixLocaleMiddleware



urlpatterns = [
    path('', lambda request: HttpResponse("Home page"), name='home'),
    path('about/', lambda request: HttpResponse("About page"), name='about'),
]

settings = {
    "LANGUAGE_CODE": 'en',
    "LANGUAGES": (('en', 'English'), ('fr', 'French')),
    "USE_I18N": True,
    "ROOT_URLCONF": __name__,
}


@pytest.fixture
def patch_urlpatterns(mocker, request):
    """
    Фикстура для патчинга `urlpatterns`.
    Умеет переключаться между обычными и i18n паттернами.
    """
    if request.param == "default":
        mocker.patch(
            'middleware.test_garpix_locale.urlpatterns',
            [
                path('', lambda request: HttpResponse("Home page"), name='home'),
                path('about/', lambda request: HttpResponse("About page"), name='about'),
            ]
        )
    elif request.param == "i18n":
        mocker.patch(
            'middleware.test_garpix_locale.urlpatterns',
            i18n_patterns(
                path('', lambda request: HttpResponse("Home page"), name='home'),
                path('about/', lambda request: HttpResponse("About page"), name='about'),
            )
        )
    else:
        raise ValueError(f"Unknown param: {request.param}")
    clear_url_caches()

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

# Пример тестов
@override_settings(**settings)
@pytest.mark.parametrize("patch_urlpatterns", ["default"], indirect=True)
def test_garpix_locale_middleware_without_language_prefix(patch_urlpatterns):
    """
    Тест для проверки обработки запроса без языкового префикса.
    """
    request_factory = RequestFactory()
    request = request_factory.get('/about/')
    middleware = GarpixLocaleMiddleware(get_response=lambda _: HttpResponse())

    # Обрабатываем запрос
    middleware.process_request(request)

    # Проверяем, что язык по умолчанию активирован
    assert request.LANGUAGE_CODE == 'en', f"Expected 'en' but got '{request.LANGUAGE_CODE}'"
    assert translation.get_language() == 'en', f"Expected 'en' but got '{translation.get_language()}'"


@override_settings(**settings)
@pytest.mark.parametrize("patch_urlpatterns", ["i18n"], indirect=True)
def test_garpix_locale_middleware_with_language_prefix(patch_urlpatterns):
    """
    Тест для проверки обработки запроса с языковым префиксом.
    """
    request_factory = RequestFactory()
    request = request_factory.get('/fr/about/')
    middleware = GarpixLocaleMiddleware(get_response=lambda _: HttpResponse())

    # Обрабатываем запрос
    middleware.process_request(request)

    # Проверяем, что язык `fr` активирован
    assert request.LANGUAGE_CODE == 'fr', f"Expected 'fr' but got '{request.LANGUAGE_CODE}'"
    assert translation.get_language() == 'fr', f"Expected 'fr' but got '{translation.get_language}'"


@override_settings(**settings)
@pytest.mark.parametrize("patch_urlpatterns", ["i18n"], indirect=True)
def test_garpix_locale_middleware_unsupported_language(patch_urlpatterns):
    """
    Тест для проверки обработки запроса с неподдерживаемым языковым префиксом.
    """
    request_factory = RequestFactory()
    request = request_factory.get('/es/about/')
    middleware = GarpixLocaleMiddleware(get_response=lambda _: HttpResponse())

    # Обрабатываем запрос
    middleware.process_request(request)

    # Проверяем, что язык по умолчанию `en` активирован
    assert request.LANGUAGE_CODE == 'en', f"Expected 'en' but got '{request.LANGUAGE_CODE}'"
    assert translation.get_language() == 'en', f"Expected 'en' but got '{translation.get_language}'"