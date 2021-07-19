# Пример реализации входа на сайт

## Реализация входа

#### Шаг 1. Создание нового проекта

Для начала, создайте новый проект по [документации](install_new_project.md).

Если после входа увидите ошибку "No template names provided" - это значит, что можно переходить к следующему шагу.

#### Шаг 2. Включаем вход

Необходимо включить вход в `.env`:

```bash
# ...

ENABLE_GARPIX_AUTH=True

```

Это включает следующие точки:

* `/login/` - вход для сайтов на шаблонах, выдает сессию;
* `/logout/` - выйти из системы, удалить токен, сессию;
* `/token-auth/` - вход для SPA сайтов, выдает токен.

## Примеры

### Пример использования входа для SPA сайтов через httpie

#### Шаг 1. Установите httpie:

```
brew install httpie  # для macos
apt-get install httpie -y  # для debian/ubuntu
```

#### Шаг 2. Включите в `.env` вход:

```bash
# ...

ENABLE_GARPIX_AUTH=True

```

#### Шаг 2. Запустите сайт

```bash
python3 backend/manage.py runserver
```

#### Шаг 3. Сделайте запрос на вход

```bash
echo '{"username": "aleksey", "password": "mQZdc5WhVXoxXEno"}' | http POST 'http://localhost:8000/token-auth/'
```

Вывод:

```
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 52
Content-Type: application/json
Date: Thu, 24 Jun 2021 20:34:49 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.10
Vary: Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "token": "5ecb261f8c2f0fea34e9efc6f1823a84501eefda"
}

```

### Пример использования входа для сайтов на шаблонах

#### Шаг 1. Настраиваем сайт

Создайте главную страницу по примеру из [документации](example_simple_templates_site.md).

#### Шаг 2. Включите в `.env` вход:

```bash
# ...

ENABLE_GARPIX_AUTH=True

```

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
{% extends 'garpixcms/base.html' %}

{% block content %}
<h1>{{object.title}}</h1>

<h2>Вход</h2>
<p>Чтобы форма входа работала, включите в <code>app/settings.py</code> переменную <code>ENABLE_GARPIX_AUTH = True</code></p>
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
