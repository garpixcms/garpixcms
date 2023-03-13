from django.contrib import admin

from garpix_user.admin import UserAdmin as BaseUSerAdmin
from user.models import User


@admin.register(User)
class UserAdmin(BaseUSerAdmin):
    pass
