# Быстрый старт

Необходимо установить Python (рекомендуется `3.8`), Pipenv, Docker и cookiecutter. Подробнее смотрите в разделе [Установка зависимостей](install_deps.md).

Далее создаем [новый проект](install_new_project.md) или [запускаем существующий](install_start_project.md). Перейдите по ссылкам для подробной документации.

Если подробная документация не требуется, то можете использовать команды ниже.

## Новый проект

```bash
cookiecutter https://github.com/garpixcms/garpixcms-empty-template
cd website
cp example.env .env
pipenv install
pipenv shell
docker-compose up -d
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser
python3 backend/manage.py runserver
```

# Запускаем существующий проект

```bash
git clone <repo_url>
cd <directory>
cp example.env .env
pipenv install
pipenv shell
docker-compose up -d
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser
python3 backend/manage.py runserver
```

# Garpix user

Начиная с версии 4.0.0 `garpix_auth` заменен на `garpix_user`.
Если вы использовали `garpix_auth` на проекте с более младшей версией cms, для корректного обновления следуйте инструкциям ниже.

1. Установите новую версию модуля `python3 manage.py garpixcms==4.0.0`.
2. Следуя инструкциям по установке `garpix_user` (https://github.com/garpixcms/garpix_user#quickstart), настройке проект (обратите внимание, что роуты и базовые настройки уже включены в модуль garpixcms в файлах `garpixcms/settings.py` и `garpixcms/urls.py` соответственно).
3. После применения миграций выполните команду `python3 manage.py update_user_module`.
4. Установите переменную окружения `ENABLE_GARPIX_AUTH` в False или просто удалите ее.
