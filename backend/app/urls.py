from garpixcms.urls import *  # noqa

urlpatterns = [
  path('admin/page_lock/', include('garpix_admin_lock.urls')),
] + urlpatterns  # noqa
