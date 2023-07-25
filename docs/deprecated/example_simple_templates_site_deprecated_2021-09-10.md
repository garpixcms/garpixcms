# Корпорат на шаблонах

Пример простого корпоративного сайта на шаблонах.

Сайт должен включать в себя следующее:

* Главная страница
* Новости список
* Новость детальная
* О нас
* Контакты

#### Шаг 1. Создание нового проекта

Для начала, создайте новый проект по [документации](../install_new_project.md).

Если после входа увидите ошибку "No template names provided" - это значит, что можно переходить к следующему шагу.

#### Шаг 2. Создаем структуру в админ-панели

Заходим в админ-панель по адресу [http://localhost:8000/admin/](http://localhost:8000/admin/).

**2.1. Заходим в "Сайты". Можно отредактировать адрес сайта на тот, который вам необходим. На компьютере разработчика можно использовать и тот, что по умолчанию - `example.com`.**

**2.2. Заходим в "Структура страниц". Нажимаем "Добавить", заполняем поля:**

* Название: "Главная"
* ЧПУ: стираем, должно быть пустым
* Сайты для отображения: Выбираем единственное значение
* Содержимое: "Главная страница моего сайта"
* Можно также заполнить SEO-теги (далее вы сможете их увидеть, если откроете код страницы [http://localhost:8000/](http://localhost:8000/))

и сохраняйте.
  
**2.3. После этого, вы можете зайти на главную страницу сайта [http://localhost:8000/](http://localhost:8000/) и увидеть стандартный бутстрап-шаблон, в который вывелись значения.**

**2.4. Возвращаемся в административную панель и создаем еще страницу через "Структуру страниц":**

Страница "О нас":

* Название: "О нас"
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* Содержимое: "Здесь текст о нас"

**2.5. Далее создаем меню. Переходим в "Пункты меню".**

Добавляем пункты меню.

Меню "Главная":

* Название для админа: Главная
* Название: Главная
* Тип меню: Header menu
* Страница, на которую ведет пункт меню: Главная страница
* Сортировка: 50

Меню "О нас":

* Название для админа: О нас
* Название: О нас
* Тип меню: Header menu
* Страница, на которую ведет пункт меню: О нас
* Сортировка: 80

**2.6. После этого, вы можете зайти на главную страницу сайта [http://localhost:8000/](http://localhost:8000/) и увидеть меню, при переходе по которым можно увидеть содержимое страниц.**

#### Шаг 3. Использование страниц

**3.1. Пояснения**

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

Вы можете посмотреть на страницу по умолчанию в `garpixcms/models/page.py`.

**3.2. Добавляем новые типы страниц**

Давайте добавим недостающие для нас типы страниц. Для этого разберем то, что есть сейчас и что необходимо добавить/изменить.

**3.2.1. Страница "Контакты"**

Эта страница должна включать в себя карту, поэтому у нее должен быть другой шаблон.
Например, поля "номер телефона", "емейл", "адрес", которые необходимо
задавать из административной панели. Соответственно, потребуется еще одна модель.

Давайте создадим новое приложение для нашего контента.

```bash
cd backend
python3 manage.py startapp content
```

Удаляем файл `models.py`, создаем директорию `content/models`.

В директории `content/models` создаем файл `contact_page.py` и создаем модель страницы (обратите внимание, на то, что это наследник `BasePage`):

```python
from garpix_page.models import BasePage
from django.db import models


class ContactPage(BasePage):
    address = models.CharField(max_length=250, verbose_name='Адрес', blank=True, default='', null=False)
    phone = models.CharField(max_length=30, verbose_name='Номер телефона', blank=True, default='', null=False)
    email = models.CharField(max_length=100, verbose_name='E-mail', blank=True, default='', null=False)
    
    template = 'pages/contact_page.html'

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"
        ordering = ('-created_at',)

```

Затем добавляем в директорию `content/models` файл `__init__.py` со следующим содержимым:

```python
from .contact_page import ContactPage

```

Удаляем файл `admin.py`. Создаем директорию `content/admin/` с файлом `contact_page.py` и содержимым:

```python
from ..models.contact_page import ContactPage
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(ContactPage)
class ContactPageAdmin(BasePageAdmin):
    pass

```

Затем добавляем в директорию `content/admin` файл `__init__.py` со следующим содержимым:

```python
from .contact_page import ContactPageAdmin

```

Добавляем переводы. Для этого, создаем директорию `content/translation/` и в ней файл `contact_page.py` с содержимым (обратите внимание, что поле `title` переводится по умолчанию и его добавлять не требуется):

```python
from modeltranslation.translator import TranslationOptions, register
from ..models import ContactPage


@register(ContactPage)
class ContactPageTranslationOptions(TranslationOptions):
    fields = ('address',)

```

Затем добавляем в директорию `content/translation` файл `__init__.py` со следующим содержимым:

```python
from .contact_page import ContactPageTranslationOptions

```

Добавляем новое приложение `content` в `app/settings.py`:

```bash
# app/settings.py

INSTALLED_APPS += ['content']

```

После чего создаем миграции и применяем их:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Также, у нас должно быть другой шаблон, поэтому давайте создадим директорию `content/templates/pages/` и в ней файл `contact_page.html` с содержимым:

```html
<!--{% extends 'garpixcms/base.html' %}-->

<!--{% block content %}-->
<!--<h1>{{object.title}}</h1>-->
<!--<div>-->
<!--    <p>Номер телефона: {{object.phone}}</p>-->
<!--    <p>E-mail: {{object.email}}</p>-->
<!--    <p>Адрес: {{object.address}}</p>-->
<!--</div>-->
<!--{% endblock %}-->
```

После этого идем в админ-панель и добавляем новую страницу через "Структура страниц":

Страница "Контакты" (выбираем модель "Контакты").

* Название: "Контакты"
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* E-mail: "example@gmail.com"
* Номер телефона: "8 999 999 99 99"
* Адрес: "г. Москва"

Затем идем в "Пункты меню" и добавляем новый:

* Название для админа: Контакты
* Название: Контакты
* Тип меню: Header menu
* Страница, на которую ведет пункт меню: Контакты
* Сортировка: 100

Теперь можете перейти на главную страница сайта и посмотреть результаты. Вы должны увидеть пункт меню "Контакты", при переходе на который вы можете управлять контентной страницей.

**3.2.2. Страница "Новость" (детальная страница новости)**

Добавим новую модель и создадим тип страницы.

В директории `content/models` создаем файл `news_page.py` (обратите внимание, что поля совпадают с обычной страницей (`garpixcms.Page`), но мы создали новую модель.
Это сделали для того, чтобы удобнее было управлять содержимым. Плюс, вполне возможно, что в будущем потребуется сделать особую логику, например, отложенную публикацию новостей.

```python
from garpix_page.models import BasePage
from ckeditor_uploader.fields import RichTextUploadingField


class NewsPage(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')
    
    template = 'pages/news_page.html'

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ('-created_at',)

```

Изменяем файл `content/models/__init__.py`:

```python
from .contact_page import ContactPage
from .news_page import NewsPage

```

В директории `content/admin` создаем файл `news_page.py`:

```python
from ..models.news_page import NewsPage
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(NewsPage)
class NewsPageAdmin(BasePageAdmin):
    pass

```

Изменяем файл `content/admin/__init__.py`:

```python
from .contact_page import ContactPageAdmin
from .news_page import NewsPageAdmin

```

В директории `content/translation` создаем файл `news_page.py`:

```python
from modeltranslation.translator import TranslationOptions, register
from ..models import NewsPage


@register(NewsPage)
class NewsPageTranslationOptions(TranslationOptions):
    fields = ('content',)

```

Изменяем файл `content/translation/__init__.py`:

```python
from .contact_page import ContactPageTranslationOptions
from .news_page import NewsPageTranslationOptions

```

Теперь опять создаем миграции и применяем их:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Также, можем реализовать другой шаблон, поэтому давайте создадим файл `content/templates/pages/news_detail.html`:

```html
<!--{% extends 'garpixcms/base.html' %}-->

<!--{% block content %}-->
<!--<h1>{{object.title}}</h1>-->
<!--<div>{{object.created_at|date:"d.m.Y"}}</div>-->
<!--<div>-->
<!--    {{object.content|safe}}-->
<!--</div>-->
<!--{% endblock %}-->
```

Пока не добавляйте новости в админ-панели. Сначала сделаем их списочное представление, см. дальше.

**3.2.3. Страница "Список новостей"**

Теперь необходимо создать страницу, которая будет содержать список новостей. Для этого сделаем еще один тип страниц.

В директории `content/models` создаем файл `news_list_page.py` и добавим модели особый контекст (функция `get_context`).

```python
from garpix_page.models import BasePage
from .news_page import NewsPage


class NewsListPage(BasePage):
    template = 'pages/news_list_page.html'
    
    def get_context(self, request=None, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = NewsPage.on_site.filter(is_active=True, parent=kwargs['object'])
        context.update({
            'posts': posts
        })
        return context

    class Meta:
        verbose_name = "Список новостей"
        verbose_name_plural = "Списки новостей"
        ordering = ('-created_at',)

```

Изменяем файл `content/models/__init__.py`:

```python
from .contact_page import ContactPage
from .news_page import NewsPage
from .news_list_page import NewsListPage

```

В директории `content/admin` создаем файл `news_list_page.py`:

```python
from ..models.news_list_page import NewsListPage
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(NewsListPage)
class NewsListPageAdmin(BasePageAdmin):
    pass

```

Изменяем файл `content/admin/__init__.py`:

```python
from .contact_page import ContactPageAdmin
from .news_page import NewsPageAdmin
from .news_list_page import NewsListPage

```

В директории `content/translation` создаем файл `news_list_page.py`:

```python
from modeltranslation.translator import TranslationOptions, register
from ..models import NewsListPage


@register(NewsListPage)
class NewsListPageTranslationOptions(TranslationOptions):
    pass

```

Изменяем файл `content/translation/__init__.py`:

```python
from .contact_page import ContactPageTranslationOptions
from .news_page import NewsPageTranslationOptions
from .news_list_page import NewsListPageTranslationOptions

```

Теперь опять создаем миграции и применяем их:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Также, можем реализовать другой шаблон, поэтому давайте создадим файл `content/templates/pages/news_list_page.html`:

```html
<!--{% extends 'garpixcms/base.html' %}-->

<!--{% block content %}-->
<!--<h1>{{object.title}}</h1>-->
<!--{% for post in posts %}-->
<!--    <div>-->
<!--        <h3><a href="{{post.get_absolute_url}}">{{post.title}}</a></h3>-->
<!--    </div>-->
<!--{% endfor %}-->
<!--{% endblock %}-->
```

Теперь можно заходить в административную панель, создавать объект "Список новостей" и заполнять его данные.

После этого, создавайте объекты "Новость" и указывайте поле "Родитель" у объекта список новостей, который только что создали.

Остается добавить меню:

* Название для админа: Новости
* Название: Новости
* Тип меню: Header menu
* Страница, на которую ведет пункт меню: Список новостей
* Сортировка: 100

После этого, можно перейти на [http://localhost:8000](http://localhost:8000) и посмотреть что получилось.

P.S. Вы можете переписать шаблон для обычных страниц `templates/garpixcms/pages/default.html`, например, на следующее содержимое:

```html
<!--{% extends 'garpixcms/base.html' %}-->

<!--{% block content %}-->
<!--<h1>{{object.title}}</h1>-->
<!--<div>-->
<!--    {{object.content|safe}}-->
<!--</div>-->
<!--{% endblock %}-->
```
