from django.contrib import admin

from garpix_user.admin import UserAdmin
from user.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    pass
