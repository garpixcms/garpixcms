from garpixcms.settings import env
from django.contrib import admin

if env.bool('DISABLE_USER_ADMIN', False):
    from user.models import User
    from django.contrib.auth.models import Group

    admin.site.unregister(User)
    admin.site.unregister(Group)

if env.bool('DISABLE_SOCIAL_DJANGO', False):
    from social_django.models import UserSocialAuth, Association, Nonce

    admin.site.unregister(Association)
    admin.site.unregister(Nonce)
    admin.site.unregister(UserSocialAuth)

if env.bool('DISABLE_BASE_PAGE', False):
    from garpix_page.models import BasePage

    admin.site.unregister(BasePage)

if env.bool('DISABLE_MENU_ITEM', False):
    from garpix_menu.models import MenuItem

    admin.site.unregister(MenuItem)

if env.bool('DISABLE_GARPIX_NOTIFY', False):
    from garpix_notify.models import (
        Notify, NotifyCategory, NotifyConfig, NotifyDevice,
        NotifyFile, SMTPAccount, NotifyTemplate, NotifyUserList,
    )

    admin.site.unregister(Notify)
    admin.site.unregister(NotifyCategory)
    admin.site.unregister(NotifyConfig)
    admin.site.unregister(NotifyDevice)
    admin.site.unregister(NotifyFile)
    admin.site.unregister(SMTPAccount)
    admin.site.unregister(NotifyTemplate)
    admin.site.unregister(NotifyUserList)

if env.bool('DISABLE_DJANGO_OAUTH_TOOLKIT', False):
    from oauth2_provider.models import AccessToken, Application, Grant, IDToken, RefreshToken

    admin.site.unregister(AccessToken)
    admin.site.unregister(Application)
    admin.site.unregister(Grant)
    admin.site.unregister(IDToken)
    admin.site.unregister(RefreshToken)

if env.bool('DISABLE_SITE', False):
    from django.contrib.sites.models import Site

    admin.site.unregister(Site)
