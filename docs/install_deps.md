# Установка зависимостей

### Зависимости:

- Python (рекомендуется использовать `3.8`)
- Pipenv
- Docker
- docker-compose
- cookiecutter

### Установка

#### Шаг 1. Устанавливаем Docker и docker-compose

```bash
su
apt update; apt upgrade -y; apt install -y curl; curl -sSL https://get.docker.com/ | sh; curl -L https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
usermod -aG docker $USER
```

Затем нажмите Ctrl+D для того, чтобы выйти из учетной записи суперпользователя и перезагрузите компьютер.

#### Шаг 2. Устанавливаем [cookiecutter](http://cookiecutter.readthedocs.io)

Cookiecutter используется для генерации нового сайта из шаблона.

```bash
pip3 install cookiecutter
```

#### Шаг 3. Устанавливаем [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)

Pipenv помогает управлять зависимостями в проекте. Он делает это лучше, чем стандартный `pip`.

```bash
pip3 install pipenv
```

Если вы на MacOS, то можете использовать brew:

```bash
brew install pipenv
```
    