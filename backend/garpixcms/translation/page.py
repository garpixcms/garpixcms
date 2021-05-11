from modeltranslation.translator import TranslationOptions, register
from ..models import Page


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('content',)
