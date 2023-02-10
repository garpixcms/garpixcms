# Пример реализации входа на SPA-сайт (React, Vue.js, Angular)

#### Шаг 1. Создание нового проекта

Для начала, создайте новый проект по [документации](../install_new_project.md).

#### Шаг 2. Включаем вход

Необходимо включить вход в `.env`:

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

## Примеры

### Пример использования входа для SPA сайтов через httpie

#### Шаг 1. Установите httpie

```
brew install httpie  # для macos
apt-get install httpie -y  # для debian/ubuntu
```

#### Шаг 2. Настройте вход

Файл `.env`:

```bash
# ...

ENABLE_GARPIX_AUTH=True
```

Создание и применение миграций:

```bash
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
```

Указать в `backend/app/settings.py` переменные (если указать значение `0` - протухать не будет):

```python
GARPIX_ACCESS_TOKEN_TTL_SECONDS = 86400  # Токен будет протухать через сутки
GARPIX_REFRESH_TOKEN_TTL_SECONDS = 86400 * 14  # Рефреш-токен будет протухать после 14 суток
```

#### Шаг 3. Запустите сайт

```bash
python3 backend/manage.py runserver
```

#### Шаг 4. Сделайте запрос на вход

Изменить адрес логина с `/api/login/` на `/api/auth/login/`.

Пример запроса (в качестве примера используется httpie):

```bash
http POST 'http://localhost:8000/api/auth/login/' username=user password=mysuperpassword
```

Пример ответа:

```json
{
    "access_token": "7c21c191a3720925ff80350b395725d31745bcac",
    "access_token_expires": 86400,
    "refresh_token": "946cd6498df1de4bb24d0fc63286b01341265b3e",
    "refresh_token_expires": 1209600,
    "token_type": "Bearer"
}
```

#### Шаг 5. Обновляйте протухший токен

Если `access_token` протух, то запросы проходить не будут.
Тогда необходимо обновить токен с помощью этой команды (в качестве примера используется httpie):

```bash
http POST 'http://localhost:8000/api/auth/refresh/' refresh_token=946cd6498df1de4bb24d0fc63286b01341265b3e
```

Пример ответа:

```json
{
    "access_token": "227b68233b26ab16239db556a267a4f849fd882c",
    "access_token_expires": 86400,
    "result": true
}
```

При этом, если refresh-токен протух, то ответ будет:

```json
{
    "result": false
}
```

#### Шаг 6. Удаляйте токены при выходе

Также, когда необходимо удалить все токены с бэкенда (сделать выход), то
используем следующую команду (в качестве примера используется httpie):

```bash
http POST 'http://localhost:8000/api/auth/logout/' 'Authorization: Bearer 227b68233b26ab16239db556a267a4f849fd882c'
```

В случае успеха будет ответ:

```json
{
    "result": true
}
```

В случае неудачи будет статус-код `401 Unauthorized`.
