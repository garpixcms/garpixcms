from ckeditor_uploader.fields import RichTextUploadingField
from garpix_page.models import BasePage


class Page(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')

    template = 'garpixcms/pages/default.html'

    class Meta:
        verbose_name = "Страница | Page"
        verbose_name_plural = "Страницы | Pages"
        ordering = ('-created_at',)
