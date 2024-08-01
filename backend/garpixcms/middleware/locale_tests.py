import pytest
from django.test import RequestFactory, override_settings
from django.conf import settings
from django.utils import translation
from django.utils.translation import activate
from garpixcms.middleware.locale import GarpixLocaleMiddleware, is_language_prefix_patterns_used_for_url


@override_settings(ROOT_URLCONF='garpixcms.urls')
@pytest.mark.parametrize('path, expected_used, expected_prefix', [
    ('/en/about/', True, '/en/'),
    ('/about/', False, False),
    ('/fr/about/', True, '/fr/'),
    ('/about-us/', False, False),
])
def test_is_language_prefix_patterns_used_for_url(path, expected_used, expected_prefix):
    request = RequestFactory().get(path)
    middleware = GarpixLocaleMiddleware()
    used, prefix = is_language_prefix_patterns_used_for_url(settings.ROOT_URLCONF, request.path)
    assert used == expected_used
    assert prefix == expected_prefix


@pytest.mark.parametrize('path, expected_language_code', [
    ('/en/about/', 'en'),
    ('/about/', 'en'),
    ('/fr/about/', 'fr'),
    ('/about-us/', 'en'),
])
def test_garpix_locale_middleware_process_request(path, expected_language_code):
    request = RequestFactory().get(path)
    middleware = GarpixLocaleMiddleware()
    activate('en')
    middleware.process_request(request)
    assert request.LANGUAGE_CODE == expected_language_code
    assert translation.get_language() == expected_language_code
    assert translation.get_language_from_request(request) == expected_language_code

    activate(settings.LANGUAGE_CODE)
