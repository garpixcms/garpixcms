from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        ('Viber', {
            'fields': (
                'viber_chat_id',
                'viber_secret_key',
            )
        }),
    ) + UserAdmin.fieldsets
