# Пример реализации входа на сайт на шаблонах

#### Шаг 1. Настраиваем сайт

Создайте главную страницу по примеру из [документации](simple_templates_site.md).

#### Шаг 2. Включите в `.env` вход:

```bash
# ...

ENABLE_GARPIX_AUTH=True

```

Это включает следующие точки:

* `/login/` - вход для сайтов на шаблонах, выдает сессию;
* `/logout/` - выйти из системы, удалить токен, сессию;
* `/api/auth/login/` - вход для SPA сайтов.
* `/api/auth/refresh/` - обновление токена SPA сайтов.
* `/api/auth/logout/` - выход для SPA сайтов.

#### Шаг 3. Создаем страницу входа

Добавим новую модель и создадим тип страницы.

В директории `content/models` создаем файл `login_page.py`.

```python
from garpix_page.models import BasePage


class LoginPage(BasePage):
    
    template = 'garpixcms/pages/login.html'

    class Meta:
        verbose_name = "Страница входа"
        verbose_name_plural = "Страницы входа"
        ordering = ('-created_at',)

```

Изменяем файл `content/models/__init__.py`:

```python
# ...
from .login_page import LoginPage

```

В директории `content/admin` создаем файл `login_page.py`:

```python
from ..models.login_page import LoginPage
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(LoginPage)
class LoginPageAdmin(BasePageAdmin):
    pass

```

Изменяем файл `content/admin/__init__.py`:

```python
# ...
from .login_page import LoginPageAdmin

```

В директории `content/translation` создаем файл `login_page.py`:

```python
from modeltranslation.translator import TranslationOptions, register
from ..models import LoginPage


@register(LoginPage)
class LoginPageTranslationOptions(TranslationOptions):
    pass

```

Изменяем файл `content/translation/__init__.py`:

```python
# ...
from .login_page import LoginPageTranslationOptions

```

Теперь опять создаем миграции и применяем их:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Также, вы можете реализовать другой шаблон. Ниже пример обычного шаблона `garpixcms/pages/login.html`:

```html

{% block content %}
<h1>{{object.title}}</h1>

<h2>Вход</h2>
<p>Чтобы форма входа работала, включите в <code>.env</code> переменную <code>ENABLE_GARPIX_AUTH=True</code></p>
<div>
    {% include 'garpixcms/include/login.html' %}
</div>

{% endblock %}
```

И файла `garpixcms/include/login.html`:

```html
{% if request.user.is_authenticated %}
    User is authenticated ({{request.user.username}}) | <a href="{% url 'logout' %}">Logout</a>
{% else %}
    <form action="{% url 'authorize' %}?next=/" method="post">
        {% csrf_token %}
        <div><input type="text" name="username"></div>
        <div><input type="password" name="password"></div>
        <div><button type="submit">Login</button></div>
    </form>
{% endif %}

```

#### Шаг 4. Создайте в админ-панели страницу входа

Создайте в "Структуре страниц" новую страницу и заполните необходимые поля. Обратите внимание, что ЧПУ не должен совпадать с обработчиком логина (URL: `/login/`)

#### Шаг 5. Попробуйте войти

Перейдите на страницу http://localhost:8000/ и попробуйте войти с помощью формы по умолчанию.
