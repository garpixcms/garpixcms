# Start project

Зависимости должны быть установлены.

#### Шаг 1. Переходим в существующий проект

Если вы присоединяетесь к проекту, то вам необходимо его склонировать из удаленного репозитория:

```bash
git clone <repo_url>
```

После клонирования или если сайт уже находится локально, то перейдите в его директорию:

```bash
cd <website_directory>
```

#### Шаг 2. Применяем переменные окружения

Загляните в файл `.env`. Вполне возможно, что вы захотите отредактировать содержимое.

```bash
cp example.env .env
```

#### Шаг 3. Устанавливаем зависимые пакеты

Перейдите в директорию с проектом и установите зависимости.

```bash
pipenv install
pipenv shell
```

#### Шаг 4. Поднимаем docker

Поднимаем базу данных и другие сервисы через docker-compose.

```bash
docker-compose up -d
```

#### Шаг 5. Применяем миграции и создаем суперпользователя

```bash
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser
```

#### Шаг 6. Запускаем сервер

```bash
python3 backend/manage.py runserver
```