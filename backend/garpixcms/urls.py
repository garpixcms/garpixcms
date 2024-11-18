from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from multiurl.multiurl import ContinueResolving, multiurl
from django.http import Http404
from django.conf import settings
from django.conf.urls.static import static
from garpix_user.views import LogoutView, LoginView, obtain_auth_token
from garpix_page.views.page import PageView
from garpix_page.views.index import IndexView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('page_lock/', include('garpix_admin_lock.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path(f'{settings.API_URL}/social-auth/', include('rest_framework_social_oauth2.urls'),
         name=settings.DRFSO2_URL_NAMESPACE),
    path('', include(('garpix_user.urls', 'garpix_user'), namespace='garpix_user')),
    path(f'{settings.API_URL}/garpix_user/token/', obtain_auth_token, name='token'),
    path('', include(('garpix_page.urls', 'garpix_page'), namespace='garpix_page')),
]

urlpatterns += [
    path('logout/', LogoutView.as_view(url='/'), name="logout"),
    path('login/', LoginView.as_view(), name="authorize")
]


if settings.DEBUG or settings.ENABLE_SWAGGER:
    urlpatterns += [
        path(f'{settings.API_URL}/schema/', SpectacularAPIView.as_view(), name='schema'),
        path(f'{settings.API_URL}/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)/$', PageView.as_view(), name='page'),
        path('', IndexView.as_view()),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)
