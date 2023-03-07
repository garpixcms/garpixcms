import functools

from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.urls import get_resolver, LocalePrefixPattern, Resolver404
from django.utils import translation


def resolve_class(get_resolver, path):
    path = str(path)
    tried = []
    match = get_resolver.pattern.match(path)
    if match:
        new_path, args, kwargs = match
        for pattern in get_resolver.url_patterns:
            try:
                sub_match = pattern.resolve(new_path)
            except Resolver404 as e:
                try:
                    get_resolver._extend_tried(tried, pattern, e.args[0].get('tried'))
                except AttributeError:
                    pass
            else:
                if sub_match:
                    sub_match_dict = {**kwargs, **get_resolver.default_kwargs}
                    sub_match_dict.update(sub_match.kwargs)
                    try:
                        get_resolver._extend_tried(tried, pattern, sub_match.tried)
                    except AttributeError:
                        pass
                    return pattern
                tried.append([pattern])


@functools.lru_cache(maxsize=None)
def is_language_prefix_patterns_used_for_url(urlconf, path):
    resolver_class = resolve_class(get_resolver(urlconf), path)
    if resolver_class and isinstance(resolver_class.pattern, LocalePrefixPattern):
        return True, resolver_class.pattern.prefix_default_language
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
