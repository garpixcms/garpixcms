from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from garpix_page.views.page import PageView
from multiurl import ContinueResolving, multiurl
from django.http import Http404
from django.conf import settings
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from garpix_auth.views import LogoutView, LoginView
from garpix_auth.rest.obtain_auth_token import obtain_auth_token
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.ENABLE_GARPIX_AUTH:
    urlpatterns += [
        path('logout/', LogoutView.as_view(url='/'), name="logout"),
        path('login/', LoginView.as_view(), name="authorize"),
        path('api/login/', obtain_auth_token),
    ]

if settings.DEBUG:
    schema_view = get_schema_view(openapi.Info(
        title="Application",
        default_version='v1',
        description="API docs",
        contact=openapi.Contact(email="garpix@garpix.com"),
    ), public=False)

    urlpatterns += [
        url(r'^api/docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)$', PageView.as_view(), name='page'),
        re_path(r'^(?P<url>.*?)/$', PageView.as_view(), name='page'),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)
