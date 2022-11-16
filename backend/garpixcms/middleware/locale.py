import functools

from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.urls import get_resolver, LocalePrefixPattern
from django.utils import translation


@functools.lru_cache(maxsize=None)
def is_language_prefix_patterns_used_for_url(urlconf, path):
    """
    Return a tuple of two booleans: (
        `True` if i18n_patterns() (LocalePrefixPattern) is used in the URLconf for the matching pattern
        `True` if the default language should be prefixed
    )
    """
    for url_pattern in get_resolver(urlconf).url_patterns:
        if url_pattern.pattern.match(path):
            if isinstance(url_pattern.pattern, LocalePrefixPattern):
                return True, url_pattern.pattern.prefix_default_language
            break
    return False, False


class GarpixLocaleMiddleware(LocaleMiddleware):

    def process_request(self, request):
        urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)

        i18n_patterns_used, prefixed_default_language = is_language_prefix_patterns_used_for_url(urlconf, request.path)
        language = translation.get_language_from_request(request, check_path=i18n_patterns_used)
        language_from_path = translation.get_language_from_path(request.path_info)

        if not language_from_path and i18n_patterns_used and not prefixed_default_language:
            language = settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
