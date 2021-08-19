# Миграция с 1.15.0 на 2.0.0

## На бэкенде

Устанавливаем garpixcms версии 2.0.0:

```bash
pipenv install garpixcms==2.0.0
```

Создать структуру файлов и директорий:

```
app/migrations/garpix_auth/
app/migrations/garpix_auth/__init__.py
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

## На фронтенде SPA

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

Изменить тип токена в заголовках (Headers) с `Token` на `Bearer`. T.е.:

- было: `Authorization: Token 7c21c191a3720925ff80350b395725d31745bcac`
- стало: `Authorization: Bearer 7c21c191a3720925ff80350b395725d31745bcac`

Также, обратите внимание, что раньше ключ в ответе был `token`, стал `access_token`.

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
