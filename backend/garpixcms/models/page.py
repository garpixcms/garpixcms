from ckeditor_uploader.fields import RichTextUploadingField
from garpix_page.models import BasePage


class Page(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ('-created_at',)
