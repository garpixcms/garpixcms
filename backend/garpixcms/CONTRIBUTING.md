# Contributing

Thanks for your interest in contributing to this project!

## Installation

1. Fork the repository.
2. Clone it on your machine.
3. Install Docker and docker-compose.
   
For Debian, Ubuntu:

```
su
apt update; apt upgrade -y; apt install -y curl; curl -sSL https://get.docker.com/ | sh; curl -L https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
```

Don't forget press CTRL+D to exit from super user account.

4. Apply environment variables:

```
cp example.env .env
```

5. Fill a random string for `SECRET_KEY` in `.env`.

6. Install dependencies:

```
pipenv install
pipenv shell
```

7. Up docker-compose, migrate database and create super user:

```
docker-compose up -d
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser
```

8. Run the server:

```
python3 backend/manage.py runserver
```

9. Make changes and send pull request to main repository.

----

For documentation:

```
mkdocs serve
mkdocs gh-deploy
```