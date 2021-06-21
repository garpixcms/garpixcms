# Корпорат на шаблонах

Пример простого корпоративного сайта на шаблонах.

Сайт должен включать в себя следующее:

* Главная страница
* Новости список
* Новость детальная
* О нас
* Контакты

#### Шаг 1. Создание нового проекта

Для начала, создайте новый проект по [документации](install_new_project.md).

Если после входа увидите ошибку "No template names provided" - это значит, что можно переходить к следующему шагу.

#### Шаг 2. Создаем структуру в админ-панели

Заходим в админ-панель по адресу [http://localhost:8000/admin/](http://localhost:8000/admin/).

**2.1. Заходим в "Сайты". Можно отредактировать адрес сайта на тот, который вам необходим. На компьютере разработчика можно использовать и тот, что по умолчанию - `example.com`.**

**2.2. Заходим в "Структура страниц". Нажимаем "Добавить", заполняем поля:**

* Название: "Главная"
* ЧПУ: стираем, должно быть пустым
* Сайты для отображения: Выбираем единственное значение
* Тип страницы: "Главная страница"
* Содержимое: "Главная страница моего сайта"
* Можно также заполнить SEO-теги (далее вы сможете их увидеть, если откроете код страницы [http://localhost:8000/](http://localhost:8000/))

и сохраняйте.
  
**2.3. После этого, вы можете зайти на главную страницу сайта [http://localhost:8000/](http://localhost:8000/) и увидеть стандартный бутстрап-шаблон, в который вывелись значения.**

**2.4. Возвращаемся в административную панель и создаем еще страницу через "Структуру страниц":**

Страница "О нас":

* Название: "О нас"
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* Тип страницы: "Обычная страница"
* Содержимое: "Здесь текст о нас"

**2.5. Далее создаем меню. Переходим в "Пункты меню".**

Добавляем пункты меню.

Меню "Главная":

* Название для админа: Главная
* Название: Главная
* Тип меню: Header menu
* Страница, на которую ведет пункт меню: Главная страница
* Сортировка: 50

Меню "Доставка":

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
* Тип страницы (Page Type) - захардкоженный в `settings.py` тип страницы. Необходим для возможности создания разного поведения и представления страниц (именно поэтому он не объединен со Страницей в одну сущность).
* Контекст (Context) - функция, которая возвращает словарь. Значения можно применять в шаблонах. Всегда включает в себя `object` (объект класса страницы) и `request`.
* Шаблон (Template) - стандартный Django шаблон.

Рассмотрим то, что есть в типах страниц по умолчанию (файл `app/settings.py` импортирует все из внутреннего `garpixcms/settings.py`):

```python
PAGE_TYPE_HOME = 'HOME'  # Тип страницы
PAGE_TYPE_DEFAULT = 'DEFAULT'  # Тип страницы

PAGE_TYPES = {
    PAGE_TYPE_HOME: {
            'title': 'Главная страница',  # Название для типа страницы
            'template': 'garpixcms/pages/home.html',  # Шаблон для типа страницы
            'context': 'garpix_page.contexts.default.context'  # Контекст для типа страницы
    },
    PAGE_TYPE_DEFAULT: {
            'title': 'Обычная страница',  # Название для типа страницы
            'template': 'garpixcms/pages/default.html',  # Шаблон для типа страницы
            'context': 'garpix_page.contexts.default.context'  # Контекст для типа страницы
    },
}

CHOICES_PAGE_TYPES = [(k, v['title']) for k, v in PAGE_TYPES.items()]  # Получение choices из словаря
```

Обратите внимание, что тип страниц связывается с самой страницей (моделью) через админ-панель.

Вы можете посмотреть на страницу по умолчанию в `garpixcms/models/page`.

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

    class Meta:
        verbose_name = "Страница Контакты"
        verbose_name_plural = "Страницы Контакты"
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

INSTALLED_APPS.append('content')

```

После чего создаем миграции и применяем их:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Также, у нас должно быть другой шаблон, поэтому давайте создадим директорию `content/templates/pages/` и в ней файл `contact_page.html` с содержимым:

```html
{% extends 'garpixcms/base.html' %}

{% block content %}
<h1>{{object.title}}</h1>
<div>
    <p>Номер телефона: {{object.phone}}</p>
    <p>E-mail: {{object.email}}</p>
    <p>Адрес: {{object.address}}</p>
</div>
{% endblock %}
```

Теперь добавляем новый тип страниц, редактируем `app/settings.py`:

```python
PAGE_TYPE_HOME = 'HOME'
PAGE_TYPE_DEFAULT = 'DEFAULT'
PAGE_TYPE_CONTACT = 'CONTACT'

PAGE_TYPES = {
    PAGE_TYPE_HOME: {
            'title': 'Главная страница',
            'template': 'garpixcms/pages/home.html',
            'context': 'garpix_page.contexts.default.context'
    },
    PAGE_TYPE_DEFAULT: {
            'title': 'Обычная страница',
            'template': 'garpixcms/pages/default.html',
            'context': 'garpix_page.contexts.default.context'
    },
    PAGE_TYPE_CONTACT: {
            'title': 'Страница Контакты',
            'template': 'pages/contact_page.html',
            'context': 'garpix_page.contexts.default.context'
    },
}

CHOICES_PAGE_TYPES = [(k, v['title']) for k, v in PAGE_TYPES.items()]

```

После этого идем в админ-панель и добавляем новую страницу через "Структура страниц":

Страница "Контакты" (выбираем модель "Страница Контакты").

* Название: "Контакты"
* ЧПУ: автоматически
* Сайты для отображения: Выбираем единственное значение
* Тип страницы: "Страница Контакты"
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

В директории `content/models` создаем файл `news_page.py`:

```python
from garpix_page.models import BasePage
from ckeditor_uploader.fields import RichTextUploadingField


class NewsPage(BasePage):
    content = RichTextUploadingField(verbose_name='Содержание', blank=True, default='')

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
{% extends 'garpixcms/base.html' %}

{% block content %}
<h1>{{object.title}}</h1>
<div>{{object.created_at|date:"d.m.Y"}}</div>
<div>
    {{object.content|safe}}
</div>
{% endblock %}
```

Теперь добавляем новый тип страниц, редактируем `app/settings.py`:

```python
PAGE_TYPE_HOME = 'HOME'
PAGE_TYPE_DEFAULT = 'DEFAULT'
PAGE_TYPE_CONTACT = 'CONTACT'
PAGE_TYPE_NEWS_DETAIL = 'NEWS_DETAIL'

PAGE_TYPES = {
    PAGE_TYPE_HOME: {
            'title': 'Главная страница',
            'template': 'garpixcms/pages/home.html',
            'context': 'garpix_page.contexts.default.context'
    },
    PAGE_TYPE_DEFAULT: {
            'title': 'Обычная страница',
            'template': 'garpixcms/pages/default.html',
            'context': 'garpix_page.contexts.default.context'
    },
    PAGE_TYPE_CONTACT: {
            'title': 'Страница Контакты',
            'template': 'pages/contact_page.html',
            'context': 'garpix_page.contexts.default.context'
    },
    PAGE_TYPE_NEWS_DETAIL: {
            'title': 'Страница Детальная новость',
            'template': 'pages/news_detail.html',
            'context': 'garpix_page.contexts.default.context'
    },
}

CHOICES_PAGE_TYPES = [(k, v['title']) for k, v in PAGE_TYPES.items()]

```

Пока не добавляйте новости в админ-панели. Сначала сделаем их списочное представление, см. дальше.

**3.2.3. Страница "Список новостей"**

