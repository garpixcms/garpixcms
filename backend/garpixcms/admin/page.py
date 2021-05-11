from ..models.page import Page
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(Page)
class PageAdmin(BasePageAdmin):
    pass
