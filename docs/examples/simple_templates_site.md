# Корпорат на шаблонах

Пример простого корпоративного сайта на шаблонах.

Сайт должен включать в себя следующее:

* Главная страница
* Новости список
* Новость детальная
* О нас
* Контакты

### Шаг 1. Создание нового проекта

Для начала, создайте новый проект по [документации](../install_new_project.md).

Далее необходимо смигрировать, создать пользователя и запустить сервер:

```bash
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser
python3 backend/manage.py runserver
```

И не забывайте использовать контроль версий:

```
git init
```

Если на [http://localhost:8000](http://localhost:8000) вы видите надпись "Ура, работает!", то можно переходить к следующему шагу.

![Ура, работает](/example_simple_templates_site/images/corp_hooray.png)

### Шаг 2. Создаем необходимые страницы в коде

В зависимости от функциональных возможностей сайта, могут потребоваться страницы
с различным контекстом. В GarpixCMS есть возможность создавать из административной панели
страницы с различным наполнением и поддержкой ЧПУ с сохранением возможности
разработчиком использовать различные представления и контексты для страниц.

Для создания страниц используется модуль [garpix_page](https://github.com/garpixcms/garpix_page) с предустановленными параметрами
(вы можете их расширять).

Для начала надо понять терминологию:

* Страница (Page, Model Page) - это модель, дочерний класс от `BasePage`. Вы можете создавать их сами.
* Контекст (Context) - функция, которая возвращает словарь. Находится в модели. Значения можно применять в шаблонах. Всегда включает в себя `object` (объект класса страницы) и `request`.
* Шаблон (Template) - стандартный Django шаблон.

**Для создания страниц будем использовать кодогенерацию.**

Параметры:

* `--app` - приложение, в котором создать код. Если приложения не существует, то оно будет создано.
* `--page` - название страницы, в snake_case. Название класса будет преобразовано в CamelCase автоматически.
* `--base` - абстрактная модель, от которой наследовать страницы.

Доступные варианты для параметра `--base`:

* `page` - одиночная страница (наследник от `BasePage`) или детальная страница списка. Например, "пост", "главная", "контакты", "товар", "услуга".
* `list` - списочная страница (наследник от `BaseListPage`). Например, "новости", "акции", "товары", "услуги".
* `search` - поисковая страница (наследник от `BaseSearchPage`). Это простая реализация поиска. По умолчанию ищет только по заголовкам (`title`).

#### 2.1. Создаем главную страницу

```bash
python3 backend/manage.py startpage --app=home --page=home --base=page
```

После этого будет создано новое приложение, добавлены модели, админка, класс для переводов, шаблон.

![Изображение](/example_simple_templates_site/images/corp_home_files.png)

#### 2.2. Создаем страницу Контакты

```bash
python3 backend/manage.py startpage --app=contacts --page=contact --base=page
```

#### 2.3. Создаем новости

```bash
python3 backend/manage.py startpage --app=news --page=post_list --base=list

python3 backend/manage.py startpage --app=news --page=post --base=page
```

#### 2.4. Создаем поисковую страницу

```bash
python3 backend/manage.py startpage --app=search --page=search --base=search
```

#### 2.5. Для страницы "О нас" будем использовать стандартные страницы `garpixcms.Page` (см. ниже).

### Шаг 3. Настраиваем страницы

#### 3.1 Главная страница

На главной странице добавим карусель изображений.

Для этого создадим обычную модель CarouselItem, которую будем связывать с главной страницей:

```python
# backend/home/models/carousel_item.py
from django.db import models
from garpix_utils.file.file_field import get_file_path
from garpix_menu.mixins import LinkMixin
from .home_page import HomePage


class CarouselItem(LinkMixin):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    home_page = models.ForeignKey(HomePage, on_delete=models.CASCADE, verbose_name='Страница (привязка)', related_name='carousel_items')
    image = models.ImageField(upload_to=get_file_path, verbose_name='Изображение')
    sort = models.PositiveSmallIntegerField(default=100, verbose_name='Сортировка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Элемент карусели'
        verbose_name_plural = 'Элементы карусели'
        ordering = ('sort',)
```

Здесь мы импортировали `LinkMixin` из `garpix_menu` - это позволит ставить ссылку на
любую страницу или внешний URL для каждого объекта.

Также, не забудьте сделать еще две вещи:

Поправить `__init__.py`:

```python
# backend/home/models/__init__.py
from .home_page import HomePage  # noqa
from .carousel_item import CarouselItem  # noqa
```

И добавить созданные нами приложения в `INSTALLED_APPS`:

```python
# backend/app/settings.py
from garpixcms.settings import *  # noqa

INSTALLED_APPS += [  # noqa
    'home',
    'contacts',
    'news',
    'search',
]
```

После этого можно смигрировать:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

И сделать админку:

```python
# backend/home/admin/carousel_item.py
from ..models.carousel_item import CarouselItem
from django.contrib import admin


class CarouselItemInline(admin.TabularInline):
    model = CarouselItem
    fk_name = 'home_page'
    fields = ('title', 'image', 'sort', 'page', 'url')
    extra = 1
```

Не забываем про `__init__.py`:

```python
# backend/home/admin/__init__.py
from .home_page import HomePageAdmin  # noqa
from .carousel_item import CarouselItemInline  # noqa
```

И подключить к странице `HomePage` саму карусель:

```python
# backend/home/admin/home_page.py
from django.contrib import admin
from garpix_page.admin import BasePageAdmin
from ..models.home_page import HomePage
from .carousel_item import CarouselItemInline


@admin.register(HomePage)
class HomePageAdmin(BasePageAdmin):
    inlines = (CarouselItemInline,)
```

Теперь можно попробовать запустить сервер (стандартный `python3 backend/manage.py runserver`) и создать
в "Структуре страниц" запись с "Home" со следующими данными:

* Название: Главная
* ЧПУ: стираем, должно быть пустым
* Сайты для отображения: Выбираем единственное значение (по умолчанию уже выбрано)
* Можно также заполнить SEO-теги (далее вы сможете их увидеть, если откроете код страницы [http://localhost:8000/](http://localhost:8000/))

Также, добавьте пару слайдов для карусели на ваш вкус.

После этого можно зайти на страницу [http://localhost:8000](http://localhost:8000) и увидеть,
что отображается заголовок страницы, но нет нашей карусели.

Т.к. в шаблонах по умолчанию используется Bootstrap 5, то давайте просто возьмем
карусель оттуда и вставим в наш шаблон:

```html
<!-- frontend/templates/pages/home.html -->
{% extends 'base.html' %}

{% block content %}
    <h1>{{ object.title }}</h1>

    <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
            {% for item in object.carousel_items.all %}
                <div class="carousel-item {% if forloop.first %}active{% endif %}">
                    <a href="{{ item.get_link }}">
                        <img class="d-block w-100" src="{{ item.image.url }}" alt="{{ item.title }}">
                    </a>
                </div>
            {% endfor %}
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls"
                data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls"
                data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
    </div>
{% endblock %}
```

После этого снова можно зайти на главную страницу и увидеть, что карусель работает. Также, вы можете создать другие
страницы, чтобы поставить на них ссылки с карусели.

![Изображение](/example_simple_templates_site/images/corp_home_site.png)

#### 3.2 Страница Контакты

Теперь давайте сделаем страницу с формой обратной связи.

##### 3.2.1. Наполнение страницы Контакты

В шаге 2.2 мы уже подготовили модель страницы контактов. Теперь давайте добавим в нее отличительных черт:

```python
# backend/contacts/models/contact_page.py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from garpix_page.models import BasePage


class ContactPage(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')
    postal_address = models.CharField(max_length=250, blank=True, default='', verbose_name='Почтовый адрес')

    template = "pages/contact.html"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ("-created_at",)
```

Обычно, необходимо также указывать электронную почту и номер телефона. Но они располагаются на всех страницах, поэтому
в контакты мы их не стали включать - вы можете сделать их глобальными через `django-solo`.
Реализуется как описано в документации [https://github.com/lazybird/django-solo](https://github.com/lazybird/django-solo).

Можно мигрировать:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

Давайте поправим шаблон страницы "Контакты":

```html
<!-- frontend/templates/pages/contact.html -->
{% extends 'base.html' %}

{% block content %}

    {% include 'include/breadcrumb.html' %}

    <h1>{{ object.title }}</h1>

    {% if object.postal_address %}
        <div class="alert alert-primary" role="alert">
            Почтовый адрес: {{ object.postal_address }}
        </div>
    {% endif %}

    <div>{{ object.content|safe }}</div>
{% endblock %}
```

И создадим в административной панели в Структуре страниц - "Contact":

* Название: Контакты
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* Почтовый адрес: г. Москва
* Содержание: Привет всем, вы можете оставить нам сообщение на этой странице.

Получится нечто подобное:

![Изображение](/example_simple_templates_site/images/corp_contact_site.png)

##### 3.2.2. Реализация формы обратной связи

Теперь давайте реализуем форму обратной связи.

Сначала поправим шаблон. Добавим новый файл `frontend/templates/include/feedback.html`:

```html
<!-- frontend/templates/include/feedback.html -->
<form method="post">
    {% csrf_token %}
    <div class="row mb-3">
        <label for="inputEmail" class="col-sm-2 col-form-label">Email</label>
        <div class="col-sm-10">
            <input type="email" name="email" class="form-control" id="inputEmail">
        </div>
    </div>
    <div class="row mb-3">
        <label for="inputComment" class="col-sm-2 col-form-label">Комментарий</label>
        <div class="col-sm-10">
            <textarea class="form-control" name="comment" id="inputComment" rows="3"></textarea>
        </div>
    </div>
    <button type="submit" class="btn btn-primary">Отправить</button>
</form>
```

И добавим его в шаблон страницы:

```html
<!-- frontend/templates/pages/contact.html -->
{% extends 'base.html' %}

{% block content %}

    {% include 'include/breadcrumb.html' %}

    <h1>{{ object.title }}</h1>

    {% if object.postal_address %}
        <div class="alert alert-primary" role="alert">
            Почтовый адрес: {{ object.postal_address }}
        </div>
    {% endif %}

    <div>{{ object.content|safe }}</div>

    {% include 'include/feedback.html' %}
{% endblock %}
```

Теперь создадим модель для получения писем обратной связи:

```python
# backend/contacts/models/feedback.py
from django.db import models


class Feedback(models.Model):
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
```

И не забывайте про `__init__.py`:

```python
# backend/contacts/models/__init__.py
from .contact_page import ContactPage  # noqa
from .feedback import Feedback  # noqa
```

Создадим админку:

```python
# backend/contacts/admin/feedback.py
from django.contrib import admin
from ..models.feedback import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'comment', 'created_at')
    readonly_fields = ('created_at',)
```

И снова `__init__.py`:

```python
# backend/contacts/admin/__init__.py
from .contact_page import ContactPageAdmin  # noqa
from .feedback import FeedbackAdmin  # noqa
```

Теперь давайте добавим форму:

```python
# backend/contacts/forms/feedback.py
from django.forms import ModelForm
from ..models.feedback import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['email', 'comment']
```

И `__init__.py`:

```python
# backend/contacts/forms/__init__.py
from .feedback import FeedbackForm  # noqa
```

Теперь давайте смигрируем:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

И реализуем обработчик формы через функцию `get_context` у модели страницы `ContactPage`:

```python
# backend/contacts/models/contact_page.py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from garpix_page.models import BasePage
from ..forms.feedback import FeedbackForm


class ContactPage(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')
    postal_address = models.CharField(max_length=250, blank=True, default='', verbose_name='Почтовый адрес')

    template = "pages/contact.html"

    def get_context(self, request=None, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save()
                context.update({
                    'message': 'Сообщение успешно отправлено',
                })
            context.update({
                'form': form,
            })
        return context

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ("-created_at",)
```

Как видим, мы сделали обработчик формы и расширили передаваемый в шаблон контекст.

Теперь добавим вывод `message`, когда он есть, в шаблоне.

```html
<!-- frontend/templates/include/feedback.html -->
<form method="post">
    {% csrf_token %}
    <div class="row mb-3">
        <label for="inputEmail" class="col-sm-2 col-form-label">Email</label>
        <div class="col-sm-10">
            <input type="text" name="email" value="{{ form.email.value }}" class="form-control" id="inputEmail">
        </div>
    </div>
    <div class="row mb-3">
        <label for="inputComment" class="col-sm-2 col-form-label">Комментарий</label>
        <div class="col-sm-10">
            <textarea class="form-control" required name="comment" id="inputComment" rows="3">{{ form.comment.value }}</textarea>
        </div>
    </div>
    <button type="submit" class="btn btn-primary">Отправить</button>
</form>

{% if message %}
<div class="alert alert-success mt-3" role="alert">
    {{ message }}
</div>
{% endif %}

{% if form.errors %}
    <div class="alert alert-danger mt-3" role="alert">
        <div>При отправке возникли ошибки:</div>
        <div>{{ form.errors }}</div>
    </div>
{% endif %}
```

После этого можете зайти на страницу "Контакты" и отправить форму, в административной панели можно увидеть,
что все сохраняется, когда форма валидна.

![Изображение](/example_simple_templates_site/images/corp_contact_site_success.png)

![Изображение](/example_simple_templates_site/images/corp_contact_site_error.png)

![Изображение](/example_simple_templates_site/images/corp_contact_feedback.png)

##### 3.2.3. Отправка уведомления

Для завершения нашей формы обратной связи осталось отправить письмо по настоящему.

Для этого будем использовать батарейку `garpix_notify` и отправку писем по SMTP в ней. Эта батарейка уже встроена в GARPIX CMS.

Создадим в "Уведомления" - "Категории" новую запись:

* Заголовок: Стандарт
* Шаблон: {{text}}

Категории позволяют использовать одинаковую верстку (шапку, футер, подпись и т.п.) в уведомлениях. Для различных писем, можно использовать
различные категории.

Например, ввиду того, что мы будем отправлять обычное уведомление, то так его и назвали.

Теперь зайдем в "Уведомления" - "SMTP аккаунты" и добавим новую запись, используя данные SMTP вашего провайдера электронной почты.

Подготовка практически завершена. Давайте создадим событие, по которому будем отправлять письмо.
Для этого в `backend/app/settings.py` добавим следующее:

```python
# backend/app/settings.py
from garpixcms.settings import *  # noqa

INSTALLED_APPS += [  # noqa
    'home',
    'contacts',
    'news',
    'search',
]

FEEDBACK_EVENT = 1

NOTIFY_EVENTS = {
    FEEDBACK_EVENT: {
        'title': 'Обратная связь',
    },
}

CHOICES_NOTIFY_EVENT = [(k, v['title']) for k, v in NOTIFY_EVENTS.items()]
```

Обратите внимание, что, обычно, на сайтах может использоваться множество событий для оповещения пользователя.
Давайте наиболее понятные имена для событий, т.к. с ними работает и разработчик и администратор сайта.

Добавим в обработку формы отправку уведомления:

```python
# backend/contacts/models/contact_page.py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from garpix_page.models import BasePage
from ..forms.feedback import FeedbackForm
from garpix_notify.models import Notify
from django.conf import settings


class ContactPage(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')
    postal_address = models.CharField(max_length=250, blank=True, default='', verbose_name='Почтовый адрес')

    template = "pages/contact.html"

    def get_context(self, request=None, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save()
                Notify.send(settings.FEEDBACK_EVENT, {
                    'feedback': feedback,
                }, email=feedback.email)
                context.update({
                    'message': 'Сообщение успешно отправлено',
                })
            context.update({
                'form': form,
            })
        return context

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ("-created_at",)
```

Мигрируем:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

Теперь идем в административную панель "Уведомления" - "Шаблоны" и создаем два шаблона.

Первый будет отправлять письмо администратору:

* Название для админа: Обратная связь - администратору
* Заголовок: Новое сообщение обратной связи
* Текст и HTML:
```
Получено новое сообщение:

Email: {{feedback.email}}
Комментарий: {{feedback.comment}}
```
* Пользователь (получатель): Указывайте свой аккаунт (убедитесь, что при создании пользователя указали email)
* Тип: E-mail
* Категория: Стандарт
* Событие: Обратная связь

Второе письмо будет отправляться на адрес указанного email.

* Название для админа: Обратная связь - клиенту
* Заголовок: Спасибо за сообщение!
* Текст и HTML:
```
Спасибо за сообщение!

Вы оставили следующий комментарий у нас на сайте:

{{feedback.comment}}
```
* Пользователь (получатель): Не указываем ничего
* Тип: E-mail
* Категория: Стандарт
* Событие: Обратная связь

Как результат, при срабатывании события FEEDBACK_EVENT будет срабатываться оба шаблона и будет отправляться два письма.
Если необходима отправка дополнительных писем или сообщений по другим каналам, то это тоже возможно.

Внимание! Письма отправляются в фоновом потоке, необходимо запустить `celery` в отдельном терминале:

```bash
cd backend
celery -A app worker --loglevel=info -B
```

После этих действий попробуйте заполнить и отправить форму на лицевой части сайта.

![Изображение](/example_simple_templates_site/images/corp_site_feedback_pending.png)

Примерно через минуту письма дойдут (можно изменить в "Уведомления" - "Настройка")

![Изображение](/example_simple_templates_site/images/corp_site_feedback_success.png)

Итого, обратная связь полностью готова. Переходим к следующему пункту.

#### 3.3. Новости

Мы уже создали списочную и детальную страницу новостей.

Давайте добавим поле `content` в детальную новость. Она станет очень похожа на другие наши модели, но
логично держать их в разных моделях. Списочную страницу менять не будем, но посмотрите на ее содержимое.

```python
# backend/news/models/post_page.py
from ckeditor_uploader.fields import RichTextUploadingField
from garpix_page.models import BasePage


class PostPage(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')
    template = "pages/post.html"

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ("-created_at",)
```

Мигрируем:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

Теперь идем в админку и "Структуру страниц" и создаем сначала список новостей (`PostList`) и заполняем
следующим образом:

* Название: Новости
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение

Затем создайте несколько новостей, например так:

Пост 1:

* Название: Пост 1
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* Родительская страница: Новости
* Содержание: Содержание поста 1

Пост 2:

* Название: Пост 2
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* Родительская страница: Новости
* Содержание: Содержание поста 2

Пост 3:

* Название: Пост 3
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* Родительская страница: Новости
* Содержание: Содержание поста 3

Получится примерно следующее

![Изображение](/example_simple_templates_site/images/corp_news_admin.png)

Давайте подправим шаблон детальной новости (мы же добавили новое поле):

```html
<!-- frontend/templates/pages/post.html -->
{% extends 'base.html' %}

{% block content %}
    {% include 'include/breadcrumb.html' %}
    <h1>{{ object.title }}</h1>
    <div>{{ object.content|safe }}</div>
{% endblock %}
```

Теперь можете попробовать перейти по ссылке "Новости" в "Структуре страниц" и увидите, работающие переходы между страницами и хлебными крошками. Также, вы можете добавить большое количество постов
или уменьшить значение `paginated_by` в модели `PostList` для того, чтобы появилась пагинация.

![Изображение](/example_simple_templates_site/images/corp_site_news.png)

![Изображение](/example_simple_templates_site/images/corp_site_news_post.png)

С новостями готово, пошли к следующему шагу.

#### 3.4. Страница поиска

Идем в "Структура страниц" и добавляем страницу `Search` и заполняем ее:

* Название: Поиск
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение

Готово. По умолчанию поиск только по заголовкам страниц.

Попробуйте перейти на страницу на лицевой части сайта и вбить заголовок одной из страниц, получите
нечто подобное:

![Изображение](/example_simple_templates_site/images/corp_site_search.png)

Для того, чтобы поиск шел также по содержимому, то добавьте поля в `searchable_fields` у модели.

Давайте поменяем это у новостей:

```python
# backend/news/models/post_page.py
from ckeditor_uploader.fields import RichTextUploadingField
from garpix_page.models import BasePage


class PostPage(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')
    template = "pages/post.html"
    searchable_fields = ['title', 'content']

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ("-created_at",)
```

Теперь можете поискать по содержимому новостей.

Обратите внимание, что данный поиск простейший и не полнотекстовый. Используйте его только тогда, когда нет особых требований для поиска.
Когда нужен серьезный инструмент для поиска - используйте ElasticSearch или аналогичные решения.

С поиском закончили, переходим к следующему шагу.

#### 3.5. Страница "О нас"

Будем использовать встроенный `Page`.

Идем в "Структура страниц", добавляем и выбираем "Страница", заполняем данными:

* Название: О нас
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* Содержание: Контент о нас.

Обычно требуется изменять внешний вид страниц, для этого просто перезапишите шаблон `frontend/templates/garpixcms/pages/default.html`.

#### 3.6. Меню

Со страницами закончили, теперь добавим удобства, создав меню.

Для этого изменим доступные меню в `backend/app/settings.py`, добавим следующий код:

```python
# ...

MENU_TYPE_HEADER_MENU = 'header_menu'

MENU_TYPES = {
    MENU_TYPE_HEADER_MENU: {
        'title': 'Верхнее меню',
    },
}

CHOICE_MENU_TYPES = [(k, v['title']) for k, v in MENU_TYPES.items()]
```

Теперь удалите ненужное меню в футере:

* В файле `frontend/templates/base.html` убрать строку `{% include 'include/footer.html' %}`.
* Удалить файл `frontend/templates/include/footer.html`.

После этого мигрируем.

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

Идем в админку "Меню" - "Пункты меню" и заполняем:

Главная:

* Название для админа: Главная
* Название: Главная
* Тип меню: Верхнее меню
* Страница, на которую ведет пункт меню: Главная страница
* Сортировка: 50

Новости:

* Название для админа: Новости
* Название: Новости
* Тип меню: Верхнее меню
* Страница, на которую ведет пункт меню: Новости
* Сортировка: 100

О нас:

* Название для админа: О нас
* Название: О нас
* Тип меню: Верхнее меню
* Страница, на которую ведет пункт меню: О нас
* Сортировка: 150

Поиск:

* Название для админа: Поиск
* Название: Поиск
* Тип меню: Верхнее меню
* Страница, на которую ведет пункт меню: Поиск
* Сортировка: 200

Контакты:

* Название для админа: Контакты
* Название: Контакты
* Тип меню: Верхнее меню
* Страница, на которую ведет пункт меню: Контакты
* Сортировка: 250

После добавления меню, вы сможете перемещаться по сайту. Количество типов меню также не ограничивается, но будьте аккуратны с неймингом.

![Изображение](/example_simple_templates_site/images/corp_site_menu.png)

#### 3.7. Карта сайта

Обратите внимание, что из коробки строится карта сайта из всех страниц.

Увидеть ее вы можете по адресу [http://localhost:8000/sitemap.xml](http://localhost:8000/sitemap.xml)

Для смены домена используются обычный `Sites Framework`. Поменять адрес можно в административной панели в "Сайты" - "Сайты".


На этом все, наш простой корпоративный сайт готов. Спасибо за внимание и успехов вам!
