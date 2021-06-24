# Пример реализации входа на сайт

## Реализация входа

#### Шаг 1. Создание нового проекта

Для начала, создайте новый проект по [документации](install_new_project.md).

Если после входа увидите ошибку "No template names provided" - это значит, что можно переходить к следующему шагу.

#### Шаг 2. Включаем вход

Необходимо включить вход в `app/settings.py`:

```python
from garpixcms.settings import *

ENABLE_GARPIX_AUTH = True

```

Это включает следующие точки:

* `/login/` - вход для сайтов на шаблонах, выдает сессию;
* `/logout/` - выйти из системы, удалить токен, сессию;
* `/token-auth/` - вход для SPA сайтов, выдает токен.

## Примеры

Пример использования входа для SPA сайтов через httpie:

#### Шаг 1. Установите httpie:

```
brew install httpie  # для macos
apt-get install httpie -y  # для debian/ubuntu
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

